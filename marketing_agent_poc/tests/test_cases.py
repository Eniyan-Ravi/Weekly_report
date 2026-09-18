"""
Mirrors the 4 test cases from the original spec.
Run: python -m tests.test_cases
(Test 4 temporarily edits config/workflow_router.md and restores it after.)
"""

from dotenv import load_dotenv
load_dotenv()

from agent.agent import run

ROUTER_PATH = "config/workflow_router.md"


def test_1_blog_aws_cost():
    result = run("Write a blog about AWS cost optimization for cloud architects.")
    assert result["skill"] == "BLOG"
    assert result["workflow"]["workflow_id"] == "WF-MKT-BLOG-001"
    print("Test 1 passed:", result["workflow"])


def test_2_research():
    result = run("Research the latest cloud cost optimization approaches.")
    assert result["skill"] == "RESEARCH"
    assert result["workflow"]["workflow_id"] == "WF-MKT-RESEARCH-001"
    print("Test 2 passed:", result["workflow"])


def test_3_blog_autoscaling():
    result = run("Write a blog about autoscaling.")
    assert result["skill"] == "BLOG"
    assert result["workflow"]["workflow_id"] == "WF-MKT-BLOG-001"
    assert any("autoscal" in r.lower() for r in result["retrieved"])
    print("Test 3 passed:", result["retrieved"])


def test_4_missing_config():
    with open(ROUTER_PATH) as f:
        original = f.read()

    edited = "\n\n".join(
        block for block in original.split("\n\n") if "SKILL: BLOG" not in block
    )
    with open(ROUTER_PATH, "w") as f:
        f.write(edited)

    try:
        result = run("Write a blog about autoscaling.")
        assert result["workflow"] is None
        assert "not found" in result["error"].lower()
        print("Test 4 passed:", result["error"])
    finally:
        with open(ROUTER_PATH, "w") as f:
            f.write(original)


if __name__ == "__main__":
    test_1_blog_aws_cost()
    test_2_research()
    test_3_blog_autoscaling()
    test_4_missing_config()