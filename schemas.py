from pydantic import BaseModel


class TaskCreate(BaseModel):
    text: str
