
import uuid

from dotenv import load_dotenv
from langgraph.types import Command

from app.graph.graph import build_graph

load_dotenv()


def ask_tone(options: list[str]) -> str:
    print("\nSelect email tone:\n")
    for i, name in enumerate(options, 1):
        print(f"{i}. {name}")
    while True:
        raw = input("\nYour choice (number or name): ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1]
        for name in options:
            if raw.lower() == name.lower():
                return name
        print("Invalid choice, try again.")


def ask_approval(payload: dict) -> dict:
    print(f"\nVersion {payload['version']} of {payload['max_versions']}.")
    while True:
        answer = input("Approve this version? (yes/no): ").strip().lower()
        if answer in {"yes", "y"}:
            return {"approved": True}
        if answer in {"no", "n"}:
            break
        print("Please enter 'yes' or 'no'.")

    if not payload["can_retry"]:
        print("This was the last allowed version.")
        return {"approved": False}
    feedback = input("Optional feedback for the next version (Enter to skip): ").strip()
    return {"approved": False, "feedback": feedback}


def answer_interrupt(payload: dict):
    if payload["type"] == "tone_selection":
        return ask_tone(payload["options"])
    return ask_approval(payload)


def pending_interrupt(graph, config) -> dict | None:
    for task in graph.get_state(config).tasks:
        for item in task.interrupts:
            return item.value
    return None


def run_request(graph, user_request: str) -> dict:
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    graph.invoke(
        {"user_request": user_request, "email_retry_count": 0, "revision_count": 0},
        config,
    )
    while (payload := pending_interrupt(graph, config)) is not None:
        graph.invoke(Command(resume=answer_interrupt(payload)), config)
    return graph.get_state(config).values


def main() -> None:
    print("\nMulti-Agent System (type 'exit' to quit)")
    graph = build_graph()

    while True:
        user_request = input("\nEnter your request(exit or quit to close):\n").strip()
        if user_request.lower() in {"exit", "quit"}:
            break
        if not user_request:
            print("No request provided.")
            continue

        result = run_request(graph, user_request)

        print(f"\nWORKFLOW COMPLETED (task: {result.get('task_type')})")
        if result.get("approval_status") != "approved":
            print("Version limit reached without approval. Last version shown:")
        print(f"\n{result.get('final_output', 'No output generated.')}")


if __name__ == "__main__":
    main()
