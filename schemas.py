from pydantic import BaseModel, field_validator, ConfigDict


class TaskCreate(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str):
        if not value.strip():
            raise ValueError("Text is empty")

        return value


class TaskResponse(BaseModel):
    id: int
    text: str

    model_config = ConfigDict(from_attributes=True)
