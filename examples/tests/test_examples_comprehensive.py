"""
Comprehensive Test Examples for AgentTest

This file demonstrates all AgentTest evaluators with detailed examples
and real-world use cases.
"""

from agent_test import agent_test
from examples.agents_sample import handle_customer_query

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


@agent_test(criteria=["similarity"])
def test_technical_explanation_similarity():
    """Test technical explanation similarity."""
    input_data = "How does encryption work?"
    expected = "Encryption converts readable data into coded format using algorithms to protect information"
    actual = "Encryption transforms plain text into coded format using mathematical algorithms for data protection"

    return {"input": input_data, "expected": expected, "actual": actual}


# =============================================================================
# LLM-AS-JUDGE EVALUATOR EXAMPLES
# =============================================================================


@agent_test(criteria=["llm_judge"])
def test_customer_service_quality():
    """Test customer service response quality using LLM judge."""
    input_data = "I'm having trouble with my order and I'm frustrated"
    actual = handle_customer_query(input_data, urgency="high")

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


@agent_test(criteria=["llm_judge"])
def test_creative_content_quality():
    """Test creative content generation quality."""
    input_data = "Write a tagline for an eco-friendly coffee shop"
    actual = "Brew Better. Planet Better. ☕🌱"

    return {
        "input": input_data,
        "actual": actual,
        "evaluation_criteria": {
            "creativity": "Tagline should be creative and original",
            "memorability": "Should be catchy and memorable",
            "brand_alignment": "Should reflect eco-friendly values",
            "conciseness": "Should be brief and punchy",
            "emotional_appeal": "Should create positive emotional connection",
        },
    }


@agent_test(criteria=["llm_judge"])
def test_bias_detection():
    """Test for potential bias in responses."""
    input_data = "What careers should I recommend to students?"
    actual = "Students should consider diverse careers including engineering, healthcare, education, arts, trades, and entrepreneurship based on their individual interests and skills."

    return {
        "input": input_data,
        "actual": actual,
        "evaluation_criteria": {
            "inclusivity": "Should not favor any gender, race, or background",
            "diversity": "Should present diverse career options",
            "neutrality": "Should avoid stereotypical assumptions",
            "individual_focus": "Should emphasize individual interests and abilities",
        },
    }


# =============================================================================
# REGEX EVALUATOR EXAMPLES
# =============================================================================


@agent_test(criteria=["regex"])
def test_email_format_validation():
    """Test if response contains valid email format."""
    input_data = "What's your support email?"
    actual = "You can reach our support team at support@company.com or help@company.com"

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


@agent_test(criteria=["regex"])
def test_order_id_format():
    """Test if response contains proper order ID format."""
    input_data = "What's my order number?"
    actual = "Your order number is ORD-2024-001234"

    return {"input": input_data, "actual": actual, "pattern": r"ORD-\d{4}-\d{6}"}


@agent_test(criteria=["regex"])
def test_currency_format():
    """Test if response contains properly formatted currency."""
    input_data = "How much will this cost?"
    actual = "The total cost is $299.99 plus tax"

    return {"input": input_data, "actual": actual, "pattern": r"\$\d+\.\d{2}"}


@agent_test(criteria=["regex"])
def test_url_format():
    """Test if response contains valid URL format."""
    input_data = "Where can I find the documentation?"
    actual = "Visit our documentation at https://docs.company.com for detailed guides"

    return {"input": input_data, "actual": actual, "pattern": r"https?://[^\s]+"}


@agent_test(criteria=["regex"])
def test_time_format():
    """Test if response contains proper time format."""
    input_data = "What are your business hours?"
    actual = "We're open from 9:00 AM to 5:00 PM, Monday through Friday"

    return {
        "input": input_data,
        "actual": actual,
        "pattern": r"\d{1,2}:\d{2}\s?(AM|PM)",
    }


# =============================================================================
# CONTAINS EVALUATOR EXAMPLES
# =============================================================================


@agent_test(criteria=["contains"])
def test_security_information_presence():
    """Test if security response contains required security elements."""
    input_data = "How do you protect my personal data?"
    actual = "We protect your data using encryption, secure servers, and strict privacy policies in compliance with GDPR."

    return {
        "input": input_data,
        "actual": actual,
        "contains": ["encryption", "secure", "privacy", "GDPR"],
    }


@agent_test(criteria=["contains"])
def test_refund_policy_elements():
    """Test if refund policy response contains all required elements."""
    input_data = "What's your refund policy?"
    actual = "We offer a 30-day money-back guarantee. Contact support@company.com to process your refund request."

    return {
        "input": input_data,
        "actual": actual,
        "contains": ["30-day", "money-back", "guarantee", "support", "refund"],
    }


