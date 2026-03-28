from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """
    Abstract base class for all agent adapters.

    Every concrete agent must implement execute(), which receives
    a validated input dict and returns a strictly structured result dict.

    Contract:
      - Input:  dict  (keys vary by task; validated upstream)
      - Output: dict  with exactly these keys:

          {
              "result":     str,            # the agent's primary output
              "warning":    str | None,      # non-fatal issue, or None
              "confidence": str,             # "high" | "medium" | "low"
          }

    All three keys are REQUIRED. Missing keys will cause downstream
    data-layer failures in later checkpoints.
    """

    @abstractmethod
    def execute(self, input: dict) -> dict:
        """
        Run the agent's core logic against the provided input.

        Args:
            input: Dict of task inputs (e.g. {"query": "...", "search_scope": "web"})

        Returns:
            Dict with keys: "result" (str), "warning" (str | None),
            "confidence" ("high" | "medium" | "low").

        Raises:
            Exception: Propagated to execution engine for failure handling.
        """
        ...  # pragma: no cover
