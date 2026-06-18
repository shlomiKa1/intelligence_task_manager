

from pydantic import BaseModel, Field
from typing import Literal


Status = Literal["NEW", "ASSIGNED", "IN_PROGRESS", "COMPLETED", "FAILED", "CANCELLED"]

class Mission(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1)
    location: str = Field(min_length=1, max_length=255)
    difficulty: int
    importance: int
    status: Status = Field(default="NEW")
    assigned_agent_id: int = Field(default=None)
