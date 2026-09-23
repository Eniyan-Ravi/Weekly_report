import os

from langchain_groq import ChatGroq

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)


prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an AI teacher. Explain concepts clearly."
    ),
    (
        "human",
        "Explain {topic} for a beginner."
    )
])


parser = StrOutputParser()


chain = prompt | llm | parser


result = chain.invoke({
    "topic": "vector databases"
})


print(result)