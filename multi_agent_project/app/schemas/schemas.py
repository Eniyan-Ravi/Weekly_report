from typing import Literal

from pydantic import BaseModel, Field


class TaskRoute(BaseModel):
    task: Literal["email", "blog", "research"] = Field(
        description="The type of task requested by the user."
    )