"""
Sample AI Agents for AgentTest Examples

This file contains sample implementations of different types of AI agents
that can be used to demonstrate AgentTest features.
"""

from dataclasses import dataclass
from typing import Dict, Optional

try:
    import google.generativeai as genai

    HAS_GOOGLE_GENAI = True
except ImportError:
    genai = None
    HAS_GOOGLE_GENAI = False


# Customer Support Agent
@dataclass
class CustomerQuery:
    """Customer query data structure."""

    query: str
    customer_type: str = "regular"  # regular, premium, enterprise
    urgency: str = "normal"  # low, normal, high, critical
    category: Optional[str] = None


class CustomerSupportAgent:
    """AI-powered customer support agent."""

    def __init__(self, api_key: str):
        """Initialize the customer support agent."""
        if not HAS_GOOGLE_GENAI:
            raise ImportError(
                "google-generativeai is required for GoogleAI agent. "
                "Install with: pip install 'agenttest[google]'"
            )
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

        # Knowledge base for common issues
        self.knowledge_base = {
            "billing": "For billing inquiries, please contact our billing department at billing@company.com",
            "technical": "For technical issues, please try restarting the application first",
            "account": "For account issues, please verify your email and password",
            "product": "For product information, please visit our documentation at docs.company.com",
        }

    def classify_query(self, query: str) -> str:
        """Classify the customer query into categories."""
        query_lower = query.lower()

        if any(word in query_lower for word in ["bill", "payment", "charge", "refund"]):
            return "billing"
        elif any(
            word in query_lower for word in ["bug", "error", "crash", "not working"]
        ):
            return "technical"
        elif any(
            word in query_lower for word in ["account", "login", "password", "access"]
        ):
            return "account"
        elif any(
            word in query_lower for word in ["feature", "how to", "documentation"]
        ):
            return "product"
        else:
            return "general"

    def should_escalate(self, query: CustomerQuery) -> bool:
        """Determine if query should be escalated to human agent."""
        escalation_keywords = [
            "frustrated",
            "angry",
            "cancel",
            "lawsuit",
            "lawyer",
            "terrible",
            "worst",
            "hate",
            "refund",
            "money back",
        ]

        if query.urgency == "critical":
            return True

        if query.customer_type == "enterprise" and query.urgency == "high":
            return True

        if any(keyword in query.query.lower() for keyword in escalation_keywords):
            return True

        return False

    def generate_response(self, query: CustomerQuery) -> Dict[str, str]:
        """Generate a response to customer query."""
        category = self.classify_query(query.query)

        # Check if escalation is needed
        if self.should_escalate(query):
            return {
                "response": "I understand your concern. Let me connect you with a specialist who can better assist you. You'll be contacted within 1 hour.",
                "action": "escalate",
                "category": category,
                "escalation_reason": "High priority or customer sentiment",
            }

        # Use knowledge base for common issues
        if category in self.knowledge_base:
            kb_response = self.knowledge_base[category]
        else:
            kb_response = None

        # Generate AI response
        prompt = f"""
        You are a helpful customer support agent.
        Customer type: {query.customer_type}
        Query category: {category}
        Urgency: {query.urgency}

        Provide a professional, helpful response.
        Keep responses concise but complete.
        If you have knowledge base info, incorporate it appropriately.

        Knowledge base info: {kb_response}

        Customer query: {query.query}
        """

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3, max_output_tokens=300
                ),
            )

            ai_response = response.text

            return {
                "response": ai_response,
                "action": "respond",
                "category": category,
                "escalation_reason": None,
            }

        except Exception as e:
            return {
                "response": "I apologize, but I'm experiencing technical difficulties. Please try again or contact our support team directly.",
                "action": "error",
                "category": category,
                "error": str(e),
            }


# Convenience functions for easy testing
def handle_customer_query(
    query: str, customer_type: str = "regular", urgency: str = "normal"
) -> Dict[str, str]:
    """Handle a customer query with default agent."""
    import os

    if not HAS_GOOGLE_GENAI:
        return {
            "response": "Google Generative AI is not available. Please install with: pip install 'agenttest[google]'",
            "action": "error",
            "category": "system",
            "error": "google-generativeai not installed",
        }

    # Try both Gemini environment variable names
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        return {
            "response": "API key not configured. Please set GOOGLE_API_KEY or GEMINI_API_KEY environment variable.",
            "action": "error",
            "category": "system",
            "error": "API key not set",
        }

    agent = CustomerSupportAgent(api_key)
    customer_query = CustomerQuery(
        query=query, customer_type=customer_type, urgency=urgency
    )

    return agent.generate_response(customer_query)


def quick_support_response(query: str) -> str:
    """Get a quick support response (just the text)."""
    result = handle_customer_query(query)
    return result["response"]


def classify_query(query: str) -> str:
    """Classify a query without needing API key or Google AI."""
    query_lower = query.lower()

    if any(word in query_lower for word in ["bill", "payment", "charge", "refund"]):
        return "billing"
    elif any(word in query_lower for word in ["bug", "error", "crash", "not working"]):
        return "technical"
    elif any(
        word in query_lower for word in ["account", "login", "password", "access"]
    ):
        return "account"
    elif any(word in query_lower for word in ["feature", "how to", "documentation"]):
        return "product"
    else:
        return "general"
