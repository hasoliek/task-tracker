from datetime import date, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TaskStatus(str, Enum):
    TODO = "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"


class TaskPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


def validate_and_clean_tags(tags: list[str]) -> list[str]:
    cleaned_tags: list[str] = []

    for tag in tags:
        cleaned_tag = tag.strip()

        # Reject blank tags rather than silently removing them.
        if not cleaned_tag:
            raise ValueError("Tags cannot be blank")

        if cleaned_tag not in cleaned_tags:
            cleaned_tags.append(cleaned_tag)

    return cleaned_tags


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: str | None = None
    due_date: date | None = None
    tags: list[str] = Field(default_factory=list)

    @field_validator("title", mode="before")
    @classmethod
    def validate_title(cls, value: Any) -> Any:
        if not isinstance(value, str):
            return value

        cleaned_title = value.strip()

        if not cleaned_title:
            raise ValueError("Title cannot be blank")

        return cleaned_title

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, value: list[str]) -> list[str]:
        return validate_and_clean_tags(value)


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    status: TaskStatus = None
    priority: TaskPriority = None
    assignee: str | None = None
    due_date: date | None = None
    tags: list[str] | None = None

    @field_validator("title", mode="before")
    @classmethod
    def validate_title(cls, value: Any) -> Any:
        if not isinstance(value, str):
            return value

        cleaned_title = value.strip()

        if not cleaned_title:
            raise ValueError("Title cannot be blank")

        return cleaned_title

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, value: list[str] | None) -> list[str] | None:
        if value is None:
            return value

        return validate_and_clean_tags(value)


class TaskResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    assignee: str | None = None
    due_date: date | None = None
    tags: list[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime