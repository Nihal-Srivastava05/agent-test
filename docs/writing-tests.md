# Writing Tests

This guide covers how to structure and write effective AI agent tests using AgentTest. Learn about test patterns, data formats, and best practices for comprehensive agent evaluation.

## 🧪 Test Structure

AgentTest uses a pytest-like decorator pattern for defining tests:

```python
from agent_test import agent_test

@agent_test(criteria=['similarity'])
def test_my_agent():
    """Test description."""
    return {
        "input": "Test input",
        "actual": agent_response,
        "expected": "Expected output"
    }
```

## 📝 Basic Test Anatomy

### Required Elements

Every test needs:

1. **@agent_test decorator** - Marks function as a test
2. **Test function** - Contains test logic
3. **Return dictionary** - Test data for evaluation

### Return Dictionary Structure

```python
{
    # Core fields
    "input": "What the agent receives",
    "actual": "What the agent produced",
    "expected": "What we expect",

    # Evaluator-specific fields
    "contains": ["required", "words"],
    "patterns": [r"regex_pattern"],
    "evaluation_criteria": ["accuracy", "clarity"],
    "metrics": {"rouge": {"min_score": 0.4}}
}
```

## 🔧 Test Decorator Options

### Basic Decorator

```python
@agent_test()                    # Uses default similarity evaluator
@agent_test(criteria=['similarity'])  # Explicit evaluator
```

### Advanced Decorator Options

```python
@agent_test(
    criteria=['similarity', 'llm_judge'],  # Multiple evaluators
    tags=['summarization', 'quality'],     # Test categorization
    timeout=60,                            # Test timeout (seconds)
    retry_count=2,                         # Retry on failure
    description="Test agent summarization" # Test description
)
```

### Decorator Parameters

| Parameter     | Type      | Default          | Description             |
| ------------- | --------- | ---------------- | ----------------------- |
| `criteria`    | List[str] | `['similarity']` | Evaluators to use       |
| `tags`        | List[str] | `[]`             | Test tags for filtering |
| `timeout`     | int       | `300`            | Timeout in seconds      |
| `retry_count` | int       | `0`              | Number of retries       |
| `**metadata`  | dict      | `{}`             | Additional metadata     |

## 📊 Evaluator-Specific Data

### Similarity Evaluator

```python
@agent_test(criteria=['similarity'])
def test_paraphrasing():
    return {
        "input": "Explain machine learning",
        "actual": agent_response,
        "expected": "Machine learning teaches computers to learn patterns from data"
    }
```

### Contains Evaluator

```python
@agent_test(criteria=['contains'])
def test_required_content():
    return {
        "input": "List data science tools",
        "actual": agent_response,
        "contains": ["Python", "pandas", "scikit-learn", "jupyter"]
    }
```

### Regex Evaluator

```python
@agent_test(criteria=['regex'])
def test_structured_output():
    return {
        "input": "Extract contact information",
        "actual": agent_response,
        "patterns": [
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # Email
            r"\b\d{3}-\d{3}-\d{4}\b",                                 # Phone
            r"\b\d{4}-\d{2}-\d{2}\b"                                  # Date
        ]
    }
```

### LLM Judge Evaluator

```python
@agent_test(criteria=['llm_judge'])
def test_creative_writing():
    return {
        "input": "Write a short story about AI",
        "actual": agent_story,
        "evaluation_criteria": ["creativity", "coherence", "engagement"]
    }
```

### Metrics Evaluator

```python
@agent_test(criteria=['metrics'])
def test_summarization_quality():
    return {
        "input": long_article,
        "actual": agent_summary,
        "reference": gold_standard_summary,
        "metrics": {
            "rouge": {
                "variants": ["rouge1", "rougeL"],
                "min_score": 0.4
            },
            "bleu": {
                "min_score": 0.3
            }
        }
    }
```

## 🎯 Common Test Patterns

