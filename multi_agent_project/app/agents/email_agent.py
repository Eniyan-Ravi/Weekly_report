from langchain_core.prompts import ChatPromptTemplate

from app.models.llm import get_llm
from app.schemas.schemas import EmailDraft
EMAIL_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """ROLE
You are an expert email writing agent.

TASK
Write one email that fulfils the user's request.

CONTEXT
Selected tone: {tone}

Tone rules (follow exactly):
{tone_rules}

This is version {version_number} of at most 3.
Previous version (None if this is the first):
{previous_email}

Reviewer feedback on the previous version (None if not provided):
{feedback}

CONSTRAINTS
- Preserve the user's original intent exactly.
- Keep the selected tone and follow every tone rule.
- Do not invent important facts (dates, names, numbers). Use bracketed
  placeholders such as [Manager's Name] or [Date] when details are missing.
- If a previous version exists, write a clearly DIFFERENT version:
  different opening, structure and wording, same intent and same tone.

OUTPUT REQUIREMENTS
Return a subject line and a complete email body. No commentary.""",
        ),
        ("human", "{user_request}"),
    ]
)


def format_email(draft: EmailDraft):
    return f"Subject: {draft.subject}\n\n{draft.body}"


def generate_email(user_request: str,tone: str,tone_rules: str,retry_count: int = 0,previous_email: str | None = None,
    feedback: str | None = None,):
    llm = get_llm().with_structured_output(EmailDraft).with_retry(stop_after_attempt=3)
    draft = (EMAIL_PROMPT | llm).invoke(
        {
            "user_request": user_request,
            "tone": tone,
            "tone_rules": tone_rules,
            "version_number": retry_count + 1,
            "previous_email": previous_email or "None",
            "feedback": feedback or "None",
        }
    )
    return format_email(draft)
