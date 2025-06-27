"""
Example AgentTest test file.

This demonstrates basic testing patterns with the @agent_test decorator.
"""

from agent_test import agent_test


def simple_agent(input_text: str) -> str:
    """A simple agent that echoes the input with a prefix."""
    return f"Agent response: {input_text}"


@agent_test(criteria=["similarity", "llm_judge"])
def test_simple_agent():
    """Test the simple agent with basic input."""
    input_text = "Hello, world!"
    expected = "Agent response: Hello, world!"

    actual = simple_agent(input_text)

    # AgentTest will automatically evaluate using configured criteria
    return {"input": input_text, "expected": expected, "actual": actual}


@agent_test(criteria=["similarity"])
def test_agent_with_different_inputs():
    """Test agent with various inputs."""
    test_cases = [
        {"input": "What is AI?", "expected": "Agent response: What is AI?"},
        {"input": "How are you?", "expected": "Agent response: How are you?"},
    ]

    results = []
    for case in test_cases:
        actual = simple_agent(case["input"])
        results.append(
            {"input": case["input"], "expected": case["expected"], "actual": actual}
        )

    return results


if __name__ == "__main__":
    # You can run tests directly or use: agenttest run
    print("Example test - run with: agenttest run")
