import os
import json
from dotenv import load_dotenv
from pathlib import Path
from groq import Groq
from rag.tools.tool_definitions import tool_definitions, tool_function_map

RAG_ENV_PATH = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=RAG_ENV_PATH)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL_NAME = "openai/gpt-oss-120b"


def generate_answer(question: str, context_chunks: list[dict]) -> str:
    context_text = "\n\n".join(
        f"[Source: {chunk['source']}]\n{chunk['text']}"
        for chunk in context_chunks
    )

    system_prompt = (
        "You are a helpful assistant for a subscription and EMI tracking app. "
        "Use the provided context to answer the user's question as accurately as possible. "
        "If the context does not contain enough information to answer, say so clearly "
        "instead of guessing."
    )

    user_prompt = f"Context:\n{context_text}\n\nQuestion: {question}"

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content


def generate_answer_with_tools(question: str, db, current_user) -> str:
    system_prompt = (
        "You are a helpful assistant for a subscription and EMI tracking app. "
        "You have access to tools that fetch the user's real, live data — always use "
        "a tool when the user asks about their actual subscriptions, EMIs, or payment history. "
        "Never guess or fabricate specific data. "
        "When a tool result has status 'empty', tell the user clearly that nothing was found. "
        "When a tool result has status 'error', relay the message plainly without guessing further. "
        "Only use the 'data' field when status is 'ok'."
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
            function_args = json.loads(tool_call.function.arguments)

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
            temperature=0.3,
        )
        return second_response.choices[0].message.content

    return response_message.content