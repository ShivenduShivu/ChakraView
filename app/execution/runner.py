# ---------------------------------------------------------------------------
# runner.py — SUPERSEDED by Checkpoint 7: Adapter Layer
# ---------------------------------------------------------------------------
# execute_step() has been removed.
# The execution engine (engine.py) now resolves agents via:
#
#   from app.adapters.registry import get_agent_adapter
#   adapter = get_agent_adapter(step.agent)
#   outcome = adapter.execute(step.input)
#
# This file is intentionally kept as a placeholder.
# It will be repurposed in a future checkpoint if needed.
# ---------------------------------------------------------------------------
