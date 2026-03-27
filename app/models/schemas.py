from typing import Any, Optional
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Standard envelope — used from Checkpoint 11 onward
# { "status": "success", "data": {...}, "error": null }
# ---------------------------------------------------------------------------
class StandardResponse(BaseModel):
    status: str
    data: Optional[Any] = None
    error: Optional[str] = None


# ---------------------------------------------------------------------------
# Workflow
# ---------------------------------------------------------------------------
class WorkflowRequest(BaseModel):
    query: str = Field(..., min_length=1, description="The query string to process")


class WorkflowResponse(BaseModel):
    status: str
    query: str
