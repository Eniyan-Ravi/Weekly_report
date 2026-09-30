from app.graph.state import State

# max number of generated versions
MAX_VERSIONS = 3


def get_revision_count(state: State) -> int:
    key = "email_retry_count" if state.get("task_type") == "email" else "revision_count"
    return state.get(key, 0)


def route_task(state: State):
    return state["task_type"]


def route_after_research(state: State):
    return "blog" if state["task_type"] == "blog" else "final_review"


def route_after_approval(state: State):
    return "approved" if state.get("approval_status") == "approved" else "revision"


def route_after_revision(state: State,):
    if get_revision_count(state) >= MAX_VERSIONS:
        return "limit_reached"
    return state["task_type"]
