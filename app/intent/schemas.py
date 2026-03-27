from pydantic import BaseModel


class TaskItem(BaseModel):
    task: str
    input: dict


class IntentResponse(BaseModel):
    tasks: list[TaskItem]
