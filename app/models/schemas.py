
from pydantic import BaseModel, Field


class WorkflowRequest(BaseModel):
    query: str = Field(..., min_length=1, description="The query string to process")


class WorkflowResponse(BaseModel):
    status: str
    query: str
