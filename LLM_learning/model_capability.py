import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

user_input = """
Write a poem about the ocean in 5 to 10 lines.

Strict constraints:
- Do not use the letter "a" anywhere in the response.
- Write between 5 and 10 lines.
- The poem should be meaningful and coherent.
"""

models = [
    "openai/gpt-oss-20b",
    "openai/gpt-oss-120b",
    "qwen/qwen3.6-27b"
]

for model in models:

    print(" ")
    print(f"MODEL: {model}")
    print(" ")

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user","content": user_input}]
    )

    result = response.choices[0].message.content

    print(result)
