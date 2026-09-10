import os
from dotenv import load_dotenv
from groq import Groq
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

user_input = input("Enter the query:")
response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[{"role": "user","content": user_input}]
)

print("Response:")
print(response.choices[0].message.content)
print("API input tokens:", response.usage.prompt_tokens)
print("\nToken Usage:")
print("Input tokens:", response.usage.prompt_tokens)
print("Output tokens:", response.usage.completion_tokens)
print("Total tokens:", response.usage.total_tokens)