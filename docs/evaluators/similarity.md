# Similarity Evaluator

The Similarity Evaluator measures text similarity between actual and expected outputs using various algorithms. It's the default evaluator and most commonly used for content quality assessment.

## 🎯 Overview

The similarity evaluator compares your agent's output against expected results using configurable similarity algorithms. It's ideal for:

- Content quality assessment
- Paraphrasing validation
- Translation quality
- Text generation evaluation

## ⚙️ Configuration

### Global Configuration (config.yaml)

```yaml
evaluators:
  - name: 'similarity'
    type: 'string_similarity'
    config:
      method: 'cosine' # cosine, levenshtein, jaccard, exact
      threshold: 0.8 # Pass threshold (0-1)
    weight: 1.0
    enabled: true
```

### Per-Test Configuration

```python
@agent_test(criteria=['similarity'])
def test_with_custom_config():
    return {
        "input": "Test input",
        "actual": "Agent response",
        "expected": "Expected response",
        "similarity_config": {
            "method": "levenshtein",
            "threshold": 0.9
        }
    }
```

## 📊 Similarity Methods

### Cosine Similarity (Default)

**Best for:** General text similarity, semantic comparison

```python
config:
  method: 'cosine'
  threshold: 0.8
```

- Uses TF-IDF vectorization
- Range: 0.0 to 1.0
- Good for semantic similarity
- Handles different text lengths well

**Example:**

```python
@agent_test(criteria=['similarity'])
def test_semantic_similarity():
    return {
        "input": "What is machine learning?",
        "actual": "ML is a subset of AI that enables computers to learn from data",
        "expected": "Machine learning allows computers to learn patterns from data automatically"
        # Cosine similarity: ~0.85 (high semantic similarity despite different wording)
    }
```

### Levenshtein Distance

**Best for:** Exact matching with tolerance for typos

```python
config:
  method: 'levenshtein'
  threshold: 0.9
```

- Edit distance based
- Range: 0.0 to 1.0
- Good for exact matches with minor variations
- Sensitive to character-level changes

**Example:**

```python
@agent_test(criteria=['similarity'])
def test_exact_format():
    return {
        "input": "Format as JSON",
        "actual": '{"name": "John", "age": 30}',
        "expected": '{"name": "John", "age": 30}',
        "similarity_config": {"method": "levenshtein", "threshold": 0.95}
        # Levenshtein: 1.0 (exact match)
    }
```

### Jaccard Similarity

**Best for:** Keyword similarity, set-based comparison

```python
config:
  method: 'jaccard'
  threshold: 0.7
```

- Set intersection over union
- Range: 0.0 to 1.0
- Good for keyword presence
- Order-independent

**Example:**

```python
@agent_test(criteria=['similarity'])
def test_keyword_coverage():
    return {
        "input": "List programming languages",
        "actual": "Python, Java, JavaScript, C++, Go",
        "expected": "JavaScript, Python, Java, C++, Rust",
        "similarity_config": {"method": "jaccard", "threshold": 0.6}
        # Jaccard: 0.8 (4 common out of 5 total unique)
    }
```

### Exact Match

**Best for:** Precise output validation

```python
config:
  method: 'exact'
  threshold: 1.0
```

- Exact string comparison
- Range: 0.0 or 1.0 only
- Case-sensitive
- No tolerance for differences

**Example:**

```python
@agent_test(criteria=['similarity'])
def test_exact_output():
    return {
        "input": "Return exactly: 'SUCCESS'",
        "actual": "SUCCESS",
        "expected": "SUCCESS",
        "similarity_config": {"method": "exact"}
        # Exact: 1.0 (perfect match)
    }
```

## 📈 Advanced Usage

### Multiple Test Cases

```python
@agent_test(criteria=['similarity'])
def test_batch_evaluation():
    test_cases = [
        {
            "input": "Question 1",
            "actual": "Answer 1",
            "expected": "Expected 1"
        },
        {
            "input": "Question 2",
            "actual": "Answer 2",
            "expected": "Expected 2"
        }
    ]

    return {"test_cases": test_cases}
```

### Dynamic Threshold Adjustment

```python
@agent_test(criteria=['similarity'])
def test_adaptive_threshold():
    difficulty = "high"  # Based on input complexity
    threshold = 0.9 if difficulty == "easy" else 0.7

    return {
        "input": complex_prompt,
        "actual": agent_response,
        "expected": reference_response,
        "similarity_config": {
            "method": "cosine",
            "threshold": threshold
        }
    }
```

### Preprocessing Options

```python
@agent_test(criteria=['similarity'])
def test_with_preprocessing():
    import re

    def clean_text(text):
        # Remove extra whitespace and normalize
        return re.sub(r'\s+', ' ', text.strip().lower())

    actual_cleaned = clean_text(agent_response)
    expected_cleaned = clean_text(reference_response)

    return {
        "input": prompt,
        "actual": actual_cleaned,
        "expected": expected_cleaned
    }
```

## 📋 Best Practices

### Method Selection Guide

| Use Case            | Recommended Method | Threshold Range |
| ------------------- | ------------------ | --------------- |
| Semantic similarity | `cosine`           | 0.7 - 0.9       |
| Exact formatting    | `levenshtein`      | 0.9 - 1.0       |
| Keyword presence    | `jaccard`          | 0.6 - 0.8       |
| Precise validation  | `exact`            | 1.0             |

### Threshold Guidelines

- **0.9-1.0**: Very strict, near-exact matching
- **0.8-0.9**: High similarity, good paraphrasing
- **0.7-0.8**: Moderate similarity, semantic equivalence
- **0.6-0.7**: Loose similarity, general topic match
- **<0.6**: Very permissive, basic relevance

### Common Patterns

#### Content Generation

```python
@agent_test(criteria=['similarity'])
def test_content_generation():
    return {
        "input": "Write about renewable energy",
        "actual": agent_content,
        "expected": reference_content,
        "similarity_config": {
            "method": "cosine",
            "threshold": 0.75  # Allow creative variation
        }
    }
```

#### Translation Quality

```python
@agent_test(criteria=['similarity'])
def test_translation():
    return {
        "input": "Translate: 'Hello world'",
        "actual": agent_translation,
        "expected": "Hola mundo",
        "similarity_config": {
            "method": "levenshtein",
            "threshold": 0.9  # High accuracy for translation
        }
    }
```

#### Code Generation

```python
@agent_test(criteria=['similarity'])
def test_code_generation():
    return {
        "input": "Write a Python function to sort a list",
        "actual": agent_code,
        "expected": reference_code,
        "similarity_config": {
            "method": "jaccard",
            "threshold": 0.8  # Focus on keyword/structure similarity
        }
    }
```

## 🔧 Troubleshooting

### Common Issues

**Low Similarity Scores**

- Check if method matches your use case
- Adjust threshold based on expected variation
- Consider preprocessing to normalize text
- Use multiple evaluators for comprehensive assessment

**Inconsistent Results**

- Ensure consistent text formatting
- Remove or normalize special characters
- Consider case sensitivity
- Check for encoding issues

**Performance Issues**

- Cosine similarity is fastest for long texts
- Levenshtein can be slow for very long strings
- Consider text length limits for batch processing

### Debug Information

The similarity evaluator provides detailed debug information:

```python
# Result details include:
{
    "passed": True,
    "score": 0.85,
    "threshold": 0.8,
    "details": {
        "actual": "Agent response",
        "expected": "Expected response",
        "similarity": 0.85,
        "method": "cosine"
    }
}
```

## 📚 Examples

See [Basic Examples](../examples/basic.md#similarity-evaluator-examples) for more similarity evaluator usage patterns.