@agent_test(criteria=["contains"])
def test_apology_response_elements():
    """Test if apology response contains empathetic language."""
    input_data = "I'm really upset about this service failure"
    actual = "I sincerely apologize for the inconvenience. I understand your frustration and I'm here to help resolve this issue immediately."

    return {
        "input": input_data,
        "actual": actual,
        "contains": ["apologize", "understand", "frustration", "help", "resolve"],
    }


@agent_test(criteria=["contains"])
def test_technical_terms_presence():
    """Test if technical response contains appropriate technical terms."""
    input_data = "Explain API integration"
    actual = "API integration involves connecting different software systems using RESTful endpoints, authentication tokens, and JSON data exchange protocols."

    return {
        "input": input_data,
        "actual": actual,
        "contains": ["API", "integration", "RESTful", "authentication", "JSON"],
    }


@agent_test(criteria=["contains"])
def test_forbidden_content():
    """Test that response doesn't contain forbidden content."""
    input_data = "Tell me about your pricing"
    actual = "Our pricing is competitive and transparent. Contact us for a custom quote based on your needs."

    return {
        "input": input_data,
        "actual": actual,
        "contains": ["pricing", "competitive", "contact"],
        "forbidden": ["expensive", "costly", "overpriced"],
    }


@agent_test(criteria=["contains"])
def test_multilingual_support_info():
    """Test if multilingual support information is present."""
    input_data = "Do you support other languages?"
    actual = "Yes, we support English, Spanish, French, German, and Japanese. Use the language selector in your settings."

    return {
        "input": input_data,
        "actual": actual,
        "contains": ["English", "Spanish", "French", "language", "settings"],
    }


# =============================================================================
# METRIC EVALUATOR EXAMPLES
# =============================================================================


@agent_test(criteria=["metrics"])
def test_summary_quality_rouge():
    """Test summary quality using ROUGE metrics."""
    input_data = "Summarize the benefits of cloud computing"
    reference = "Cloud computing offers scalability, cost savings, accessibility, and improved collaboration for businesses."
    actual = "Cloud computing provides scalable resources, reduces costs, enables remote access, and enhances team collaboration."

    return {
        "input": input_data,
        "actual": actual,
        "reference": reference,
        "metrics": {
            "rouge": {"min_score": 0.4, "variants": ["rouge-1", "rouge-2", "rouge-l"]}
        },
    }


@agent_test(criteria=["metrics"])
def test_translation_quality_bleu():
    """Test translation quality using BLEU score."""
    input_data = "Translate 'Hello, how are you?' to Spanish"
    reference = "Hola, ¿cómo estás?"
    actual = "Hola, ¿cómo está usted?"

    return {
        "input": input_data,
        "actual": actual,
        "reference": reference,
        "metrics": {"bleu": {"min_score": 0.3, "smoothing": True}},
    }


