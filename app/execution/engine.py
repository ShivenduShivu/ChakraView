import logging
from datetime import datetime, timezone
from app.workflow.models import WorkflowStep
from app.workflow.state import StepStatus
from app.adapters.registry import get_agent_adapter

logger = logging.getLogger(__name__)


def run_workflow(steps: tuple[WorkflowStep, ...]) -> dict:
    """
    Execute all workflow steps sequentially with status tracking.

    Logic per step:
      1. Set status = running
      2. Call execute_step()
      3. On success: set status = completed, collect result
      4. On error:   set status = failed, break execution

    Returns:
      {
        "steps":   list of updated WorkflowStep,
        "results": list of { step_id, task, result, error, timestamp }
      }
    """
    updated_steps = []
    results       = []

    for step in steps:

        # Step 1 — mark as running
        step = step.model_copy(update={"status": StepStatus.running})
        logger.info("[execution] Step %d | status: running | task: %s",
                    step.step_id, step.task)

        try:
            # Step 2 — resolve adapter and execute
            adapter = get_agent_adapter(step.agent)
            outcome = adapter.execute(step.input)

            # Step 3 — mark as completed
            step = step.model_copy(update={"status": StepStatus.completed})
            logger.info("[execution] Step %d | status: completed", step.step_id)

            results.append({
                "step_id":    step.step_id,
                "task":       step.task,
                "result":     outcome.get("result"),
                "warning":    outcome.get("warning"),
                "confidence": outcome.get("confidence"),
                "error":      None,
                "timestamp":  datetime.now(timezone.utc).isoformat(),
            })

        except Exception as e:
            # Step 4 — mark as failed, stop execution
            step = step.model_copy(update={"status": StepStatus.failed})
            logger.error("[execution] Step %d | status: failed | error: %s",
                         step.step_id, str(e))

            results.append({
                "step_id":   step.step_id,
                "task":      step.task,
                "result":    None,
                "error":     str(e),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })

            updated_steps.append(step)
            logger.error("[execution] Halting workflow at step %d.", step.step_id)
            break

        updated_steps.append(step)

    logger.info("[execution] Workflow complete | %d/%d step(s) executed.",
                len(updated_steps), len(steps))

    return {
        "steps":   updated_steps,
        "results": results,
    }
