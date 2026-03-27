import logging
from app.intent.schemas import IntentResponse
from app.registry.loader import get_task, get_all_agents
from app.validation.errors import (
    ValidationError,
    TaskNotFoundError,
    MissingInputError,
    InvalidInputError,
)

logger = logging.getLogger(__name__)


def validate_tasks(intent_response: IntentResponse) -> None:
    """
    Validate every task in an IntentResponse against the registry.

    Rules enforced per task:
      1. Task must exist in registry             → TaskNotFoundError
      2. Input must be a dict                    → InvalidInputError
      3. All required_inputs must be present     → MissingInputError
      4. All allowed_agents must exist in agents registry
    """
    # Build agent ID set once — used for allowed_agents check
    all_agent_ids = {a["agent_id"] for a in get_all_agents()}

    for item in intent_response.tasks:
        task_name = item.task

        # Rule 1 — task must exist in registry
        registry_task = get_task(task_name)
        if registry_task is None:
            raise TaskNotFoundError(task_name)

        logger.info("[validation] Task found in registry: %s", task_name)

        # Rule 2 — input must be a dict
        if not isinstance(item.input, dict):
            raise InvalidInputError(task_name)

        logger.info("[validation] Input type valid for task: %s", task_name)

        # Rule 3 — all required_inputs must be present in input
        required_inputs = registry_task.get("required_inputs", [])
        for field in required_inputs:
            if field not in item.input:
                raise MissingInputError(task_name, field)

        logger.info("[validation] All required inputs present for task: %s", task_name)

        # Rule 4 — all allowed_agents for this task must exist in agents registry
        allowed_agents = registry_task.get("allowed_agents", [])
        for agent_id in allowed_agents:
            if agent_id not in all_agent_ids:
                raise ValidationError(
                    f"Invalid agent mapping for task '{task_name}': "
                    f"agent '{agent_id}' not found in registry."
                )

        logger.info("[validation] Task '%s' passed all validation rules.", task_name)

    logger.info("[validation] All %d task(s) validated successfully.", len(intent_response.tasks))
