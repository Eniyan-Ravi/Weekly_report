from pathlib import Path

from langchain_core.prompts import ChatPromptTemplate
from langgraph.types import interrupt
from langchain_text_splitters import MarkdownHeaderTextSplitter


from app.agents.blog_agent import extract_blog_style, generate_blog
from app.agents.email_agent import generate_email
from app.agents.research_agent import research_topic
from app.graph.routing import MAX_VERSIONS, get_revision_count
from app.graph.state import State
from app.models.llm import get_llm
from app.schemas.schemas import TaskRoute

TONE_FILE = Path(__file__).resolve().parents[2] / "config" / "email_tones.md"

TASK_ROUTER_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
                        """You are a task router. Classify the user's request as exactly one of:
- email: the user wants an email/mail/message/letter written to someone
  (e.g. leave request, follow-up, complaint, thank-you note).
- blog: the user wants a blog post or article written.
- research: the user wants information researched, explained or summarised,
  with no blog/article requested.

Judge by intent, not keywords. Examples:
"Write me a mail for leave to my manager" -> email
"Draft a note to my landlord about the broken heater" -> email
"Write a blog about remote work" -> blog
"What are the causes of inflation?" -> research

Call the provided tool with the chosen task type.""",
        ),
        ("human", "{user_request}"),
    ]
)


#Task Router
def classify_task(user_request: str):
    llm = get_llm(temperature=0).with_structured_output(TaskRoute).with_retry(stop_after_attempt=3)
    return (TASK_ROUTER_PROMPT | llm).invoke({"user_request": user_request}).task


def task_router(state: State):
    return {"task_type": classify_task(state["user_request"])}


#Email
def load_email_tones() -> dict[str, str]:
    """Parse config/email_tones.md into {tone name: rules text}."""
    splitter = MarkdownHeaderTextSplitter(headers_to_split_on=[("##", "tone")])
    docs = splitter.split_text(TONE_FILE.read_text(encoding="utf-8"))
    return {
        doc.metadata["tone"]: doc.page_content.strip()
        for doc in docs
        if "tone" in doc.metadata
    }

def select_email_tone(state: State):
    tones = load_email_tones()
    choice = interrupt({"type": "tone_selection", "options": list(tones)})

    matches = {name.lower(): name for name in tones}
    key = str(choice).strip().lower()
    if key not in matches:
        raise ValueError(f"Unknown tone '{choice}'. Available: {list(tones)}")
    tone = matches[key]
    return {"email_tone": tone, "email_tone_rules": tones[tone]}


def email_node(state: State):
    retry = state.get("email_retry_count", 0)
    email = generate_email(
        user_request=state["user_request"],
        tone=state["email_tone"],
        tone_rules=state["email_tone_rules"],
        retry_count=retry,
        previous_email=state.get("email_output") if retry else None,
        feedback=state.get("review_feedback") if retry else None,
    )
    return {"email_output": email, "final_output": email}


#Research
def research_node(state: State):
    revising = state.get("task_type") == "research" and state.get("revision_count", 0) > 0
    research = research_topic(
        user_request=state["user_request"],
        previous_output=state.get("research_output") if revising else None,
        feedback=state.get("review_feedback") if revising else None,
    )
    update = {"research_output": research}
    if state["task_type"] == "research":
        update["final_output"] = research
    return update


#Blog
def blog_node(state: State):
    style = state.get("blog_style") or extract_blog_style(state["user_request"])
    revising = state.get("revision_count", 0) > 0
    blog = generate_blog(
        user_request=state["user_request"],
        research_output=state["research_output"],
        blog_style=style,
        previous_blog=state.get("blog_output") if revising else None,
        feedback=state.get("review_feedback") if revising else None,
    )
    return {"blog_style": style, "blog_output": blog, "final_output": blog}


#approval
def final_review(state: State):
    bar = " "
    print(f"\n{bar}\nFINAL REVIEW\n{bar}\n")
    print(state["final_output"])
    print(f"\n{bar}")
    return {}


def human_approval(state: State):
    versions_used = get_revision_count(state) + 1
    decision = interrupt(
        {
            "type": "approval",
            "version": versions_used,
            "max_versions": MAX_VERSIONS,
            "can_retry": versions_used < MAX_VERSIONS,
        }
    )
    approved = bool(decision.get("approved"))
    return {
        "approval_status": "approved" if approved else "rejected",
        "review_feedback": "" if approved else decision.get("feedback", ""),
    }


def revision_node(state: State):
    key = "email_retry_count" if state["task_type"] == "email" else "revision_count"
    return {key: state.get(key, 0) + 1}
