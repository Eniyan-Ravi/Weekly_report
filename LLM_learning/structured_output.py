import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

review = """
The Samsung phone has an excellent camera, but the battery is disappointing.
I would not recommend it.
"""

schema = {
    "type": "object",
    "properties": {
        "sentiment": {
            "type": "string",
            "enum": ["Positive", "Negative", "Mixed", "Neutral"]
        },
        "product": {
            "type": "string"
        },
        "recommendation": {
            "type": "string",
            "enum": ["Yes", "No"]
        }
    },
    "required": [
        "sentiment",
        "product",
        "recommendation"
    ],
    "additionalProperties": False
}

prompt = f"""
Analyze the customer review below.

Review:
{review}

Return the result as JSON.

The JSON must follow this schema:

{schema}

Do not include explanations.
Do not include markdown.
Return JSON only.
"""

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0
)

print(response.choices[0].message.content)