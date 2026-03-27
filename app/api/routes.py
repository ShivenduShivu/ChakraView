from fastapi import APIRouter
from app.models.schemas import WorkflowRequest, WorkflowResponse

router = APIRouter()


@router.post("/run-workflow", response_model=WorkflowResponse)
async def run_workflow(payload: WorkflowRequest) -> WorkflowResponse:
    """
    Accepts a workflow query and acknowledges receipt.
    Business logic will be wired in future checkpoints.
    """
    return WorkflowResponse(status="received", query=payload.query)
