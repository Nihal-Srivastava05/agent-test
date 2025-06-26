# Basic Examples

This guide provides practical examples to help you get started with AgentTest. Each example demonstrates different features and evaluation approaches.

## 🚀 Getting Started Examples

### Example 1: Simple Q&A Agent {#similarity-evaluator-examples}

Test a basic question-answering agent with similarity evaluation.

```python
from agent_test import agent_test

def my_qa_agent(question):
    """Simple Q&A agent (replace with your implementation)."""
    responses = {
        "What is the capital of France?": "The capital of France is Paris.",
        "What is 2+2?": "2+2 equals 4.",
        "Who wrote Romeo and Juliet?": "William Shakespeare wrote Romeo and Juliet."
    }
    return responses.get(question, "I don't know the answer to that question.")

@agent_test(criteria=['similarity'])
def test_basic_qa():
    """Test basic question answering capability."""
    question = "What is the capital of France?"
    answer = my_qa_agent(question)

    return {
        "input": question,
        "actual": answer,
        "expected": "Paris is the capital of France."
    }

@agent_test(criteria=['similarity'])
def test_math_qa():
    """Test mathematical question answering."""
    question = "What is 2+2?"
    answer = my_qa_agent(question)

    return {
        "input": question,
        "actual": answer,
        "expected": "The answer is 4."
    }
```

### Example 2: Content Contains Validation

Ensure your agent's responses contain required information.

```python
@agent_test(criteria=['contains'])
def test_python_libraries():
    """Test if agent mentions required Python libraries."""

    def get_data_science_libraries():
        return "For data science in Python, you should use pandas for data manipulation, numpy for numerical computing, matplotlib for visualization, and scikit-learn for machine learning."

    response = get_data_science_libraries()

    return {
        "input": "What Python libraries should I use for data science?",
        "actual": response,
        "contains": ["pandas", "numpy", "matplotlib", "scikit-learn"]
    }

@agent_test(criteria=['contains'])
def test_recipe_ingredients():
    """Test if agent includes all required ingredients."""

    def get_pancake_recipe():
        return "To make pancakes, you need flour, eggs, milk, sugar, baking powder, and salt. Mix them together and cook on a griddle."

    response = get_pancake_recipe()

    return {
        "input": "How do I make pancakes?",
        "actual": response,
        "contains": ["flour", "eggs", "milk", "sugar", "baking powder", "salt"]
    }
```

### Example 3: Pattern Matching with Regex {#pattern-matching-examples}

Validate structured outputs using regular expressions.

```python
@agent_test(criteria=['regex'])
def test_contact_extraction():
    """Test contact information extraction."""

    def extract_contact_info():
        return """
        Name: John Doe
        Email: john.doe@email.com
        Phone: 555-123-4567
        Date: 2024-06-26
        """

    extracted_info = extract_contact_info()

    return {
        "input": "Extract contact information from the document",
        "actual": extracted_info,
        "patterns": [
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # Email
            r"\b\d{3}-\d{3}-\d{4}\b",                                 # Phone
            r"\b\d{4}-\d{2}-\d{2}\b"                                  # Date
        ]
    }

@agent_test(criteria=['regex'])
def test_url_generation():
    """Test if agent generates valid URLs."""

    def generate_urls():
        return "Check out these resources: https://www.python.org and http://github.com/user/repo"

    response = generate_urls()

    return {
        "input": "Generate some useful URLs",
        "actual": response,
        "patterns": [r"https?://[^\s]+"]  # URL pattern
    }
```

## 🔄 Multi-Evaluator Examples

### Example 4: Comprehensive Evaluation

Combine multiple evaluators for thorough testing.

```python
@agent_test(criteria=['similarity', 'contains', 'llm_judge'])
def test_explanation_quality():
    """Test explanation quality across multiple dimensions."""

    def explain_photosynthesis():
        return "Photosynthesis is the process by which plants convert sunlight, carbon dioxide, and water into glucose and oxygen. This process uses chlorophyll in the leaves and is essential for plant survival and oxygen production."

    explanation = explain_photosynthesis()

    return {
        "input": "Explain photosynthesis",
        "actual": explanation,
        "expected": "Photosynthesis converts sunlight into energy for plants using chlorophyll, carbon dioxide, and water.",
        "contains": ["sunlight", "chlorophyll", "carbon dioxide", "water", "oxygen"],
        "evaluation_criteria": ["accuracy", "clarity", "completeness"]
    }
```

## 📊 Real-World Scenarios

### Example 5: Customer Support Agent

Test a customer support chatbot's responses.

```python
@agent_test(criteria=['llm_judge', 'contains'])
def test_customer_support_greeting():
    """Test customer support greeting quality."""

    def customer_support_bot(message):
        if "hello" in message.lower() or "hi" in message.lower():
            return "Hello! Welcome to our customer support. I'm here to help you with any questions or issues you may have. How can I assist you today?"
        return "I'm here to help! What can I do for you?"

    response = customer_support_bot("Hello, I need help")

    return {
        "input": "Hello, I need help",
        "actual": response,
        "contains": ["hello", "help", "assist"],
        "evaluation_criteria": ["politeness", "helpfulness", "professionalism"]
    }
```

## 📈 Running the Examples

### Save and Run Tests

```bash
# Run all examples
agenttest run --path test_examples.py

# Run with verbose output
agenttest run --path test_examples.py --verbose

# Run specific examples
agenttest run --path test_examples.py::test_basic_qa
```

### Expected Output

```
🧪 Running AgentTest suite...

📊 Test Results Summary:
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Test                          ┃ Status  ┃ Score   ┃ Duration     ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ test_basic_qa                 │ ✅ PASS │ 0.892   │ 0.234s       │
│ test_python_libraries         │ ✅ PASS │ 1.000   │ 0.156s       │
│ test_contact_extraction       │ ✅ PASS │ 1.000   │ 0.089s       │
│ test_explanation_quality      │ ✅ PASS │ 0.845   │ 1.234s       │
│ test_customer_support_greeting│ ✅ PASS │ 0.923   │ 0.678s       │
└───────────────────────────────┴─────────┴─────────┴──────────────┘

📈 Overall Results:
• Total Tests: 5
• Passed: 5 (100%)
• Failed: 0 (0%)
• Average Score: 0.912
• Total Duration: 2.39s

✅ Test run completed!
```

## 🔄 Next Steps

1. **Modify Examples**: Adapt these examples to your specific agent
2. **Add More Evaluators**: Experiment with different evaluation criteria
3. **Create Test Suites**: Organize related tests into coherent suites
4. **Use Configuration**: Customize evaluator thresholds and settings
5. **Track Progress**: Use git integration to monitor improvements

## 🔗 Related Documentation

- [Writing Tests](../writing-tests.md) - Comprehensive test writing guide
- [Evaluators](../evaluators.md) - Understanding all evaluation options
- [Configuration](../configuration.md) - Customizing test behavior
