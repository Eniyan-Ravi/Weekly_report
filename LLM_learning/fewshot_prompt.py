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
        Classify customer reviews as Positive, Negative, or Neutral.
        """
    },
    {
        "role": "user",
        "content": """
        Review: The product is amazing and works perfectly.
        Classification: Positive

        Review: The product broke after two days and the service was terrible.
        Classification: Negative

        Review: The package arrived this morning.
        Classification: Neutral

        Review: The delivery was incredibly fast and the product is in good condition.
        Classification:
        """
    }
],
    temperature=0
)

print(response.choices[0].message.content)