### Pattern 1: Simple Q&A Testing

```python
@agent_test(criteria=['similarity'])
def test_factual_qa():
    """Test factual question answering."""
    question = "What is the capital of France?"
    answer = my_qa_agent(question)

    return {
        "input": question,
        "actual": answer,
        "expected": "Paris is the capital of France."
    }
```

### Pattern 2: Multi-Criteria Evaluation

```python
@agent_test(criteria=['similarity', 'contains', 'llm_judge'])
def test_comprehensive_response():
    """Test response quality across multiple dimensions."""
    prompt = "Explain quantum computing for beginners"
    response = my_agent(prompt)

    return {
        "input": prompt,
        "actual": response,
        "expected": "Quantum computing uses quantum mechanics principles...",
        "contains": ["quantum", "qubit", "superposition", "entanglement"],
        "evaluation_criteria": ["accuracy", "clarity", "beginner_friendly"]
    }
```

### Pattern 3: Conversation Testing

```python
@agent_test(criteria=['llm_judge'])
def test_conversation_flow():
    """Test multi-turn conversation quality."""
    conversation = [
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "assistant", "content": "I'm doing well, thank you! How can I help you today?"},
        {"role": "user", "content": "Can you help me learn Python?"}
    ]

    response = my_chatbot(conversation)

    return {
        "input": conversation,
        "actual": response,
        "evaluation_criteria": ["helpfulness", "engagement", "appropriateness"]
    }
```

### Pattern 4: Data Extraction Testing

```python
@agent_test(criteria=['regex', 'contains'])
def test_information_extraction():
    """Test structured data extraction."""
    document = """
    John Doe, born 1985-03-15, lives at 123 Main St.
    Contact: john.doe@email.com or 555-123-4567
    """

    extracted = my_extraction_agent(document)

    return {
        "input": document,
        "actual": extracted,
        "patterns": [
            r"\b[A-Z][a-z]+ [A-Z][a-z]+\b",           # Names
            r"\d{4}-\d{2}-\d{2}",                     # Dates
            r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",  # Emails
            r"\d{3}-\d{3}-\d{4}"                      # Phone numbers
        ],
        "contains": ["John Doe", "1985-03-15", "john.doe@email.com", "555-123-4567"]
    }
```

### Pattern 5: Code Generation Testing

```python
@agent_test(criteria=['regex', 'contains', 'llm_judge'])
def test_code_generation():
    """Test AI code generation capabilities."""
    prompt = "Write a Python function to calculate factorial"
    generated_code = my_code_agent(prompt)

    return {
        "input": prompt,
        "actual": generated_code,
        "patterns": [
            r"def\s+\w+\s*\(",                       # Function definition
            r"return\s+\w+",                         # Return statement
            r"if\s+\w+\s*[<>=]"                      # Conditional logic
        ],
        "contains": ["def", "factorial", "return"],
        "evaluation_criteria": ["correctness", "efficiency", "readability"]
    }
```

### Pattern 6: Content Generation Testing

```python
@agent_test(criteria=['metrics', 'llm_judge'])
def test_content_generation():
    """Test content generation quality."""
    topic = "The benefits of renewable energy"
    generated_content = my_content_agent(topic)
    reference_content = load_reference_content()

    return {
        "input": topic,
        "actual": generated_content,
        "reference": reference_content,
        "metrics": {
            "rouge": {"variants": ["rouge1", "rougeL"], "min_score": 0.3}
        },
        "evaluation_criteria": ["informativeness", "coherence", "engagement"]
    }
```

## 🔄 Dynamic Test Generation

### Parameterized Tests

