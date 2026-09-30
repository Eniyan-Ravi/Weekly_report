from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from app.graph.routing import (
    route_after_approval,
    route_after_research,
    route_after_revision,
    route_task,
)
from app.graph.state import State
from app.graph.workflow import (
    blog_node,
    email_node,
    final_review,
    human_approval,
    research_node,
    revision_node,
    select_email_tone,
    task_router,
)


def build_graph():
    graph = StateGraph(State)

    graph.add_node("task_router", task_router)
    graph.add_node("select_email_tone", select_email_tone)
    graph.add_node("email", email_node)
    graph.add_node("research", research_node)
    graph.add_node("blog", blog_node)
    graph.add_node("final_review", final_review)
    graph.add_node("human_approval", human_approval)
    graph.add_node("revision", revision_node)

    graph.add_edge(START, "task_router")
    graph.add_conditional_edges(
        "task_router",
        route_task,
        {"email": "select_email_tone", "blog": "research", "research": "research"},
    )

    graph.add_edge("select_email_tone", "email")
    graph.add_edge("email", "final_review")

    graph.add_conditional_edges(
        "research",
        route_after_research,
        {"blog": "blog", "final_review": "final_review"},
    )
    graph.add_edge("blog", "final_review")

    graph.add_edge("final_review", "human_approval")
    graph.add_conditional_edges(
        "human_approval",
        route_after_approval,
        {"approved": END, "revision": "revision"},
    )
    graph.add_conditional_edges(
        "revision",
        route_after_revision,
        {
            "email": "email",
            "blog": "blog",
            "research": "research",
            "limit_reached": END,
        },
    )

    return graph.compile(checkpointer=MemorySaver())
