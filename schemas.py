from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator


class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=50)
    priority: Literal["low", "medium", "high"]
    description: Optional[str] = "No description"

    @field_validator("title")
    @classmethod
    def title_must_start_with_uppercase(cls, value):
        if not value[0].isupper():
            raise ValueError("Title must start with an uppercase letter")
        return value


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=50)
    priority: Optional[Literal["low", "medium", "high"]] = None
    description: Optional[str] = None

    @field_validator("title")
    @classmethod
    def title_must_start_with_uppercase(cls, value):
        # Only check the title if the user actually sent one
        if value is None:
            return value
        if not value[0].isupper():
            raise ValueError("Title must start with an uppercase letter")
        return value


class TaskResponse(BaseModel):
    task_id: int
    title: str
    priority: str
    description: str
    status: str


# Serialization demo: run "python schemas.py" to see it
if __name__ == "__main__":
    task = TaskCreate(title="Buy groceries", priority="high")

    print("As dictionary:")
    print(task.model_dump())

    print("As JSON:")
    print(task.model_dump_json())