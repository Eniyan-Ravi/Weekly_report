import os
import json
from dotenv import load_dotenv
from pathlib import Path
from groq import Groq

from rag.retrieval.hybrid_search import hybrid_search
from rag.vectorstore.faiss_store import load_index
from rag.retrieval.keyword_search import build_bm25_index
from rag.tools.tool_definitions import tool_definitions, tool_function_map

ENV_PATH = Path(__file__).parent / ".env"
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL_NAME = "openai/gpt-oss-120b"

_index, _chunks = load_index()
_bm25 = build_bm25_index(_chunks)


def answer_question(question: str, db, current_user, top_k: int = 3) -> str:
    retrieved_chunks = hybrid_search(question, _index, _bm25, _chunks, top_k=top_k)

    context_text = "\n\n".join(
        f"[Source: {chunk['source']}]\n{chunk['text']}"
        for chunk in retrieved_chunks
    )

    system_prompt = (
        "You are a helpful assistant for a subscription and EMI tracking app.\n\n"
        "You have two sources of information:\n"
        "1. Behavioral and policy guidance retrieved below — use this to decide HOW to respond.\n"
        "2. Tools that fetch the user's real, live data — use these whenever the user asks "
        "about their actual subscriptions, EMIs, or payment history. Never guess or fabricate specific data.\n\n"
        "When a tool result has status 'empty', tell the user clearly that nothing was found. "
        "When a tool result has status 'error', relay the message plainly without guessing further. "
        "Only use the 'data' field when status is 'ok'.\n\n"
        f"Guidance:\n{context_text}"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question},
    ]

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        tools=tool_definitions,
        tool_choice="auto",
        temperature=0.3,
    )

    response_message = response.choices[0].message

    if response_message.tool_calls:
        messages.append(response_message)

        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            raw_args = tool_call.function.arguments
            try:
                function_args = json.loads(raw_args) if raw_args and raw_args.strip() else {}
            except json.JSONDecodeError:
                function_args = {}

            function_to_call = tool_function_map.get(function_name)

            if function_to_call is None:
                result = {"status": "error", "message": f"Unknown tool: {function_name}"}
            else:
                result = function_to_call(db, current_user, **function_args)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": json.dumps(result),
            })

        second_response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=tool_definitions,
            tool_choice="none",
            temperature=0.3,
        )
        return second_response.choices[0].message.content

    return response_message.content

if __name__ == "__main__":
    from app.database import SessionLocal
    from app.models import User
    from sqlalchemy import select
    from app.security import verify_password

    db = SessionLocal()

    email = input("Email: ").strip()
    password = input("Password: ").strip()

    user = db.execute(select(User).where(User.email == email)).scalar_one_or_none()

    if user is None or not verify_password(password, user.hashed_password):
        print("Invalid email or password.")
        db.close()
        exit()

    print(f"\nLogged in as {user.name}. Type 'exit' to quit.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() in ("exit", "quit"):
            break

        if not question:
            continue

        answer = answer_question(question, db, user)
        print(f"\nAssistant: {answer}\n")

    db.close()