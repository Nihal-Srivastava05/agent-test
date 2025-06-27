"""
Basic usage example for AgentTest.

This demonstrates how to create and test a simple AI agent.
"""

from agent_test import agent_test


def simple_echo_agent(input_text: str) -> str:
    """A simple agent that echoes the input with a prefix."""
    return f"Agent response: {input_text}"


def smart_agent(query: str) -> str:
    """A smarter agent that provides different responses based on input."""
    query_lower = query.lower()

    if "hello" in query_lower:
        return "Hello! How can I help you today?"
    elif "weather" in query_lower:
        return "I don't have access to current weather data, but you can check a weather app!"
    elif "time" in query_lower:
        return "I don't have access to the current time, but you can check your device clock."
    elif len(query.strip()) == 0:
        return "Please provide a question or statement."
    else:
        return f"I received your message: '{query}'. How can I assist you?"


# Basic test with exact matching
@agent_test(criteria=["similarity"])
def test_echo_agent_basic():
    """Test the echo agent with basic input."""
    input_text = "Hello, world!"
    expected = "Agent response: Hello, world!"

    actual = simple_echo_agent(input_text)

    return {"input": input_text, "expected": expected, "actual": actual}


# Test with multiple test cases
@agent_test(criteria=["similarity"])
def test_echo_agent_multiple():
    """Test the echo agent with multiple inputs."""
    test_cases = [
        {"input": "Test 1", "expected": "Agent response: Test 1"},
        {"input": "Another test", "expected": "Agent response: Another test"},
        {"input": "", "expected": "Agent response: "},
    ]

    results = []
    for case in test_cases:
        actual = simple_echo_agent(case["input"])
        results.append(
            {"input": case["input"], "expected": case["expected"], "actual": actual}
        )

    return results


# Test with LLM judge evaluation (requires API key)
@agent_test(criteria=["llm_judge"], tags=["smart_agent"])
def test_smart_agent_hello():
    """Test smart agent's greeting functionality."""
    input_text = "Hello there!"
    actual = smart_agent(input_text)

    return {
        "input": input_text,
        "actual": actual,
        "evaluation_criteria": {
            "friendliness": "Response should be friendly and welcoming",
            "relevance": "Response should be relevant to the greeting",
        },
    }


# Test with contains evaluator
@agent_test(criteria=["contains"])
def test_smart_agent_weather():
    """Test smart agent's weather response."""
    input_text = "What's the weather like?"
    actual = smart_agent(input_text)

    return {
        "input": input_text,
        "actual": actual,
        "contains": ["weather", "app"],  # Should contain these words
    }


# Edge case testing
@agent_test(criteria=["similarity"], tags=["edge_case"])
def test_empty_input_handling():
    """Test how agents handle empty input."""
    actual_echo = simple_echo_agent("")
    actual_smart = smart_agent("")

    return [
        {"input": "", "actual": actual_echo, "expected": "Agent response: "},
        {
            "input": "",
            "actual": actual_smart,
            "expected": "Please provide a question or statement.",
        },
    ]


# Regex pattern testing
@agent_test(criteria=["regex"])
def test_response_format():
    """Test that echo agent responses follow expected format."""
    input_text = "Format test"
    actual = simple_echo_agent(input_text)

    return {"input": input_text, "actual": actual, "pattern": r"Agent response: .+"}


# Performance testing
@agent_test(criteria=["similarity"], tags=["performance"])
def test_long_input():
    """Test agent with long input."""
    long_input = "This is a very long input string. " * 100
    expected = f"Agent response: {long_input}"

    actual = simple_echo_agent(long_input)

    return {"input": long_input, "expected": expected, "actual": actual}


if __name__ == "__main__":
    print("AgentTest Example - Basic Usage")
    print("=" * 40)

    # You can run individual tests directly
    print("Running echo agent test...")
    result = test_echo_agent_basic()
    print(f"Result: {result}")

    print("\nRunning smart agent test...")
    result = test_smart_agent_hello()
    print(f"Result: {result}")

    print("\nTo run all tests, use: agenttest run")
