import json
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# Registry directory — always relative to this file
REGISTRY_DIR = Path(__file__).parent

# In-memory storage
_agents: list = []
_tasks: list = []


def load_agents() -> list:
    """Read agents.json and store contents in memory."""
    global _agents

    agents_path = REGISTRY_DIR / "agents.json"

    with open(agents_path, "r") as f:
        data = json.load(f)

    _agents = data["agents"]

    logger.info("Registry loaded: %d agent(s) loaded from %s", len(_agents), agents_path.name)
    print(f"[registry] {len(_agents)} agent(s) loaded: {[a['agent_id'] for a in _agents]}")

    return _agents


def load_tasks() -> list:
    """Read tasks.json and store contents in memory."""
    global _tasks

    tasks_path = REGISTRY_DIR / "tasks.json"

    with open(tasks_path, "r") as f:
        data = json.load(f)

    _tasks = data["tasks"]

    logger.info("Registry loaded: %d task(s) loaded from %s", len(_tasks), tasks_path.name)
    print(f"[registry] {len(_tasks)} task(s) loaded: {[t['task_name'] for t in _tasks]}")

    return _tasks


# ---------------------------------------------------------------------------
# Access functions
# ---------------------------------------------------------------------------

def get_all_agents() -> list:
    """Return all loaded agents."""
    return _agents


def get_agent(agent_id: str) -> Optional[dict]:
    """Return a single agent by agent_id. Returns None if not found."""
    return next((a for a in _agents if a["agent_id"] == agent_id), None)


def get_all_tasks() -> list:
    """Return all loaded tasks."""
    return _tasks


def get_task(task_name: str) -> Optional[dict]:
    """Return a single task by task_name. Returns None if not found."""
    return next((t for t in _tasks if t["task_name"] == task_name), None)
