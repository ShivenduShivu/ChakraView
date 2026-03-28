import logging
from app.adapters.base import BaseAgent
from app.adapters.mock_agents import ResearchAgent, SummaryAgent, ReportAgent

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Adapter registry — maps agent_id (from tasks.json) to agent instance
# ---------------------------------------------------------------------------

AGENT_REGISTRY: dict[str, BaseAgent] = {
    "research_agent": ResearchAgent(),
    "summary_agent":  SummaryAgent(),
    "report_agent":   ReportAgent(),
}


def get_agent_adapter(agent_name: str) -> BaseAgent:
    """
    Look up and return the adapter instance for the given agent name.

    Args:
        agent_name: The agent_id string (e.g. "research_agent").
                    Must match a key in AGENT_REGISTRY.

    Returns:
        Concrete BaseAgent instance ready to call .execute() on.

    Raises:
        ValueError: If agent_name is not registered.
    """
    if agent_name not in AGENT_REGISTRY:
        registered = list(AGENT_REGISTRY.keys())
        logger.error(
            "[adapter-registry] Unknown agent '%s'. Registered: %s",
            agent_name, registered,
        )
        raise ValueError(f"Adapter not found for agent '{agent_name}'")

    adapter = AGENT_REGISTRY[agent_name]
    logger.info("[adapter-registry] Resolved adapter for '%s': %s",
                agent_name, type(adapter).__name__)
    return adapter
