# Quick Start Guide

Get up and running with AgentTest in 5 minutes! This guide will walk you through creating your first AI agent test.

## 🚀 Setup (30 seconds)

```bash
# Install AgentTest
pip install agenttest

# Set your API key
export OPENAI_API_KEY="your-api-key-here"

# Initialize project
agenttest init
```

## 📝 Your First Test (2 minutes)

Create a test file `tests/test_my_agent.py`:

```python
from agent_test import agent_test

# Simple similarity test
@agent_test(criteria=['similarity'])
def test_basic_response():
    """Test if agent gives expected response."""

    # Your agent's response (replace with actual agent call)
    agent_response = "The capital of France is Paris."

    return {
        "input": "What is the capital of France?",
        "actual": agent_response,
        "expected": "Paris is the capital of France."
    }

# Multi-evaluator test
@agent_test(criteria=['similarity', 'contains', 'llm_judge'])
def test_comprehensive_response():
    """Test agent response with multiple criteria."""

    # Simulate your agent
    def my_agent(prompt):
        return f"Based on your question '{prompt}', here's my response: The answer is 42."

    user_input = "What is the meaning of life?"
    agent_output = my_agent(user_input)

    return {
        "input": user_input,
        "actual": agent_output,
        "expected": "The meaning of life is often considered to be 42.",
        "contains": ["42", "meaning", "life"],          # Must contain these words
        "evaluation_criteria": ["accuracy", "helpfulness"]  # For LLM judge
    }
```

## 🏃‍♂️ Run Your Tests (30 seconds)

```bash
# Run all tests
agenttest run

# Run with detailed output
agenttest run --verbose

# Run specific test
agenttest run --path tests/test_my_agent.py
```

You'll see output like:

```
🧪 Running AgentTest suite...

📊 Test Results Summary:
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Test                          ┃ Status  ┃ Score   ┃ Duration     ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ test_basic_response           │ ✅ PASS │ 0.850   │ 0.234s       │
│ test_comprehensive_response   │ ✅ PASS │ 0.923   │ 1.456s       │
└───────────────────────────────┴─────────┴─────────┴──────────────┘

📈 Overall Results:
• Total Tests: 2
• Passed: 2 (100%)
• Failed: 0 (0%)
• Average Score: 0.887
• Total Duration: 1.69s

✅ Test run completed!
```

## 🔍 Understanding the Results (1 minute)

Each test is evaluated using the specified criteria:

- **similarity**: How similar is the actual vs expected response
- **contains**: Whether the response contains required words/phrases
- **llm_judge**: AI evaluation based on custom criteria

## 🎯 Common Test Patterns

### Pattern 1: API Response Testing

```python
@agent_test(criteria=['similarity', 'contains'])
def test_api_response():
    """Test API endpoint response quality."""

    response = call_my_api("summarize this text...")

    return {
        "input": "Long text to summarize...",
        "actual": response["summary"],
        "expected": "Expected summary content...",
        "contains": ["key", "points", "summary"]
    }
```

### Pattern 2: Conversation Testing

```python
@agent_test(criteria=['llm_judge'])
def test_conversation_quality():
    """Test conversational agent responses."""

    messages = [
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "assistant", "content": agent_response}
    ]

    return {
        "input": "Hello, how are you?",
        "actual": agent_response,
        "evaluation_criteria": ["politeness", "engagement", "naturalness"]
    }
```

### Pattern 3: Data Extraction Testing

```python
@agent_test(criteria=['regex', 'contains'])
def test_data_extraction():
    """Test if agent extracts data correctly."""

    extracted_data = my_extraction_agent(document)

    return {
        "input": document,
        "actual": extracted_data,
        "patterns": [
            r"\d{4}-\d{2}-\d{2}",  # Date pattern
            r"\$\d+\.\d{2}",       # Currency pattern
            r"\b[A-Z][a-z]+\s[A-Z][a-z]+\b"  # Name pattern
        ],
        "contains": ["John Doe", "2024-01-15", "$99.99"]
    }
```

## 🛠️ Next Steps

### Explore Evaluators

Learn about different evaluation methods:

- **Similarity**: Text similarity comparison
- **LLM Judge**: AI-powered evaluation
- **Metrics**: ROUGE, BLEU, METEOR scores
- **Patterns**: Regex and text matching

See [Evaluators Guide](evaluators.md) for details.

### Advanced Features

- **Git Integration**: Track performance across commits
- **Batch Testing**: Run multiple test scenarios
- **Custom Evaluators**: Build your own evaluation logic
- **Logging**: Debug with detailed execution logs

### Configuration

Customize evaluation thresholds, LLM providers, and more in `.agenttest/config.yaml`:

```yaml
evaluators:
  - name: 'similarity'
    config:
      threshold: 0.7 # Lower threshold = more lenient
      method: 'cosine' # cosine, levenshtein, jaccard
```

## 📚 Examples Gallery

### Simple Q&A Agent

```python
@agent_test(criteria=['similarity'])
def test_qa_accuracy():
    return {
        "input": "What's 2+2?",
        "actual": "The answer is 4.",
        "expected": "2+2 equals 4."
    }
```

### Content Generation

```python
@agent_test(criteria=['llm_judge', 'contains'])
def test_blog_post_generation():
    return {
        "input": "Write about AI testing",
        "actual": generate_blog_post("AI testing"),
        "contains": ["testing", "AI", "automation"],
        "evaluation_criteria": ["coherence", "informativeness", "engagement"]
    }
```

### Code Generation

```python
@agent_test(criteria=['regex', 'contains'])
def test_code_generation():
    return {
        "input": "Generate a Python function to calculate factorial",
        "actual": generate_code("factorial function"),
        "patterns": [r"def\s+\w+\(", r"return\s+\w+"],
        "contains": ["def", "factorial", "return"]
    }
```

## 🔧 Troubleshooting

**No tests found?**

- Ensure test files start with `test_`
- Check that functions are decorated with `@agent_test`

**API errors?**

- Verify API keys are set correctly
- Check internet connection
- Validate API quotas

**Low scores?**

- Adjust similarity thresholds in config
- Use more specific expected outputs
- Try different evaluation criteria

---

**Ready for more?** Check out:

- [Configuration Guide](configuration.md) - Customize your setup
- [Writing Tests](writing-tests.md) - Advanced test patterns
- [CLI Commands](cli-commands.md) - Power user features
