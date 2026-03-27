import json
import logging
from app.registry.loader import get_all_tasks, get_task
from app.intent.prompt import build_prompt
from app.intent.schemas import TaskItem, IntentResponse

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Mock LLM — returns hardcoded JSON based on keywords in query
# Replace this with a real LLM call (OpenAI, etc.) in a later checkpoint
# ---------------------------------------------------------------------------
def _mock_llm(prompt: str, query: str) -> str:
    query_lower = query.lower()

    # NOTE: summarize check must come before search/find
    # because "findings" contains "find" — would cause false match
    if "summar" in query_lower:
        return json.dumps({
            "tasks": [
                {"task": "summarize", "input": {}}
            ]
        })

    if "revenue" in query_lower and "report" in query_lower:
        return json.dumps({
            "tasks": [
                {"task": "analyze_data",    "input": {}},
                {"task": "generate_report", "input": {}}
            ]
        })

    if "search" in query_lower or "find" in query_lower:
        return json.dumps({
            "tasks": [
                {"task": "search_information", "input": {}}
            ]
        })

    # Default fallback
    return json.dumps({
        "tasks": [
            {"task": "search_information", "input": {}},
            {"task": "analyze_data",       "input": {}}
        ]
    })


# ---------------------------------------------------------------------------
# Core intent parsing function
# ---------------------------------------------------------------------------
def parse_intent(query: str) -> IntentResponse:
    """
    Convert a user query into a validated list of registry-bound tasks.

    Steps:
      1. Fetch tasks from registry
      2. Build LLM prompt
      3. Call LLM (mocked for now)
      4. Parse JSON response
      5. Validate each task exists in registry
      6. Return structured IntentResponse
    """
    # Step 1 — get registry tasks
    tasks = get_all_tasks()

    # Step 2 — build prompt
    prompt = build_prompt(query, tasks)
    logger.info("[intent] Prompt built for query: %s", query)

    # Step 3 — call LLM (mocked)
    raw_output = _mock_llm(prompt, query)
    logger.info("[intent] Raw LLM output: %s", raw_output)

    # Step 4 — parse JSON
    try:
        parsed = json.loads(raw_output)
    except json.JSONDecodeError as e:
        raise ValueError(f"LLM returned invalid JSON: {e}")

    # Step 5 — validate each task against registry
    valid_task_names = {t["task_name"] for t in tasks}
    validated_tasks = []
    parsed_tasks = parsed.get("tasks", [])

    if not parsed_tasks:
        raise ValueError("No tasks generated from intent engine")

    for item in parsed_tasks:
        task_name = item.get("task", "").strip()  # normalize: strip whitespace

        if task_name not in valid_task_names:
            raise ValueError(
                f"Invalid task '{task_name}' returned by LLM. "
                f"Allowed tasks: {sorted(valid_task_names)}"
            )

        validated_tasks.append(TaskItem(task=task_name, input=item.get("input", {})))
        logger.info("[intent] Validated task: %s", task_name)

    # Step 6 — return structured response
    result = IntentResponse(tasks=validated_tasks)
    logger.info("[intent] IntentResponse built with %d task(s)", len(result.tasks))

    return result
