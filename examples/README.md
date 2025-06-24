# 🧪 AgentTest Examples & Complete Tutorial

This comprehensive guide walks you through using AgentTest to test AI agents and prompts, from creating your first project to advanced evaluation scenarios.

## 📋 Table of Contents

- [🚀 Quick Start](#-quick-start)
- [🤖 Sample AI Agent Project](#-sample-ai-agent-project)
- [🔧 Setting Up AgentTest](#-setting-up-agenttest)
- [🎯 Test Generation](#-test-generation)
- [🏃‍♂️ Running Tests](#-running-tests)
- [📊 Evaluator Deep Dive](#-evaluator-deep-dive)
- [🔍 Advanced Testing Scenarios](#-advanced-testing-scenarios)
- [📈 Results & Analysis](#-results--analysis)
- [🌟 Best Practices](#-best-practices)

## 🚀 Quick Start

### 1. Install AgentTest

```bash
# Install with all features
pip install agenttest[all]

# Or install minimal version
pip install agenttest
```

### 2. Set Up API Keys

```bash
# Choose your preferred LLM provider(s)
export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-anthropic-key"
export GOOGLE_API_KEY="your-google-api-key"
```

### 3. Initialize Your Project

```bash
cd your-ai-project
agenttest init
```

### 4. Generate and Run Tests

```bash
# Auto-generate tests from your code
agenttest generate

# Run all tests
agenttest run

# View results
agenttest log
```

## 🤖 Sample AI Agent Project

Let's create a realistic AI agent project to demonstrate AgentTest capabilities. We'll build a **Customer Support Agent** that handles various types of customer inquiries.

### Project Structure

```
my-ai-project/
├── agents/
│   ├── __init__.py
│   ├── customer_support.py
│   └── content_generator.py
├── tests/
│   ├── __init__.py
│   └── test_agents.py
├── .agenttest/
│   ├── config.yaml
│   └── templates/
├── requirements.txt
└── README.md
```

### Create the Customer Support Agent

Create `agents/customer_support.py`:

```python
"""
Customer Support AI Agent

Handles customer inquiries, classifies issues, and escalates when necessary.
"""

import openai
from typing import Dict, Optional
from dataclasses import dataclass

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
        self.client = openai.OpenAI(api_key=api_key)
        self.model = "gpt-4"

        # Knowledge base for common issues
        self.knowledge_base = {
            "billing": "For billing inquiries, contact billing@company.com",
            "technical": "For technical issues, try restarting the application first",
            "account": "For account issues, verify your email and password",
            "product": "For product info, visit docs.company.com"
        }

    def classify_query(self, query: str) -> str:
        """Classify customer query into categories."""
        query_lower = query.lower()

        if any(word in query_lower for word in ["bill", "payment", "charge", "refund"]):
            return "billing"
        elif any(word in query_lower for word in ["bug", "error", "crash", "not working"]):
            return "technical"
        elif any(word in query_lower for word in ["account", "login", "password"]):
            return "account"
        elif any(word in query_lower for word in ["feature", "how to", "documentation"]):
            return "product"
        else:
            return "general"

    def should_escalate(self, query: CustomerQuery) -> bool:
        """Determine if query should be escalated."""
        escalation_keywords = [
            "frustrated", "angry", "cancel", "lawsuit",
            "terrible", "worst", "hate", "refund", "money back"
        ]

        if query.urgency == "critical":
            return True

        if query.customer_type == "enterprise" and query.urgency == "high":
            return True

        if any(keyword in query.query.lower() for keyword in escalation_keywords):
            return True

        return False

    def generate_response(self, query: CustomerQuery) -> Dict[str, str]:
        """Generate response to customer query."""
        category = self.classify_query(query.query)

        # Check if escalation is needed
        if self.should_escalate(query):
            return {
                "response": "I understand your concern. Let me connect you with a specialist who can better assist you.",
                "action": "escalate",
                "category": category,
                "escalation_reason": "High priority or negative sentiment"
            }

        # Generate standard response
        kb_info = self.knowledge_base.get(category, "")

        return {
            "response": f"Thank you for your {category} inquiry. {kb_info} I'm here to help resolve this issue.",
            "action": "respond",
            "category": category,
            "escalation_reason": None
        }

# Convenience functions for easy testing
def handle_customer_query(query: str, customer_type: str = "regular", urgency: str = "normal") -> Dict[str, str]:
    """Handle customer query with mock agent."""
    # For demo purposes, use a simple mock
    agent = CustomerSupportAgent("demo-key")
    customer_query = CustomerQuery(query=query, customer_type=customer_type, urgency=urgency)
    return agent.generate_response(customer_query)

def quick_support_response(query: str) -> str:
    """Get quick support response text."""
    result = handle_customer_query(query)
    return result["response"]
```

### Create Content Generator Agent

Create `agents/content_generator.py`:

```python
"""
Content Generator AI Agent

Generates blog posts, social media content, and marketing copy.
"""

from typing import Dict

class ContentGenerator:
    """AI-powered content generation agent."""

    def __init__(self, api_key: str = "demo"):
        """Initialize content generator."""
        self.api_key = api_key

    def generate_blog_post(self, topic: str, tone: str = "professional") -> Dict[str, str]:
        """Generate blog post content."""
        return {
            "title": f"Understanding {topic}",
            "content": f"This is a {tone} blog post about {topic}. It covers key aspects and provides valuable insights.",
            "word_count": 20,
            "tone": tone
        }

    def generate_social_media_post(self, topic: str, platform: str = "twitter") -> Dict[str, str]:
        """Generate social media content."""
        hashtags = f" #{topic.replace(' ', '')} #AI" if platform == "twitter" else ""
        content = f"Exploring {topic} and its impact.{hashtags}"

        return {
            "content": content,
            "platform": platform,
            "character_count": len(content),
            "within_limit": len(content) <= 280
        }

# Convenience functions
def generate_quick_blog(topic: str) -> str:
    """Generate quick blog post."""
    generator = ContentGenerator()
    result = generator.generate_blog_post(topic)
    return result["content"]

def generate_quick_social(topic: str) -> str:
    """Generate quick social media post."""
    generator = ContentGenerator()
    result = generator.generate_social_media_post(topic)
    return result["content"]
```

## 🔧 Setting Up AgentTest

### 1. Initialize AgentTest

```bash
cd my-ai-project
agenttest init --template basic
```

This creates:

- `.agenttest/config.yaml` - Main configuration file
- `.agenttest/templates/` - Test templates
- `tests/test_agents.py` - Initial test file

### 2. Configure AgentTest

Edit `.agenttest/config.yaml`:

```yaml
version: '1.0'
project_name: 'Customer Support Agent Testing'

# LLM Configuration
llm:
  provider: 'openai' # or 'anthropic', 'gemini'
  model: 'gpt-4'
  temperature: 0.0
  max_tokens: 1000

# Evaluator Configuration
evaluators:
  - name: 'similarity'
    type: 'string_similarity'
    config:
      method: 'cosine'
      threshold: 0.8

  - name: 'llm_judge'
    type: 'llm_as_judge'
    config:
      provider: 'openai'
      model: 'gpt-4'
      criteria: ['accuracy', 'relevance', 'helpfulness']

  - name: 'regex_check'
    type: 'regex'
    config:
      flags: ['IGNORECASE']

  - name: 'contains_check'
    type: 'contains'
    config:
      case_sensitive: false

  - name: 'metrics'
    type: 'metric'
    config:
      metrics: ['bleu', 'rouge']

# Testing Configuration
testing:
  test_dirs: ['tests']
  test_patterns: ['test_*.py', '*_test.py']
  parallel: false
  timeout: 300

# Logging Configuration
logging:
  level: 'INFO'
  git_aware: true
  results_dir: '.agenttest/results'
```

### 3. Create Requirements File

Create `requirements.txt`:

```
agenttest[all]
openai>=1.0.0
anthropic>=0.7.0
google-generativeai>=0.3.0
```

## 🎯 Test Generation

AgentTest can automatically generate test cases by analyzing your agent code:

### 1. Auto-Generate Tests

```bash
# Generate tests for all agents
agenttest generate

# Generate for specific agent
agenttest generate --agent agents/customer_support.py --count 10

# Generate in different formats
agenttest generate --agent agents/customer_support.py --format yaml
agenttest generate --agent agents/content_generator.py --format json
```

### 2. Example Generated Test

After running `agenttest generate`, you'll get `tests/test_customer_support_generated.py`:

```python
"""
Generated test for customer_support.

This test was automatically generated by AgentTest.
"""

from agenttest import agent_test
from agents.customer_support import *

@agent_test(criteria=['accuracy', 'relevance', 'helpfulness'], tags=['generated'])
def test_handle_billing_query():
    """Test handling of billing-related customer queries."""
    input_data = {
        "query": "I was charged twice for my subscription",
        "customer_type": "premium",
        "urgency": "high"
    }

    actual = handle_customer_query(
        input_data["query"],
        input_data["customer_type"],
        input_data["urgency"]
    )

    return {
        "input": input_data,
        "actual": actual,
        "evaluation_criteria": {
            "accuracy": "Should address billing issue accurately",
            "relevance": "Should be relevant to billing query",
            "helpfulness": "Should provide helpful next steps"
        }
    }

@agent_test(criteria=['accuracy'], tags=['generated', 'escalation'])
def test_escalation_detection():
    """Test automatic escalation for frustrated customers."""
    input_data = {
        "query": "This is terrible service! I want my money back!",
        "customer_type": "regular",
        "urgency": "high"
    }

    actual = handle_customer_query(
        input_data["query"],
        input_data["customer_type"],
        input_data["urgency"]
    )

    return {
        "input": input_data,
        "actual": actual,
        "evaluation_criteria": {
            "accuracy": "Should detect need for escalation"
        }
    }
```

## 🏃‍♂️ Running Tests

### 1. Basic Test Execution

```bash
# Run all tests
agenttest run

# Run with verbose output
agenttest run --verbose

# Run specific test files
agenttest run --files tests/test_customer_support.py

# Run tests with specific tags
agenttest run --tags billing,escalation

# Run tests with specific evaluators
agenttest run --evaluators similarity,llm_judge
```

### 2. Example Test Output

```
🧪 AgentTest Runner
==================

📊 Test Discovery
├── Found 3 test files
├── Discovered 8 test functions
├── Tagged tests: 5 billing, 3 escalation
└── Using evaluators: similarity, llm_judge, regex, contains

🔄 Running Tests
├── test_handle_billing_query ✅ PASSED (0.8s) [Score: 0.89]
├── test_escalation_detection ✅ PASSED (1.2s) [Score: 0.95]
├── test_email_format_validation ✅ PASSED (0.3s) [Regex: ✓]
├── test_contains_security_terms ✅ PASSED (0.2s) [Contains: 4/4]
└── test_content_quality_metrics ✅ PASSED (1.1s) [ROUGE: 0.72]

📈 Results Summary
├── Total Tests: 5
├── Passed: 5 (100%)
├── Failed: 0
├── Average Score: 0.89
├── Total Time: 3.6s
└── Git Commit: abc123f

📝 Detailed Results: .agenttest/results/2024-01-15_10-30-45.json
```

### 3. Advanced Test Execution

```bash
# Run tests in parallel
agenttest run --parallel --workers 4

# Run with timeout
agenttest run --timeout 120

# Run tests and export results
agenttest run --export-json results.json --export-csv results.csv

# Run specific test by name
agenttest run --test test_handle_billing_query

# Run with custom configuration
agenttest run --config custom_config.yaml
```

## 📊 Evaluator Deep Dive

AgentTest provides five main types of evaluators. Let's explore each with detailed examples:

### 1. String Similarity Evaluator

**Purpose**: Measures how similar the actual output is to expected output.

**Configuration**:

```yaml
evaluators:
  - name: 'similarity'
    type: 'string_similarity'
    config:
      method: 'cosine' # cosine, jaccard, levenshtein
      threshold: 0.8 # Pass threshold (0.0-1.0)
      case_sensitive: false
```

**Example Test**:

```python
@agent_test(criteria=['similarity'])
def test_greeting_consistency():
    """Test consistent greeting responses."""
    input_data = "Hello"
    expected = "Hello! How can I help you today?"
    actual = quick_support_response(input_data)

    return {
        "input": input_data,
        "expected": expected,
        "actual": actual
    }
```

**Methods Available**:

- `cosine`: Best for semantic similarity
- `jaccard`: Good for word overlap
- `levenshtein`: Good for edit distance
- `exact`: For exact string matching

### 2. LLM-as-Judge Evaluator

**Purpose**: Uses LLM to evaluate responses based on custom criteria.

**Configuration**:

```yaml
evaluators:
  - name: 'llm_judge'
    type: 'llm_as_judge'
    config:
      provider: 'openai' # openai, anthropic, gemini
      model: 'gpt-4'
      temperature: 0.0
      criteria: ['accuracy', 'helpfulness']
```

**Basic Example**:

```python
@agent_test(criteria=['llm_judge'])
def test_customer_service_quality():
    """Test customer service response quality."""
    input_data = "I'm frustrated with my order delay"
    actual = handle_customer_query(input_data, urgency="high")

    return {
        "input": input_data,
        "actual": actual,
        "evaluation_criteria": {
            "empathy": "Response should show understanding of customer frustration",
            "professionalism": "Should maintain professional tone",
            "helpfulness": "Should offer concrete solutions or next steps",
            "timeliness": "Should acknowledge the delay issue"
        }
    }
```

**Advanced Example with Scoring**:

```python
@agent_test(criteria=['llm_judge'])
def test_technical_explanation():
    """Test technical explanation quality with weighted scoring."""
    input_data = "Explain how our API works"
    actual = "Our API uses REST endpoints with JSON payloads. You authenticate with API keys and can access user data through GET requests."

    return {
        "input": input_data,
        "actual": actual,
        "evaluation_criteria": {
            "technical_accuracy": "Should be technically correct about API functionality",
            "clarity": "Should be clear and understandable",
            "completeness": "Should cover key API concepts",
            "examples": "Should include examples when helpful"
        },
        "scoring_weights": {
            "technical_accuracy": 0.4,
            "clarity": 0.3,
            "completeness": 0.2,
            "examples": 0.1
        }
    }
```

### 3. Regex Evaluator

**Purpose**: Tests if output matches specific patterns using regular expressions.

**Configuration**:

```yaml
evaluators:
  - name: 'regex_check'
    type: 'regex'
    config:
      flags: ['IGNORECASE', 'MULTILINE']
```

**Examples**:

```python
@agent_test(criteria=['regex'])
def test_email_format():
    """Test if response contains valid email format."""
    input_data = "What's your support email?"
    actual = "Contact support at support@company.com or help@company.com"

    return {
        "input": input_data,
        "actual": actual,
        "pattern": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    }

@agent_test(criteria=['regex'])
def test_phone_number_format():
    """Test phone number format validation."""
    input_data = "What's your phone number?"
    actual = "Call us at (555) 123-4567 or (555) 987-6543"

    return {
        "input": input_data,
        "actual": actual,
        "pattern": r'\(\d{3}\)\s\d{3}-\d{4}'
    }

@agent_test(criteria=['regex'])
def test_multiple_patterns():
    """Test multiple regex patterns."""
    input_data = "Generate order summary"
    actual = "Order #ORD-2024-001, Total: $99.99, Contact: customer@email.com"

    return {
        "input": input_data,
        "actual": actual,
        "patterns": [
            r'Order #ORD-\d{4}-\d{3}',                    # Order ID
            r'\$\d+\.\d{2}',                              # Currency
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'  # Email
        ]
    }
```

### 4. Contains Evaluator

**Purpose**: Tests if output contains specific words, phrases, or elements.

**Configuration**:

```yaml
evaluators:
  - name: 'contains_check'
    type: 'contains'
    config:
      case_sensitive: false
      partial_match: true
```

**Examples**:

```python
@agent_test(criteria=['contains'])
def test_security_response():
    """Test security response contains required elements."""
    input_data = "How do you protect my data?"
    actual = "We use encryption, secure servers, and follow privacy regulations to protect your information."

    return {
        "input": input_data,
        "actual": actual,
        "expected": ["encryption", "secure", "privacy", "protect"]
    }

@agent_test(criteria=['contains'])
def test_comprehensive_policy():
    """Test comprehensive policy response."""
    input_data = "What's your refund policy?"
    actual = "We offer a 30-day money-back guarantee. Contact support to process refunds."

    return {
        "input": input_data,
        "actual": actual,
        "required_all": ["30-day", "money-back", "guarantee"],      # All must be present
        "required_any": ["refund", "return", "money back"],         # At least one
        "forbidden": ["no refunds", "non-refundable"],              # None allowed
        "min_required": 2  # At least 2 required terms
    }

@agent_test(criteria=['contains'])
def test_technical_terms():
    """Test technical documentation contains appropriate terms."""
    input_data = "Explain machine learning"
    actual = "Machine learning uses algorithms to analyze data, train models, and make predictions through neural networks."

    return {
        "input": input_data,
        "actual": actual,
        "expected": ["machine learning", "algorithms", "data", "models"],
        "bonus_terms": ["neural networks", "training", "predictions"],  # Extra credit
        "technical_level": "intermediate"
    }
```

### 5. Metric Evaluator

**Purpose**: Uses standard NLP metrics to evaluate text quality.

**Configuration**:

```yaml
evaluators:
  - name: 'metrics'
    type: 'metric'
    config:
      metrics: ['bleu', 'rouge', 'meteor']
      rouge_variants: ['rouge-1', 'rouge-2', 'rouge-l']
```

**Examples**:

```python
@agent_test(criteria=['metrics'])
def test_summary_quality():
    """Test summary quality using ROUGE metrics."""
    input_data = "Summarize cloud computing benefits"
    reference = "Cloud computing offers scalability, cost savings, and improved accessibility for businesses."
    actual = "Cloud computing provides scalable resources, reduces costs, and enhances business accessibility."

    return {
        "input": input_data,
        "actual": actual,
        "reference": reference,
        "metrics": {
            "rouge": {
                "min_score": 0.4,
                "variants": ["rouge-1", "rouge-2", "rouge-l"]
            }
        }
    }

@agent_test(criteria=['metrics'])
def test_content_quality_comprehensive():
    """Test content quality with multiple metrics."""
    input_data = "Write about renewable energy"
    reference = "Renewable energy sources like solar and wind provide clean power while reducing environmental impact."
    actual = "Solar and wind energy offer clean electricity generation with minimal environmental effects."

    return {
        "input": input_data,
        "actual": actual,
        "reference": reference,
        "metrics": {
            "rouge": {"min_score": 0.5},
            "bleu": {"min_score": 0.3, "smoothing": True},
            "meteor": {"min_score": 0.4}
        }
    }
```

## 🔍 Advanced Testing Scenarios

### 1. Multi-Evaluator Tests

```python
@agent_test(criteria=['similarity', 'contains', 'regex', 'llm_judge'])
def test_comprehensive_order_response():
    """Test order response with multiple evaluation methods."""
    input_data = "Check my order status"
    actual = "Order #ORD-2024-001 is confirmed. Total: $99.99. Track at track.company.com"
    expected = "Your order #ORD-2024-001 has been confirmed for $99.99"

    return {
        "input": input_data,
        "actual": actual,
        "expected": expected,
        # Contains evaluation
        "contains_required": ["order", "confirmed", "total"],
        # Regex evaluation
        "regex_patterns": [
            r'Order #ORD-\d{4}-\d{3}',
            r'\$\d+\.\d{2}',
            r'track\.[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        ],
        # LLM judge evaluation
        "evaluation_criteria": {
            "completeness": "Should include order ID, status, and total",
            "clarity": "Should be clear and informative",
            "actionability": "Should provide tracking information"
        }
    }
```

### 2. Edge Case Testing

```python
@agent_test(criteria=['llm_judge'])
def test_empty_input():
    """Test handling of empty input."""
    input_data = ""
    actual = handle_customer_query(input_data)

    return {
        "input": input_data,
        "actual": actual,
        "evaluation_criteria": {
            "graceful_handling": "Should handle empty input gracefully",
            "user_guidance": "Should guide user to provide input",
            "no_errors": "Should not produce error messages"
        }
    }

@agent_test(criteria=['llm_judge'])
def test_very_long_input():
    """Test handling of very long input."""
    input_data = "I need help with my account " * 100
    actual = handle_customer_query(input_data)

    return {
        "input": input_data,
        "actual": actual,
        "evaluation_criteria": {
            "performance": "Should handle long input efficiently",
            "accuracy": "Should still classify correctly",
            "conciseness": "Should provide concise response despite long input"
        }
    }
```

### 3. Scenario-Based Testing

```python
@agent_test(criteria=['llm_judge', 'contains'])
def test_escalation_scenarios():
    """Test various escalation scenarios."""
    scenarios = [
        {
            "query": "This is unacceptable! I demand to speak to a manager!",
            "customer_type": "premium",
            "urgency": "high",
            "expected_action": "escalate"
        },
        {
            "query": "I'm having a small issue with login",
            "customer_type": "regular",
            "urgency": "low",
            "expected_action": "respond"
        },
        {
            "query": "Our entire system is down, this is critical!",
            "customer_type": "enterprise",
            "urgency": "critical",
            "expected_action": "escalate"
        }
    ]

    results = []
    for scenario in scenarios:
        actual = handle_customer_query(
            scenario["query"],
            scenario["customer_type"],
            scenario["urgency"]
        )

        results.append({
            "input": scenario,
            "actual": actual,
            "expected_action": scenario["expected_action"],
            "evaluation_criteria": {
                "correct_action": f"Should {scenario['expected_action']} based on scenario",
                "appropriate_tone": "Should match tone to customer type and urgency"
            }
        })

    return results
```

### 4. Performance Testing

```python
@agent_test(criteria=['llm_judge'], tags=['performance'], timeout=30)
def test_response_time():
    """Test agent response time under load."""
    import time

    start_time = time.time()
    input_data = "I need help with billing"
    actual = handle_customer_query(input_data)
    response_time = time.time() - start_time

    return {
        "input": input_data,
        "actual": actual,
        "response_time": response_time,
        "evaluation_criteria": {
            "speed": "Should respond within acceptable time limits",
            "quality": "Should maintain quality despite speed requirements"
        }
    }
```

## 📈 Results & Analysis

### 1. Viewing Test Results

```bash
# View latest results
agenttest log

# View specific number of results
agenttest log --limit 10

# View results with filtering
agenttest log --tags billing --since "2024-01-01"

# View results in different formats
agenttest log --format json
agenttest log --format csv
agenttest log --format html
```

### 2. Git-Aware Analysis

```bash
# Compare results between branches
agenttest compare main feature/new-model

# Compare specific commits
agenttest compare abc123 def456

# View regression analysis
agenttest log --regression --since "1 week ago"

# Generate trend report
agenttest log --trend --group-by day
```

### 3. Detailed Result Analysis

```bash
# Generate comprehensive report
agenttest run --generate-report

# Export detailed results
agenttest run --export-detailed results_detailed.json

# Create performance profile
agenttest run --profile --benchmark
```

### 4. Dashboard and Visualization

```bash
# Start web dashboard
agenttest dashboard --port 8080

# Generate static HTML report
agenttest report --output-dir ./reports

# Create charts and graphs
agenttest visualize --type performance,accuracy
```

## 🌟 Best Practices

### 1. Test Organization

```python
# Use descriptive test names
@agent_test(criteria=['llm_judge'], tags=['critical', 'customer_service'])
def test_critical_billing_escalation():
    """Test escalation for critical billing issues."""
    pass

# Group related tests
@agent_test(criteria=['similarity'], tags=['greeting', 'basic'])
def test_greeting_responses():
    """Test various greeting scenarios."""
    pass

# Use appropriate tags
@agent_test(criteria=['contains'], tags=['security', 'compliance'])
def test_security_information():
    """Test security-related information disclosure."""
    pass
```

### 2. Evaluation Strategy

```python
# Use multiple evaluators for comprehensive testing
@agent_test(criteria=['llm_judge', 'contains', 'regex'])
def test_comprehensive_response():
    """Comprehensive test using multiple evaluation methods."""
    pass

# Choose appropriate evaluators for your use case
@agent_test(criteria=['similarity'])  # For consistent responses
@agent_test(criteria=['llm_judge'])   # For quality assessment
@agent_test(criteria=['regex'])       # For format validation
@agent_test(criteria=['contains'])    # For required elements
@agent_test(criteria=['metrics'])     # For content quality
```

### 3. Configuration Management

```yaml
# Environment-specific configurations
development:
  llm:
    provider: 'openai'
    model: 'gpt-3.5-turbo' # Faster/cheaper for development

production:
  llm:
    provider: 'openai'
    model: 'gpt-4' # Higher quality for production

# Test-specific configurations
evaluators:
  - name: 'strict_similarity'
    type: 'string_similarity'
    config:
      threshold: 0.95 # High threshold for critical tests

  - name: 'lenient_similarity'
    type: 'string_similarity'
    config:
      threshold: 0.7 # Lower threshold for creative content
```

### 4. CI/CD Integration

```yaml
# .github/workflows/agenttest.yml
name: AgentTest CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run AgentTest
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
        run: |
          agenttest run --ci --verbose --export-json results.json

      - name: Upload results
        uses: actions/upload-artifact@v3
        with:
          name: test-results
          path: results.json
```

### 5. Debugging and Troubleshooting

```bash
# Debug test discovery
agenttest run --discovery-verbose

# Debug specific evaluator
agenttest run --evaluator-debug similarity

# Run with maximum verbosity
agenttest run --debug --verbose --trace

# Test single function
agenttest run --test test_specific_function --debug
```

## 🚀 Next Steps

1. **Start Simple**: Begin with basic similarity tests
2. **Add Complexity**: Gradually introduce LLM judges and regex patterns
3. **Automate**: Set up CI/CD integration
4. **Monitor**: Use git-aware logging to track improvements
5. **Scale**: Add more agents and comprehensive test suites
6. **Contribute**: Share your patterns with the community

## 📚 Additional Resources

- **[Basic Usage Example](basic_usage.py)** - Simple examples to get started
- **[Comprehensive Examples](comprehensive_examples.py)** - All evaluators with detailed examples
- **[Sample Agents](agents_sample.py)** - Sample agent implementations
- **[Main Documentation](../README.md)** - Complete framework documentation

## 🆘 Getting Help

- **Issues**: [GitHub Issues](https://github.com/agenttest-ai/agenttest/issues)
- **Discussions**: [GitHub Discussions](https://github.com/agenttest-ai/agenttest/discussions)
- **Email**: support@agenttest.ai
- **Documentation**: [Full Documentation](https://agenttest.readthedocs.io)

---

**Happy Testing! 🧪✨**

_This comprehensive guide provides everything you need to start testing your AI agents effectively with AgentTest._
