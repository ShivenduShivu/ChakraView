def build_prompt(query: str, tasks: tuple) -> str:
    """
    Build a structured prompt for the LLM.
    Dynamically lists all registry tasks so LLM is strictly bound to them.
    """
    task_lines = "\n".join(
        f"  - {t['task_name']}: {t['description']}"
        for t in tasks
    )

    prompt = f"""You are an intent parser for a workflow engine.

Given a user query, extract the tasks that need to be executed.

AVAILABLE TASKS ONLY (do not use any task not listed here):
{task_lines}

RULES:
- You MUST only use tasks from the list above.
- Output ONLY a valid JSON object. No explanation. No extra text.
- Format:
{{
  "tasks": [
    {{"task": "<task_name>", "input": {{}}}},
    ...
  ]
}}

USER QUERY:
{query}

JSON OUTPUT:"""

    return prompt