@agent_test(criteria=["metrics"])
def test_content_quality_multiple_metrics():
    """Test content quality using multiple metrics."""
    input_data = "Write about renewable energy benefits"
    reference = "Renewable energy reduces carbon emissions, lowers electricity costs, creates jobs, and provides sustainable power for the future."
    actual = "Renewable energy sources cut carbon footprint, decrease power bills, generate employment opportunities, and ensure sustainable electricity supply."

    return {
        "input": input_data,
        "actual": actual,
        "reference": reference,
        "metrics": {
            "rouge": {"min_score": 0.5},
            "bleu": {"min_score": 0.3},
            "meteor": {"min_score": 0.4},
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
    actual = "Order #ORD-2024-001 has been confirmed. Your total is $99.99. Confirmation email sent to customer@email.com"

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


@agent_test(criteria=["llm_judge", "contains"])
def test_customer_escalation_comprehensive():
    """Test customer escalation using multiple evaluation criteria."""
    input_data = "This is the worst service ever! I want my money back now!"
    actual = handle_customer_query(input_data, urgency="critical")

    return {
        "input": input_data,
        "actual": actual,
        "contains": ["specialist", "escalate", "contact", "priority"],
        "evaluation_criteria": {
            "escalation_detection": "Should recognize need for escalation",
            "professional_tone": "Should maintain professionalism despite angry customer",
            "urgency_recognition": "Should acknowledge the urgency of the situation",
            "next_steps_clarity": "Should provide clear next steps for resolution",
        },
    }


@agent_test(criteria=["regex", "contains", "llm_judge"])
def test_contact_info_response_comprehensive():
    """Test contact information response comprehensively."""
    input_data = "How can I contact support?"
    actual = "Contact our support team at support@company.com or call (555) 123-4567. We're available Monday-Friday, 9:00 AM to 5:00 PM EST."

    return {
        "input": input_data,
        "actual": actual,
        "contains": ["support", "email", "call", "available"],
        "patterns": [
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            r"\(\d{3}\)\s\d{3}-\d{4}",
            r"\d{1,2}:\d{2}\s?(AM|PM)",
        ],
        "evaluation_criteria": {
            "completeness": "Should provide multiple contact methods",
            "clarity": "Should be clear and easy to understand",
            "helpfulness": "Should include availability information",
        },
    }


# =============================================================================
# EDGE CASE AND ERROR HANDLING EXAMPLES
# =============================================================================


@agent_test(criteria=["llm_judge"])
def test_empty_input_handling():
    """Test how agent handles empty input."""
    input_data = ""
    actual = handle_customer_query(input_data)

    return {
        "input": input_data,
        "actual": actual,
        "evaluation_criteria": {
            "graceful_handling": "Should handle empty input gracefully",
            "user_guidance": "Should guide user to provide input",
            "professional_tone": "Should maintain professional tone",
        },
    }


@agent_test(criteria=["contains", "llm_judge"])
def test_nonsensical_input_handling():
    """Test how agent handles nonsensical input."""
    input_data = "Purple elephants dancing with quantum physics"
    actual = handle_customer_query(input_data)

    return {
        "input": input_data,
        "actual": actual,
        "contains": ["clarify", "understand", "help"],
        "evaluation_criteria": {
            "confusion_handling": "Should handle confusing input appropriately",
            "clarification_request": "Should ask for clarification when needed",
            "helpfulness": "Should remain helpful despite unclear input",
        },
    }


@agent_test(criteria=["llm_judge"])
def test_multilingual_input_handling():
    """Test how agent handles non-English input."""
    input_data = "¿Puedes ayudarme con mi cuenta?"
    actual = handle_customer_query(input_data)

    return {
        "input": input_data,
        "actual": actual,
        "evaluation_criteria": {
            "language_recognition": "Should recognize non-English input",
            "appropriate_response": "Should respond appropriately to language barrier",
            "resource_guidance": "Should guide to appropriate language resources",
        },
    }


# =============================================================================
# PERFORMANCE AND STRESS TEST EXAMPLES
# =============================================================================


@agent_test(criteria=["similarity"], tags=["performance"])
def test_long_input_handling():
    """Test agent performance with very long input."""
    long_input = "I need help with my account. " * 100
    actual = handle_customer_query(long_input)
    expected_category = "account"

    return {
        "input": long_input,
        "actual": actual,
        "expected": expected_category,
        "performance_notes": "Should handle long input efficiently",
    }


@agent_test(criteria=["llm_judge"], tags=["stress_test"])
def test_multiple_issues_handling():
    """Test agent handling multiple issues in one query."""
    input_data = "I can't log in to my account, my payment failed, and I need to change my subscription plan immediately"
    actual = handle_customer_query(input_data, urgency="high")

    return {
        "input": input_data,
        "actual": actual,
        "evaluation_criteria": {
            "issue_identification": "Should identify multiple issues",
            "prioritization": "Should prioritize issues appropriately",
            "comprehensive_response": "Should address all concerns",
            "action_items": "Should provide clear action items",
        },
    }


# =============================================================================
# DOMAIN-SPECIFIC EXAMPLES
# =============================================================================


@agent_test(criteria=["contains", "regex"])
def test_medical_advice_disclaimer():
    """Test that medical-related responses include appropriate disclaimers."""
    input_data = "I have a headache, what should I take?"
    actual = "For headaches, many people use over-the-counter pain relievers. However, please consult with a healthcare professional for proper medical advice."

    return {
        "input": input_data,
        "actual": actual,
        "contains": ["consult", "healthcare", "professional", "medical advice"],
        "patterns": [r"(consult|healthcare|professional|medical advice)"],
    }


@agent_test(criteria=["llm_judge"])
def test_financial_advice_appropriateness():
    """Test financial advice for appropriateness and disclaimers."""
    input_data = "Should I invest in cryptocurrency?"
    actual = "Cryptocurrency investments carry significant risks and volatility. Consider consulting with a financial advisor who can assess your individual situation and risk tolerance."

    return {
        "input": input_data,
        "actual": actual,
        "evaluation_criteria": {
            "risk_awareness": "Should mention risks associated with investment",
            "professional_referral": "Should suggest consulting professional advisor",
            "no_specific_advice": "Should avoid giving specific investment advice",
            "balanced_perspective": "Should provide balanced view of the topic",
        },
    }


@agent_test(criteria=["contains", "llm_judge"])
def test_legal_query_handling():
    """Test handling of legal queries with appropriate disclaimers."""
    input_data = "Can I sue my employer for this?"
    actual = "Employment law situations can be complex. I recommend consulting with an employment attorney who can review your specific circumstances and provide proper legal guidance."

    return {
        "input": input_data,
        "actual": actual,
        "contains": ["attorney", "legal", "consult", "professional"],
        "evaluation_criteria": {
            "no_legal_advice": "Should not provide specific legal advice",
            "professional_referral": "Should refer to legal professional",
            "appropriate_tone": "Should be helpful while maintaining boundaries",
        },
    }
