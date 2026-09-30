from langchain_core.prompts import ChatPromptTemplate

from app.models.llm import get_llm
from app.tools.research_tools import RESEARCH_TOOLS

TOOLS_BY_NAME = {t.name: t for t in RESEARCH_TOOLS}
MAX_TOOL_ROUNDS = 3

RESEARCH_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """ROLE
You are a research agent.

TASK
Produce clear, factual, well-structured research on the user's request.

CONTEXT
You have a `search_research` tool. Use it to look up information.
If the tool reports that no live search backend is configured, rely only
on well-established knowledge and say so.
{revision_context}

CONSTRAINTS
- Focus only on research. Do NOT write a blog, article or other creative content.
- Do not invent facts, statistics, quotes or sources.
- Clearly mark anything uncertain or unverified.

OUTPUT REQUIREMENTS
Structured notes: overview, key findings (bullets), important details,
and a short 'Limitations / uncertainty' section.""",
        ),
        ("human", "{user_request}"),
    ]
)

def _invoke_with_tool_retry(tool_llm, plain_llm, messages, attempts: int = 3):
    """Retry malformed tool calls; fall back to a plain answer if they persist."""
    for _ in range(attempts):
        try:
            return tool_llm.invoke(messages)
        except Exception as exc:
            if "tool_use_failed" not in str(exc):
                raise
    return plain_llm.invoke(messages)

def research_topic(user_request: str,previous_output: str | None = None,feedback: str | None = None,):
    revision_context = ""
    if previous_output:
        revision_context = (
            "\nThis is a revision. Improve the previous research using the "
            f"reviewer feedback.\nPrevious research:\n{previous_output}\n"
            f"Reviewer feedback: {feedback or 'None provided'}\n"
        )

    llm = get_llm()
    tool_llm = llm.bind_tools(RESEARCH_TOOLS)
    messages = RESEARCH_PROMPT.format_messages(
        user_request=user_request, revision_context=revision_context
    )

    for _ in range(MAX_TOOL_ROUNDS):
        response = _invoke_with_tool_retry(tool_llm, llm, messages)
        messages.append(response)
        if not response.tool_calls:
            return response.content
        for call in response.tool_calls:
            messages.append(TOOLS_BY_NAME[call["name"]].invoke(call))

    return llm.invoke(messages).content


