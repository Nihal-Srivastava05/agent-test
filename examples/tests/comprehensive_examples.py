"""
Comprehensive Test Examples for AgentTest

This file demonstrates all AgentTest evaluators with detailed examples
and real-world use cases.
"""

from agent_test import agent_test


# Sample agent function for testing
def mock_customer_support(query: str, urgency: str = "normal") -> dict:
    """Mock customer support agent for testing purposes."""
    if "billing" in query.lower():
        return {
            "response": "For billing inquiries, please contact our billing department at billing@company.com",
            "category": "billing",
            "action": "respond",
        }
    elif "angry" in query.lower() or "terrible" in query.lower():
        return {
            "response": "I understand your concern. Let me connect you with a specialist.",
            "category": "escalation",
            "action": "escalate",
        }
    else:
        return {
            "response": "Thank you for your inquiry. I'm here to help you with this issue.",
            "category": "general",
            "action": "respond",
        }


# =============================================================================
# STRING SIMILARITY EVALUATOR EXAMPLES
# =============================================================================


@agent_test(criteria=["similarity"])
def test_exact_greeting_response():
    """Test exact greeting response matching."""
    input_data = "Hello"
    expected = "Hello! How can I help you today?"
    actual = "Hello! How can I help you today?"

    return {"input": input_data, "expected": expected, "actual": actual}


@agent_test(criteria=["similarity"])
def test_similar_support_response():
    """Test similar response matching with tolerance."""
    input_data = "I need help with my account"
    expected = "I'll help you with your account issue"
    actual = "I can assist you with your account problem"

    return {"input": input_data, "expected": expected, "actual": actual}


# =============================================================================
# LLM-AS-JUDGE EVALUATOR EXAMPLES
# =============================================================================


@agent_test(criteria=["llm_judge"])
def test_customer_service_quality():
    """Test customer service response quality using LLM judge."""
    input_data = "I'm having trouble with my order and I'm frustrated"
    actual = mock_customer_support(input_data, urgency="high")

    return {
        "input": input_data,
        "actual": actual,
        "evaluation_criteria": {
            "empathy": "Response should show understanding and empathy for customer frustration",
            "professionalism": "Response should maintain professional tone despite customer frustration",
            "helpfulness": "Response should offer concrete help or next steps",
            "de_escalation": "Response should help calm the frustrated customer",
        },
    }


@agent_test(criteria=["llm_judge"])
def test_technical_explanation_quality():
    """Test quality of technical explanations."""
    input_data = "Explain machine learning in simple terms"
    actual = "Machine learning is when computers learn patterns from data to make predictions, like how Netflix recommends movies based on what you've watched before."

    return {
        "input": input_data,
        "actual": actual,
        "evaluation_criteria": {
            "clarity": "Explanation should be clear and easy to understand",
            "accuracy": "Technical information should be correct",
            "simplicity": "Should avoid jargon and use simple language",
            "relatability": "Should use familiar examples or analogies",
            "completeness": "Should cover the essential concept adequately",
        },
    }


# =============================================================================
# REGEX EVALUATOR EXAMPLES
# =============================================================================


@agent_test(criteria=["regex"])
def test_email_format_validation():
    """Test if response contains valid email format."""
    input_data = "What's your support email?"
    actual = "You can reach our support team at support@company.com"

    return {
        "input": input_data,
        "actual": actual,
        "pattern": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
    }


@agent_test(criteria=["regex"])
def test_phone_number_format():
    """Test if response contains properly formatted phone number."""
    input_data = "What's your phone number?"
    actual = "Call us at (555) 123-4567 during business hours"

    return {"input": input_data, "actual": actual, "pattern": r"\(\d{3}\)\s\d{3}-\d{4}"}


# =============================================================================
# CONTAINS EVALUATOR EXAMPLES
# =============================================================================


@agent_test(criteria=["contains"])
def test_security_information_presence():
    """Test if security response contains required security elements."""
    input_data = "How do you protect my personal data?"
    actual = "We protect your data using encryption, secure servers, and strict privacy policies."

    return {
        "input": input_data,
        "actual": actual,
        "contains": ["encryption", "secure", "privacy"],
    }


@agent_test(criteria=["contains"])
def test_refund_policy_elements():
    """Test if refund policy response contains all required elements."""
    input_data = "What's your refund policy?"
    actual = "We offer a 30-day money-back guarantee. Contact support to process your refund."

    return {
        "input": input_data,
        "actual": actual,
        "contains": ["30-day", "money-back", "guarantee", "support", "refund"],
    }


# =============================================================================
# METRIC EVALUATOR EXAMPLES
# =============================================================================


@agent_test(criteria=["metrics"])
def test_summary_quality_rouge():
    """Test summary quality using ROUGE metrics."""
    input_data = "Summarize the benefits of cloud computing"
    reference = "Cloud computing offers scalability, cost savings, accessibility, and improved collaboration."
    actual = "Cloud computing provides scalable resources, reduces costs, enables remote access, and enhances collaboration."

    return {
        "input": input_data,
        "actual": actual,
        "reference": reference,
        "metrics": {
            "rouge": {"min_score": 0.4, "variants": ["rouge-1", "rouge-2", "rouge-l"]}
        },
    }


# =============================================================================
# COMBINATION EVALUATOR EXAMPLES
# =============================================================================


@agent_test(criteria=["similarity", "contains", "regex"])
def test_structured_response_comprehensive():
    """Test structured response using multiple evaluators."""
    input_data = "Generate an order confirmation"
    expected = (
        "Order #ORD-2024-001 confirmed. Total: $99.99. Email sent to customer@email.com"
    )
    actual = "Order #ORD-2024-001 has been confirmed. Your total is $99.99. Confirmation sent to customer@email.com"

    return {
        "input": input_data,
        "expected": expected,
        "actual": actual,
        "contains": ["Order", "confirmed", "total", "email"],
        "patterns": [
            r"Order #ORD-\d{4}-\d{3}",
            r"\$\d+\.\d{2}",
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        ],
    }


# =============================================================================
# EDGE CASE EXAMPLES
# =============================================================================


@agent_test(criteria=["llm_judge"])
def test_empty_input_handling():
    """Test how agent handles empty input."""
    input_data = ""
    actual = mock_customer_support(input_data)

    return {
        "input": input_data,
        "actual": actual,
        "evaluation_criteria": {
            "graceful_handling": "Should handle empty input gracefully",
            "user_guidance": "Should guide user to provide input",
            "professional_tone": "Should maintain professional tone",
        },
    }


if __name__ == "__main__":
    print("AgentTest Comprehensive Examples")
    print("=" * 40)
    print("This file contains examples of all AgentTest evaluators:")
    print("- String Similarity")
    print("- LLM-as-Judge")
    print("- Regex")
    print("- Contains")
    print("- Metrics")
    print("- Combination Tests")
    print("- Edge Cases")
    print("\nTo run these tests: agenttest run")
