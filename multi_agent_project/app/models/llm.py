"""Centralized LangChain LLM configuration."""

import os

from dotenv import load_dotenv
from langchain_core.language_models.chat_models import BaseChatModel

load_dotenv()

DEFAULT_MODEL = "openai/gpt-oss-20b"




def get_llm(temperature: float = 0.7):
    api_key = os.getenv("GROQ_API_KEY", "").strip()

    from langchain_groq import ChatGroq

    return ChatGroq(
        model=os.getenv("GROQ_MODEL", DEFAULT_MODEL),
        api_key=api_key,
        temperature=temperature,
    )
