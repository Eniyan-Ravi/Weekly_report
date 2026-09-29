from typing import Literal

from app.graph.state import State


def route_task(
    state: State,
) -> Literal["email", "blog", "research"]:
    """
    Route the workflow based on the task type
    determined by the Task Router.
    """

    task_type = state["task_type"]

    return task_type