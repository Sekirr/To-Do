from pydantic import BaseModel, field_validator


class TaskCreate(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def validate_text(cls, value):
        if not value.strip():
            raise ValueError("Text is empty")

        return value
