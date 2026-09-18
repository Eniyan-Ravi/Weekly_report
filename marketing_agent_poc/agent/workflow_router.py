"""
Parses config/workflow_router.md into {SKILL: {skill_id, workflow_id, automation_id}}.
This simulates a "central config" lookup — the agent must call get_workflow()
instead of guessing an ID. If a skill isn't in the file, we return None.
"""

ROUTER_PATH = "config/workflow_router.md"


def parse_router(path=ROUTER_PATH):
    with open(path, "r") as f:
        text = f.read()

    registry = {}

    # Each skill "block" is separated by a blank line
    blocks = text.strip().split("\n\n")

    for block in blocks:
        fields = {}
        for line in block.strip().splitlines():
            key, value = line.split(":", 1)   # split on first ":" only
            fields[key.strip()] = value.strip()

        registry[fields["SKILL"]] = {
            "skill_id": fields["SKILL_ID"],
            "workflow_id": fields["WORKFLOW_ID"],
            "automation_id": fields["AUTOMATION_ID"],
        }

    return registry


def get_workflow(skill, path=ROUTER_PATH):
    """Returns the workflow dict for a skill, or None if not registered."""
    return parse_router(path).get(skill)


if __name__ == "__main__":
    # Quick manual check: python -m agent.workflow_router
    for skill, info in parse_router().items():
        print(skill, "->", info)