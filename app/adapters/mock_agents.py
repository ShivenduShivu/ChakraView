import logging
from app.adapters.base import BaseAgent

logger = logging.getLogger(__name__)


class ResearchAgent(BaseAgent):
    """
    Mock adapter for research_agent.
    Handles tasks: search_information, analyze_data
    """

    def execute(self, input: dict) -> dict:
        logger.info("[ResearchAgent] execute called | input keys: %s", list(input.keys()))

        result = (
            f"ResearchAgent completed research. "
            f"Query scope: '{input.get('search_scope') or input.get('analysis_type', 'general')}'. "
            f"Data processed successfully."
        )

        logger.info("[ResearchAgent] result produced.")
        return {
            "result":     result,
            "warning":    None,
            "confidence": "high",
        }


class SummaryAgent(BaseAgent):
    """
    Mock adapter for summary_agent.
    Handles tasks: summarize
    """

    def execute(self, input: dict) -> dict:
        logger.info("[SummaryAgent] execute called | input keys: %s", list(input.keys()))

        max_length = input.get("max_length", "unspecified")
        result = (
            f"SummaryAgent condensed content. "
            f"Target length: {max_length} words. "
            f"Summary generated from source text."
        )

        logger.info("[SummaryAgent] result produced.")
        return {
            "result":     result,
            "warning":    None,
            "confidence": "medium",
        }


class ReportAgent(BaseAgent):
    """
    Mock adapter for report_agent.
    Handles tasks: generate_report, summarize
    """

    def execute(self, input: dict) -> dict:
        logger.info("[ReportAgent] execute called | input keys: %s", list(input.keys()))

        report_format = input.get("report_format", "default")
        result = (
            f"ReportAgent generated structured report. "
            f"Format: {report_format}. "
            f"Insights compiled from analyzed data and summary."
        )

        logger.info("[ReportAgent] result produced.")
        return {
            "result":     result,
            "warning":    None,
            "confidence": "high",
        }
