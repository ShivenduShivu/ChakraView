from pydantic import BaseModel
from app.workflow.state import StepStatus


class WorkflowStep(BaseModel):
    step_id:     int
    task:        str
    agent:       str
    input:       dict
    status:      StepStatus
    workflow_id: str = ""   # placeholder — populated by workflow runner in later checkpoint
