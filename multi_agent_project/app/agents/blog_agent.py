
from langchain_core.prompts import ChatPromptTemplate

from app.models.llm import get_llm
from app.schemas.schemas import BlogStyle

STYLE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Extract the blog style, tone or audience the user asked for "
            "(e.g. 'casual', 'technical', 'for beginners'). If none is "
            "stated, use 'informative and engaging'.",
        ),
        ("human", "{user_request}"),
    ]
)

BLOG_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """ROLE
You are a blog writing agent.

TASK
Convert the provided research into a blog post in the requested style.

CONTEXT
The Research Agent's output below is your ONLY factual context.
{revision_context}

CONSTRAINTS
- Do not perform independent research.
- Do not add facts, numbers or claims that the research does not support.
- Carry over the research's uncertainty notes; do not overstate.
- Follow the requested style.

OUTPUT REQUIREMENTS
A complete blog: title, short introduction, headed sections, conclusion.""",
        ),
        (
            "human",
            """Original request:
{user_request}

Requested blog style:
{blog_style}

Research (factual context):
{research_output}""",
        ),
    ]
)


def extract_blog_style(user_request: str):
    llm = get_llm(temperature=0).with_structured_output(BlogStyle)
    return (STYLE_PROMPT | llm).invoke({"user_request": user_request}).style


def generate_blog(user_request: str,research_output: str,blog_style: str,previous_blog: str | None = None,
    feedback: str | None = None,):
    revision_context = ""
    if previous_blog:
        revision_context = (
            "\nThis is a revision. Rewrite the blog using the reviewer "
            f"feedback.\nPrevious blog:\n{previous_blog}\n"
            f"Reviewer feedback: {feedback or 'None provided'}\n"
        )
    response = (BLOG_PROMPT | get_llm()).invoke(
        {
            "user_request": user_request,
            "blog_style": blog_style,
            "research_output": research_output,
            "revision_context": revision_context,
        }
    )
    return response.content
