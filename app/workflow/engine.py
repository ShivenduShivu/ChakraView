import logging
from app.intent.schemas import IntentResponse
from app.registry.loader import get_task
from app.workflow.models import WorkflowStep
from app.workflow.state import StepStatus

logger = logging.getLogger(__name__)


def build_workflow(intent_response: IntentResponse) -> tuple[WorkflowStep, ...]:
    """
    Convert a validated IntentResponse into an ordered list of WorkflowSteps.

    Logic per task:
      1. Fetch task info from registry
      2. Assign first allowed_agent as the executor
      3. Create WorkflowStep with status=pending
      4. Raise ValueError if no agent is available
    """
    steps = []

    for step_id, item in enumerate(intent_response.tasks, start=1):
        task_name = item.task

        # Step 1 — fetch task info from registry
        registry_task = get_task(task_name)
        if registry_task is None:
            raise ValueError(f"Task '{task_name}' not found in registry.")

        # Step 2 — assign first allowed agent
        allowed_agents = registry_task.get("allowed_agents", [])
        if not allowed_agents:
            raise ValueError(
                f"Task '{task_name}' has no allowed agents assigned in registry."
            )
        assigned_agent = allowed_agents[0]

        # Step 3 — build WorkflowStep
        step = WorkflowStep(
            step_id = step_id,
            task    = task_name,
            agent   = assigned_agent,
            input   = item.input,
            status  = StepStatus.pending,
        )
        steps.append(step)

        logger.info(
            "[workflow] Step %d | task: %s | agent: %s | status: %s",
            step_id, task_name, assigned_agent, StepStatus.pending,
        )

    frozen_steps = tuple(steps)
    logger.info("[workflow] Built %d step(s) in workflow (frozen).", len(frozen_steps))
    return frozen_steps
