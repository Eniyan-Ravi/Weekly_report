from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import InMemorySaver


class State(TypedDict):
    amount: int
    approved: str

def check_amount(state: State):
    print(f"Transaction amount: ₹{state['amount']}")
    decision = interrupt(
        "Do you approve this transaction? Enter yes or no."
    )
    print("Human decision:", decision)
    return {
        "approved": decision
    }


def process_transaction(state: State):
    if state["approved"].lower() == "yes":
        print("Transaction processed.")
    else:
        print("Transaction rejected.")

    return {}


graph = StateGraph(State)
graph.add_node("check_amount", check_amount)
graph.add_node("process", process_transaction)
graph.add_edge(START, "check_amount")
graph.add_edge("check_amount", "process")
graph.add_edge("process", END)

checkpointer = InMemorySaver()

app = graph.compile(
    checkpointer=checkpointer
)


config = {
    "configurable": {
        "thread_id": "transaction_001"
    }
}


result = app.invoke(
    {
        "amount": 5000,
        "approved": ""
    },
    config
)

print("Graph paused.")
print("Result:", result)


decision = input("Approve transaction? (yes/no): ")

result = app.invoke(
    Command(resume=decision),
    config
)

print("Final result:", result)