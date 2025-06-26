# Evaluators Overview

Evaluators are the core components that assess the quality of your AI agent's outputs. AgentTest provides multiple built-in evaluators and supports custom evaluators for specialized use cases.

## 🧪 Available Evaluators

| Evaluator                               | Purpose                    | Best For                      | Key Parameters          |
| --------------------------------------- | -------------------------- | ----------------------------- | ----------------------- |
| **[Similarity](#similarity-evaluator)** | Text similarity comparison | Content quality, paraphrasing | `method`, `threshold`   |
| **[LLM Judge](#llm-judge-evaluator)**   | AI-powered evaluation      | Complex reasoning, creativity | `criteria`, `provider`  |
| **[Metrics](#metrics-evaluator)**       | NLP metrics (ROUGE, BLEU)  | Summarization, translation    | `variants`, `min_score` |
| **[Contains](#contains-evaluator)**     | Required content checking  | Keyword presence, facts       | `contains`              |
| **[Regex](#regex-evaluator)**           | Pattern matching           | Structured data, formats      | `patterns`              |

## 📊 Similarity Evaluator

Measures text similarity between actual and expected outputs using various algorithms.

### Configuration

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

### Methods

| Method        | Description                   | Use Case                  | Range  |
| ------------- | ----------------------------- | ------------------------- | ------ |
| `cosine`      | Cosine similarity with TF-IDF | General text similarity   | 0-1    |
| `levenshtein` | Edit distance based           | Exact matching with typos | 0-1    |
| `jaccard`     | Set intersection/union        | Keyword similarity        | 0-1    |
| `exact`       | Exact string match            | Precise outputs           | 0 or 1 |

### Usage Example

```python
@agent_test(criteria=['similarity'])
def test_paraphrasing():
    return {
        "input": "Explain photosynthesis",
        "actual": "Plants convert sunlight into energy through photosynthesis.",
        "expected": "Photosynthesis is how plants use sunlight to create energy."
    }
```

### Advanced Configuration

```python
# Per-test configuration
@agent_test(criteria=['similarity'])
def test_with_custom_threshold():
    return {
        "input": "Question",
        "actual": "Answer",
        "expected": "Expected answer",
        "similarity_config": {
            "method": "levenshtein",
            "threshold": 0.9
        }
    }
```

## 🤖 LLM Judge Evaluator

Uses AI models to evaluate outputs based on custom criteria like accuracy, creativity, and helpfulness.

### Configuration

```yaml
evaluators:
  - name: 'llm_judge'
    type: 'llm_as_judge'
    config:
      provider: 'openai' # openai, anthropic, gemini
      model: 'gpt-4'
      criteria: ['accuracy', 'relevance', 'clarity']
      temperature: 0.0
    weight: 1.0
    enabled: true
```

### Built-in Criteria

| Criterion      | Description            | Evaluation Focus          |
| -------------- | ---------------------- | ------------------------- |
| `accuracy`     | Factual correctness    | Truth, facts, precision   |
| `relevance`    | Topic relevance        | Context appropriateness   |
| `clarity`      | Communication clarity  | Understandability         |
| `creativity`   | Original thinking      | Innovation, uniqueness    |
| `helpfulness`  | Practical utility      | Usefulness, actionability |
| `conciseness`  | Brevity                | Information density       |
| `completeness` | Comprehensive coverage | Thoroughness              |

### Usage Example

```python
@agent_test(criteria=['llm_judge'])
def test_creative_writing():
    return {
        "input": "Write a story about a robot",
        "actual": agent_story,
        "evaluation_criteria": ["creativity", "coherence", "engagement"]
    }
```

### Custom Criteria

```python
@agent_test(criteria=['llm_judge'])
def test_medical_advice():
    return {
        "input": "Explain diabetes symptoms",
        "actual": medical_response,
        "evaluation_criteria": [
            "medical_accuracy",
            "patient_safety",
            "professional_tone"
        ]
    }
```

## 📈 Metrics Evaluator

Provides standard NLP evaluation metrics for text generation tasks.

### Configuration

```yaml
evaluators:
  - name: 'metrics'
    type: 'nlp_metrics'
    config:
      rouge:
        variants: ['rouge1', 'rouge2', 'rougeL']
        min_score: 0.4
      bleu:
        n_grams: [1, 2, 3, 4]
        min_score: 0.3
      meteor:
        min_score: 0.5
    weight: 1.0
    enabled: true
```

### Available Metrics

#### ROUGE (Recall-Oriented Understudy for Gisting Evaluation)

- `rouge1`: Unigram overlap
- `rouge2`: Bigram overlap
- `rougeL`: Longest common subsequence

#### BLEU (Bilingual Evaluation Understudy)

- N-gram precision evaluation
- Standard for translation quality

#### METEOR (Metric for Evaluation of Translation with Explicit ORdering)

- Harmonic mean of precision and recall
- Considers word order and synonyms

### Usage Example

```python
@agent_test(criteria=['metrics'])
def test_summarization():
    return {
        "input": "Long article text...",
        "actual": generated_summary,
        "reference": "Gold standard summary...",
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

## 🔍 Contains Evaluator

Checks if the output contains required words, phrases, or concepts.

### Configuration

```yaml
evaluators:
  - name: 'contains'
    type: 'contains_check'
    config:
      case_sensitive: false
      partial_match: true
    weight: 1.0
    enabled: true
```

### Usage Example

```python
@agent_test(criteria=['contains'])
def test_required_information():
    return {
        "input": "List Python data types",
        "actual": "Python has int, float, str, list, dict, tuple types...",
        "contains": ["int", "float", "str", "list", "dict"]
    }
```

### Advanced Usage

```python
@agent_test(criteria=['contains'])
def test_with_phrases():
    return {
        "input": "Explain machine learning",
        "actual": ml_explanation,
        "contains": [
            "machine learning",
            "algorithms",
            "data patterns",
            "predictive models"
        ]
    }
```

## 🔤 Regex Evaluator

Uses regular expressions to validate structured content and formats.

### Configuration

```yaml
evaluators:
  - name: 'regex'
    type: 'regex_pattern'
    config:
      flags: ['IGNORECASE']
    weight: 1.0
    enabled: true
```

### Usage Example

```python
@agent_test(criteria=['regex'])
def test_contact_extraction():
    return {
        "input": "Extract contact info from this text",
        "actual": extracted_contacts,
        "patterns": [
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # Email
            r"\b\d{3}-\d{3}-\d{4}\b",                                 # Phone
            r"\b\d{4}-\d{2}-\d{2}\b"                                  # Date
        ]
    }
```

### Common Patterns

```python
# Useful regex patterns
patterns = {
    "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
    "phone": r"\b\d{3}-\d{3}-\d{4}\b",
    "date": r"\b\d{4}-\d{2}-\d{2}\b",
    "currency": r"\$\d+\.\d{2}",
    "url": r"https?://[^\s]+",
    "zipcode": r"\b\d{5}(-\d{4})?\b",
    "ssn": r"\b\d{3}-\d{2}-\d{4}\b"
}
```

## 🔧 Combining Evaluators

You can use multiple evaluators for comprehensive testing:

```python
@agent_test(criteria=['similarity', 'contains', 'llm_judge', 'regex'])
def test_comprehensive_evaluation():
    return {
        "input": "Generate a product description",
        "actual": generated_description,
        "expected": "Reference product description...",
        "contains": ["features", "benefits", "price"],
        "patterns": [r"\$\d+\.\d{2}"],  # Price format
        "evaluation_criteria": ["persuasiveness", "clarity"]
    }
```

## ⚙️ Evaluator Weights

Configure how much each evaluator contributes to the final score:

```yaml
evaluators:
  - name: 'similarity'
    weight: 0.4 # 40% of total score
  - name: 'llm_judge'
    weight: 0.6 # 60% of total score
```

## 🎯 Threshold Configuration

Set pass/fail thresholds for each evaluator:

```yaml
evaluators:
  - name: 'similarity'
    config:
      threshold: 0.8 # Must score >= 0.8 to pass
  - name: 'llm_judge'
    config:
      threshold: 0.7 # Must score >= 0.7 to pass
```

## 📊 Evaluation Results

Each evaluator returns structured results:

```json
{
  "passed": true,
  "score": 0.85,
  "threshold": 0.8,
  "details": {
    "method": "cosine",
    "similarity": 0.85,
    "actual": "Agent response...",
    "expected": "Expected response..."
  }
}
```

## 🚀 Best Practices

### 1. Choose Appropriate Evaluators

- **Similarity**: For paraphrasing, content quality
- **LLM Judge**: For subjective quality, creativity
- **Metrics**: For summarization, translation
- **Contains**: For required facts, keywords
- **Regex**: For structured data, formats

### 2. Set Realistic Thresholds

- Start with lower thresholds (0.6-0.7)
- Gradually increase as you improve
- Different tasks need different standards

### 3. Use Multiple Evaluators

- Combine objective and subjective measures
- Cross-validate with different approaches
- Balance precision with coverage

### 4. Monitor Performance

- Track scores over time
- Use git integration for regression testing
- Analyze which evaluators are most predictive

## 🔗 Related Documentation

- [Configuration](configuration.md) - Evaluator configuration details
- [Writing Tests](writing-tests.md) - Test structure and patterns
- Custom Evaluators - Building your own evaluators (coming soon)
- [CLI Commands](cli-commands.md) - Running tests with specific evaluators
