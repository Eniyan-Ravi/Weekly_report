from langchain_core.prompts import ChatPromptTemplate

from app.models.llm import llm

def generate_email(user_request: str,tone: str,tone_rules: str,retry_count: int = 0,) -> str:

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are an email writing agent.

Write an email based on the user's request.

Follow the selected tone and all tone rules exactly.

The email must:
- Preserve the user's original intent.
- Follow the selected tone.
- Be clear and natural.
- Not invent important facts.
- Produce a different version when retry_count is greater than 0.

Selected tone:
{tone}

Tone rules:
{tone_rules}

Retry count:
{retry_count}
""",
            ),
            (
                "human",
                "{user_request}",
            ),
        ]
    )

    chain = prompt | llm

    response = chain.invoke(
        {
            "user_request": user_request,
            "tone": tone,
            "tone_rules": tone_rules,
            "retry_count": retry_count,
        }
    )

    return response.content