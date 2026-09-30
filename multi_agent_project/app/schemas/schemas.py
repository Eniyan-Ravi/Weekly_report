from typing import Literal

from pydantic import BaseModel, Field


class TaskRoute(BaseModel):
    task: Literal["email", "blog", "research"] = Field(
        description="The type of task requested by the user."
    )


class EmailDraft(BaseModel):
    subject: str = Field(description="Concise email subject line.")
    body: str = Field(
        description="Complete email body including greeting and sign-off."
    )


class BlogStyle(BaseModel):
    style: str = Field(
        description=(
            "Requested blog style/tone/audience in a short phrase. "
            "Use 'informative and engaging' if none was requested."
        )
    )
