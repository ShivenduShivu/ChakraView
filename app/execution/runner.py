import logging
from app.workflow.models import WorkflowStep

logger = logging.getLogger(__name__)


def execute_step(step: WorkflowStep) -> dict:
    """
    Execute a single workflow step.
    Returns a mock result for now — real adapter logic added in later checkpoint.
    """
    logger.info("[runner] Executing step %d | task: %s | agent: %s",
                step.step_id, step.task, step.agent)

    # Mock execution — replace with real agent adapter in later checkpoint
    result = {
        "result": f"Executed {step.task}",
        "status": "completed",
    }

    logger.info("[runner] Step %d completed | result: %s", step.step_id, result)
    return result
