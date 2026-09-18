"""
CLI chat loop.
Each message is a fresh call to run() — no conversation history is kept,
so every turn behaves exactly like running the script once from scratch.
Usage:
    python main.py
    (type your request, press Enter; type 'exit' to quit)
"""

from dotenv import load_dotenv

load_dotenv()

from agent.agent import run  # noqa: E402  (import after load_dotenv on purpose)


def print_result(result):
    if result.get("error"):
        print(f"[Agent] {result['error']}")
        return

    print(f"[Agent] Identified skill: {result['skill']}")
    print(f"[Agent] Workflow config: {result['workflow']}")

    if result["skill"] == "BLOG":
        print("\n[Retrieved knowledge]")
        for r in result["retrieved"]:
            print(f" - {r}")
        print("\n[Generated blog]\n")
        print(result["blog"])
    elif result["skill"] == "RESEARCH":
        print(f"[Agent] {result['note']}")


def main():
    print("Marketing Agent POC — type 'exit' to quit.\n")

    while True:
        query = input("You: ").strip()

        if not query:
            continue

        if query.lower() in ("exit", "quit"):
            print("Goodbye.")
            break

        result = run(query)  # fresh call every time — no memory of prior turns
        print()
        print_result(result)
        print()


if __name__ == "__main__":
    main()