```python
test_cases = [
    ("What is 2+2?", "4"),
    ("What is the capital of Japan?", "Tokyo"),
    ("Who wrote Romeo and Juliet?", "William Shakespeare")
]

def generate_qa_tests():
    """Generate multiple Q&A tests."""
    tests = []

    for i, (question, expected) in enumerate(test_cases):
        @agent_test(criteria=['similarity'])
        def test_func():
            answer = my_qa_agent(question)
            return {
                "input": question,
                "actual": answer,
                "expected": expected
            }

        test_func.__name__ = f"test_qa_{i}"
        tests.append(test_func)

    return tests

# Generate all tests
qa_tests = generate_qa_tests()
```

### Data-Driven Tests

```python
import json

@agent_test(criteria=['similarity', 'contains'])
def test_from_dataset():
    """Test using external dataset."""
    # Load test data
    with open('test_data.json') as f:
        test_data = json.load(f)

    results = []
    for case in test_data['test_cases']:
        response = my_agent(case['input'])
        results.append({
            "input": case['input'],
            "actual": response,
            "expected": case['expected'],
            "contains": case.get('required_terms', [])
        })

    return {"test_cases": results}  # Multi-case format
```

## 🏗️ Advanced Test Structures

### Multi-Step Tests

```python
@agent_test(criteria=['llm_judge'])
def test_multi_step_reasoning():
    """Test complex multi-step reasoning."""

    # Step 1: Initial query
    step1_response = my_agent("What factors affect climate change?")

    # Step 2: Follow-up based on response
    step2_response = my_agent(f"Given that {step1_response}, what can individuals do?")

    # Step 3: Synthesis
    step3_response = my_agent(f"Synthesize: {step1_response} and {step2_response}")

    return {
        "input": "Multi-step climate change discussion",
        "actual": step3_response,
        "evaluation_criteria": ["logical_flow", "completeness", "actionability"]
    }
```

### Comparative Tests

```python
@agent_test(criteria=['llm_judge'])
def test_model_comparison():
    """Compare different agent versions."""
    prompt = "Explain artificial intelligence"

    response_v1 = agent_v1(prompt)
    response_v2 = agent_v2(prompt)

    return {
        "input": prompt,
        "actual": f"V1: {response_v1}\n\nV2: {response_v2}",
        "evaluation_criteria": ["compare_quality", "compare_clarity", "prefer_version"]
    }
```

### Context-Aware Tests

```python
@agent_test(criteria=['similarity', 'llm_judge'])
def test_context_awareness():
    """Test agent's ability to maintain context."""

    # Establish context
    context = "You are a financial advisor speaking to a college student."
    query = "Should I invest in stocks?"

    response = my_agent(query, context=context)

    return {
        "input": f"Context: {context}\nQuery: {query}",
        "actual": response,
        "expected": "Student-appropriate financial advice",
        "evaluation_criteria": ["context_appropriate", "helpful", "age_appropriate"]
    }
```

## 🛠️ Test Utilities and Helpers

### Custom Assertion Functions

```python
def assert_contains_all(text, required_items):
    """Helper to check if text contains all required items."""
    missing = [item for item in required_items if item.lower() not in text.lower()]
    if missing:
        raise AssertionError(f"Missing required items: {missing}")

@agent_test(criteria=['similarity'])
def test_with_assertions():
    """Test with custom assertions."""
    response = my_agent("List programming languages")

    # Custom assertions
    assert_contains_all(response, ["Python", "JavaScript", "Java"])

    return {
        "input": "List programming languages",
        "actual": response,
        "expected": "Python, JavaScript, Java, C++, and other popular languages"
    }
```

### Test Data Management

```python
# test_data.py
class TestDataManager:
    """Centralized test data management."""

    @staticmethod
    def get_qa_pairs():
        return [
            ("What is Python?", "Python is a programming language"),
            ("What is AI?", "AI is artificial intelligence"),
        ]

    @staticmethod
    def get_sample_documents():
        return {
            "news_article": "Breaking news: AI breakthrough...",
            "technical_doc": "Implementation details for...",
            "user_manual": "Step-by-step instructions..."
        }

# test_agent.py
from test_data import TestDataManager

@agent_test(criteria=['similarity'])
def test_with_managed_data():
    """Test using centralized test data."""
    qa_pairs = TestDataManager.get_qa_pairs()
    question, expected = qa_pairs[0]

    response = my_agent(question)

    return {
        "input": question,
        "actual": response,
        "expected": expected
    }
```

