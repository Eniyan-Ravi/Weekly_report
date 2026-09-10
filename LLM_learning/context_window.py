import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

messages = []

while True:

    user_input = input("\nEnter your message (type 'exit' to stop): ")

    if user_input.lower() == "exit":
        break

    messages.append({"role": "user","content": user_input})
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages
    )

    assistant_message = response.choices[0].message.content
    messages.append({"role": "assistant","content": assistant_message})

    print("\nResponse:")
    print(assistant_message)
    print("\nToken usage:")
    print("Input tokens:", response.usage.prompt_tokens)
    print("Output tokens:", response.usage.completion_tokens)
    print("Total tokens:", response.usage.total_tokens)