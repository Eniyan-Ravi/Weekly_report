from typing import TypedDict


class State(TypedDict, total=False):
    user_request: str
    task_type: str

    email_tone: str
    email_tone_rules: str
    email_output: str
    email_retry_count: int  # revisions requested for the email

    research_output: str

    blog_style: str
    blog_output: str
    revision_count: int  # revisions requested for research/blog

    final_output: str
    review_feedback: str
    approval_status: str