## 📊 Test Organization

### File Structure

```
tests/
├── __init__.py
├── conftest.py                 # Shared test configuration
├── test_basic_functionality.py # Core feature tests
├── test_edge_cases.py          # Edge case handling
├── test_performance.py         # Performance tests
├── test_safety.py              # Safety and robustness
├── integration/                # Integration tests
│   ├── test_api_integration.py
│   └── test_workflow_integration.py
├── data/                       # Test data files
│   ├── sample_inputs.json
│   └── reference_outputs.json
└── utils/                      # Test utilities
    ├── helpers.py
    └── fixtures.py
```

### Test Categories with Tags

```python
# Core functionality
@agent_test(criteria=['similarity'], tags=['core', 'qa'])
def test_basic_qa():
    pass

# Performance tests
@agent_test(criteria=['similarity'], tags=['performance'], timeout=120)
def test_large_input_handling():
    pass

# Edge cases
@agent_test(criteria=['llm_judge'], tags=['edge_case', 'robustness'])
def test_empty_input_handling():
    pass

# Safety tests
@agent_test(criteria=['llm_judge'], tags=['safety', 'ethics'])
def test_harmful_content_filtering():
    pass
```

### Running Specific Test Categories

```bash
# Run only core functionality tests
agenttest run --tag core

# Run performance tests with longer timeout
agenttest run --tag performance

# Run multiple categories
agenttest run --tag safety --tag robustness
```

## 🔍 Debugging and Troubleshooting

### Debug Mode Testing

```python
@agent_test(criteria=['similarity'])
def test_with_debugging():
    """Test with debug information."""

    # Enable debug mode
    debug_mode = True

    if debug_mode:
        print(f"Input: {input_text}")

    response = my_agent(input_text)

    if debug_mode:
        print(f"Response: {response}")
        print(f"Response length: {len(response)}")

    return {
        "input": input_text,
        "actual": response,
        "expected": expected_response
    }
```

### Verbose Test Output

```python
@agent_test(criteria=['llm_judge'])
def test_with_detailed_output():
    """Test with detailed evaluation context."""

    response = my_agent(input_text)

    return {
        "input": input_text,
        "actual": response,
        "evaluation_criteria": ["accuracy", "clarity"],
        "context": {
            "model_version": "v2.1",
            "temperature": 0.7,
            "max_tokens": 150,
            "prompt_template": "Answer the following question..."
        }
    }
```

## 📈 Best Practices

### 1. Test Design Principles

- **Specific**: Test one capability at a time
- **Measurable**: Use clear success criteria
- **Achievable**: Set realistic thresholds
- **Relevant**: Test real-world scenarios
- **Time-bound**: Set appropriate timeouts

### 2. Data Quality

- Use diverse test cases
- Include edge cases and failure modes
- Maintain high-quality reference data
- Regular test data updates

### 3. Evaluation Strategy

- Combine multiple evaluators for robustness
- Start with objective measures (similarity, regex)
- Add subjective measures (LLM judge) for quality
- Use metrics for specific NLP tasks

### 4. Maintenance

- Regular test review and updates
- Remove obsolete tests
- Add tests for new features
- Monitor test performance over time

### 5. Documentation

- Clear test descriptions
- Document expected behavior
- Include examples and rationale
- Maintain test data documentation

## 🔗 Related Documentation

- [Evaluators](evaluators.md) - Understanding evaluation criteria
- [Configuration](configuration.md) - Test configuration options
- [CLI Commands](cli-commands.md) - Running and managing tests
- [Git Integration](git-integration.md) - Version control and comparison
