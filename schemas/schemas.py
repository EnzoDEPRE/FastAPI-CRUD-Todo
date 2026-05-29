
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TodoStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"


class TodoCreate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    title: str = Field(..., min_length=1, description="Title must not be empty")
    description: Optional[str] = None
    status: TodoStatus = TodoStatus.pending

class TodoUpdate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    title: Optional[str] = Field(None, min_length=1, description="Title must not be empty")
    description: Optional[str] = None
    status: Optional[TodoStatus] = None

class TodoOut(TodoCreate):
    id: int
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
