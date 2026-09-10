import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

user_input = input("Enter the query: ")
temperature = float(input("Enter temperature (0-2): "))

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[{"role": "user","content": user_input}],
    temperature=temperature
)

print("\nResponse:")
print(response.choices[0].message.content)

print("\nToken Usage:")
print("Input tokens:", response.usage.prompt_tokens)
print("Output tokens:", response.usage.completion_tokens)