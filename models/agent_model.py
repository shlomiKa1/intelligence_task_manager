from pydantic import BaseModel, Field
from typing import Literal

Rank = Literal["Commander", "Senior", "Junior"]

class Agent(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    specialty: str = Field(min_length=1, max_length=255)
    is_active: bool = Field(default=True)
    completed_missions: int
    failed_missions: int
    agent_rank: Rank

class Updateagent(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    specialty: str | None = Field(default=None, min_length=1, max_length=255)
    is_active: bool | None = Field(default=True or None)
    completed_missions: int | None = None
    failed_missions: int | None = None
    agent_rank: Rank | None = None
