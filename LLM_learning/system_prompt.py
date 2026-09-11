import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "system",
            "content": """
You are a strict Python interviewer.
Give concise interview-style answers.
Do not provide code unless specifically requested.
"""
#"content": "You are a Python programming tutor. Give clear and practical answers."
#base on changing this and the above system prompt i got diff o/p 
},

        {
            "role": "user",
            "content": "What is a Python dictionary?"
        }
    ],
    temperature=0
)

print(response.choices[0].message.content)