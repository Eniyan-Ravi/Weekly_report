from typing import TypedDict, Literal


class State(TypedDict, total=False):

    user_request: str

    task_type: Literal["email", "blog", "research"]

    email_tone: str
    email_tone_rules: str
    email_output: str
    email_retry_count: int

    research_output: str

    blog_style: str
    blog_output: str

    final_output: str
    review_feedback: str
    approval_status: Literal["approved", "rejected"]