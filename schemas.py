from pydantic import BaseModel, field_validator, ConfigDict


class TaskBase(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str):
        if not value.strip():
            raise ValueError("Text is empty")

        return value


class TaskCreate(TaskBase):
    pass


class TaskResponse(TaskBase):
    id: int
    completed: bool

    model_config = ConfigDict(from_attributes=True)


class TaskUpdate(TaskBase):
    completed: bool
