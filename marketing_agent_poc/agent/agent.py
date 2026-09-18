"""
Core orchestration:
  1. Identify skill (BLOG / RESEARCH) via LLM classification
  2. Look up workflow config via agent/workflow_router.py (never invent an ID)
  3. If BLOG -> retrieve top-3 knowledge chunks, generate using ONLY those facts
"""

import os
from groq import Groq

from agent.workflow_router import get_workflow
from rag.semantic_search import retrieve

client = Groq(api_key=os.environ["GROQ_API_KEY"])
LLM_MODEL = "openai/gpt-oss-20b"


def identify_skill(user_query):
    prompt = (
        "Classify the user's request into exactly one skill: BLOG or RESEARCH.\n"
        "Respond with only the skill name, nothing else.\n\n"
        f"User request: {user_query}"
    )
    resp = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return resp.choices[0].message.content.strip().upper()


def run_blog_workflow(user_query):
    retrieved = retrieve(user_query, top_k=3)

    context = "\n".join(f"- {c}" for c in retrieved)
    prompt = (
        "You are a marketing blog writer.\n"
        "Use ONLY the facts listed below. Do not invent facts that are not present here.\n\n"
        f"Retrieved knowledge:\n{context}\n\n"
        f"Task: {user_query}\n\n"
        "Write a short blog post (3-4 paragraphs) using only the above facts."
    )
    resp = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )
    return resp.choices[0].message.content, retrieved


def run(user_query):
    """Returns a result dict so both main.py and tests can consume it."""
    skill = identify_skill(user_query)

    workflow = get_workflow(skill)
    if not workflow:
        return {"skill": skill, "workflow": None, "error": "Workflow ID not found. Do not invent an ID."}

    if skill == "BLOG":
        blog, retrieved = run_blog_workflow(user_query)
        return {"skill": skill, "workflow": workflow, "blog": blog, "retrieved": retrieved}

    if skill == "RESEARCH":
        return {"skill": skill, "workflow": workflow, "note": "RESEARCH workflow not implemented in this POC."}

    return {"skill": skill, "workflow": workflow, "error": f"Unrecognized skill '{skill}'."}