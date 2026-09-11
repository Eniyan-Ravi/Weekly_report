import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

review = """
The Samsung phone has an excellent camera, but the battery is disappointing.
I would not recommend it.
"""

prompt_unstructured = f"""
You are a customer review analyzer. Analyze this review and tell me
the sentiment, the product mentioned, and whether the customer
recommends it. Review: The Samsung phone has an excellent camera,
but the battery is disappointing. I would not recommend it.
"""

prompt_structured = f"""
ROLE:
You are a customer review analyzer.

TASK:
Analyze the customer review and extract:
1. Sentiment
2. Product
3. Recommendation

RULES:
- Sentiment must be Positive, Negative, or Mixed.
- Recommendation must be Yes or No.
- Do not add information that is not present in the review.

REVIEW:
The Samsung phone has an excellent camera, but the battery is disappointing.
I would not recommend it.

OUTPUT:
Provide the three extracted fields clearly.
"""

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "user",
            "content": prompt_structured #prompt_unstuctured for unstructure answer
        }
    ],
    temperature=0
)

print(response.choices[0].message.content)