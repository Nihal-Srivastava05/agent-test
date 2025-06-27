# NLP Metrics Evaluator

The NLP Metrics Evaluator provides standard evaluation metrics for text generation tasks including ROUGE, BLEU, and METEOR. These metrics are widely used in academic research and industry for evaluating summarization, translation, and text generation quality.

## 🎯 Overview

The metrics evaluator implements established NLP evaluation metrics for quantitative assessment of text generation quality. It's ideal for:

- Summarization quality assessment
- Translation evaluation
- Text generation benchmarking
- Academic research and comparison
- Automated quality scoring

## ⚙️ Configuration

### Global Configuration (config.yaml)

```yaml
evaluators:
  - name: 'metrics'
    type: 'nlp_metrics'
    config:
      rouge:
        variants: ['rouge1', 'rouge2', 'rougeL']
        min_score: 0.4
        use_stemmer: true
      bleu:
        n_grams: [1, 2, 3, 4]
        min_score: 0.3
        smoothing: true
      meteor:
        min_score: 0.5
        alpha: 0.9
        beta: 3.0
        gamma: 0.5
    weight: 1.0
    enabled: true
```

### Per-Test Configuration

```python
@agent_test(criteria=['metrics'])
def test_with_custom_metrics():
    return {
        "input": "Summarize this article",
        "actual": agent_summary,
        "reference": gold_standard_summary,
        "metrics": {
            "rouge": {
                "variants": ["rouge1", "rougeL"],
                "min_score": 0.4
            },
            "bleu": {
                "min_score": 0.3,
                "smoothing": True
            }
        }
    }
```

## 📊 Available Metrics

### ROUGE (Recall-Oriented Understudy for Gisting Evaluation)

ROUGE measures recall-based overlap between generated and reference texts.

#### ROUGE Variants

| Variant  | Description                         | Best For              |
| -------- | ----------------------------------- | --------------------- |
| `rouge1` | Unigram (single word) overlap       | Basic content overlap |
| `rouge2` | Bigram (two word) overlap           | Phrase-level quality  |
| `rougeL` | Longest Common Subsequence          | Sentence structure    |
| `rougeW` | Weighted Longest Common Subsequence | Word order importance |
| `rougeS` | Skip-bigram overlap                 | Non-consecutive pairs |

#### Configuration Options

```yaml
rouge:
  variants: ['rouge1', 'rouge2', 'rougeL']
  min_score: 0.4
  use_stemmer: true # Apply Porter stemming
  remove_stopwords: false # Remove common words
  alpha: 0.5 # F-score balance (precision vs recall)
```

#### Usage Example

```python
@agent_test(criteria=['metrics'])
def test_summarization_rouge():
    """Test summarization using ROUGE metrics."""
    article = "Long article text..."
    summary = summarization_agent(article)
    reference = "Gold standard summary..."

    return {
        "input": article,
        "actual": summary,
        "reference": reference,
        "metrics": {
            "rouge": {
                "variants": ["rouge1", "rouge2", "rougeL"],
                "min_score": 0.4
            }
        }
    }
```

### BLEU (Bilingual Evaluation Understudy)

BLEU measures precision-based n-gram overlap, originally designed for machine translation.

#### Configuration Options

```yaml
bleu:
  n_grams: [1, 2, 3, 4] # N-gram levels to evaluate
  min_score: 0.3
  smoothing: true # Apply smoothing for short texts
  auto_reweigh: true # Automatically adjust weights
  weights: [0.25, 0.25, 0.25, 0.25] # Custom n-gram weights
```

#### Usage Example

```python
@agent_test(criteria=['metrics'])
def test_translation_bleu():
    """Test translation quality using BLEU."""
    source = "Hello, how are you today?"
    translation = translation_agent(source, target_lang="es")
    reference = "Hola, ¿cómo estás hoy?"

    return {
        "input": source,
        "actual": translation,
        "reference": reference,
        "metrics": {
            "bleu": {
                "n_grams": [1, 2, 3, 4],
                "min_score": 0.3,
                "smoothing": True
            }
        }
    }
```

### METEOR (Metric for Evaluation of Translation with Explicit ORdering)

METEOR considers word order, synonyms, and paraphrases for more sophisticated evaluation.

#### Configuration Options

```yaml
meteor:
  min_score: 0.5
  alpha: 0.9 # Precision-recall balance
  beta: 3.0 # Fragmentation penalty weight
  gamma: 0.5 # Fragmentation penalty exponent
  wordnet: true # Use WordNet for synonyms
```

#### Usage Example

```python
@agent_test(criteria=['metrics'])
def test_paraphrasing_meteor():
    """Test paraphrasing quality using METEOR."""
    original = "The quick brown fox jumps over the lazy dog"
    paraphrase = paraphrasing_agent(original)

    return {
        "input": original,
        "actual": paraphrase,
        "reference": original,
        "metrics": {
            "meteor": {
                "min_score": 0.5,
                "alpha": 0.9
            }
        }
    }
```

## 💡 Advanced Usage

### Multi-Reference Evaluation

```python
@agent_test(criteria=['metrics'])
def test_multi_reference():
    """Evaluate against multiple reference texts."""

    references = [
        "First reference summary...",
        "Second reference summary...",
        "Third reference summary..."
    ]

    return {
        "input": source_text,
        "actual": agent_summary,
        "references": references,  # Multiple references
        "metrics": {
            "rouge": {
                "variants": ["rouge1", "rougeL"],
                "min_score": 0.4
            }
        }
    }
```

### Comparative Evaluation

```python
@agent_test(criteria=['metrics'])
def test_model_comparison():
    """Compare multiple models using metrics."""

    summary_a = model_a.summarize(article)
    summary_b = model_b.summarize(article)

    return {
        "input": article,
        "actual": summary_a,
        "alternatives": [summary_b],
        "reference": gold_summary,
        "metrics": {
            "rouge": {"variants": ["rouge1", "rouge2", "rougeL"]},
            "bleu": {"n_grams": [1, 2, 3, 4]},
            "meteor": {"min_score": 0.5}
        }
    }
```

### Domain-Specific Configuration

```python
@agent_test(criteria=['metrics'])
def test_domain_specific():
    """Configure metrics for specific domains."""

    # For technical documentation
    if domain == "technical":
        config = {
            "rouge": {
                "variants": ["rouge1", "rougeL"],
                "min_score": 0.6,  # Higher threshold for technical accuracy
                "use_stemmer": False  # Preserve technical terms
            }
        }

    # For creative writing
    elif domain == "creative":
        config = {
            "meteor": {
                "min_score": 0.4,  # Lower threshold for creativity
                "alpha": 0.8,      # Favor recall over precision
                "wordnet": True    # Consider synonyms
            }
        }

    return {
        "input": prompt,
        "actual": agent_output,
        "reference": reference_output,
        "metrics": config
    }
```

### Batch Evaluation

```python
@agent_test(criteria=['metrics'])
def test_batch_metrics():
    """Evaluate multiple text pairs efficiently."""

    test_pairs = [
        {"actual": summary1, "reference": ref1},
        {"actual": summary2, "reference": ref2},
        {"actual": summary3, "reference": ref3}
    ]

    return {
        "test_cases": test_pairs,
        "metrics": {
            "rouge": {"variants": ["rouge1", "rougeL"]},
            "bleu": {"n_grams": [1, 2, 3, 4]}
        }
    }
```

## 📈 Metric Selection Guide

### By Task Type

| Task Type          | Recommended Metrics | Configuration             |
| ------------------ | ------------------- | ------------------------- |
| Summarization      | ROUGE-1, ROUGE-L    | High recall focus         |
| Translation        | BLEU, METEOR        | Precision and fluency     |
| Paraphrasing       | METEOR, ROUGE-L     | Synonym awareness         |
| Question Answering | ROUGE-1, BLEU-1     | Exact match and overlap   |
| Content Generation | METEOR, ROUGE-2     | Creativity with coherence |

### By Evaluation Focus

| Focus Area          | Primary Metric | Secondary Metrics |
| ------------------- | -------------- | ----------------- |
| Content Overlap     | ROUGE-1        | ROUGE-2, BLEU-1   |
| Phrase Quality      | ROUGE-2        | BLEU-2, BLEU-3    |
| Structure           | ROUGE-L        | METEOR            |
| Fluency             | BLEU           | METEOR            |
| Semantic Similarity | METEOR         | ROUGE-L           |

## 🔍 Result Format

The metrics evaluator returns detailed scores:

```python
{
    "passed": True,
    "score": 0.65,  # Overall combined score
    "threshold": 0.4,
    "details": {
        "rouge": {
            "rouge1": {
                "precision": 0.72,
                "recall": 0.68,
                "f1": 0.70
            },
            "rouge2": {
                "precision": 0.65,
                "recall": 0.61,
                "f1": 0.63
            },
            "rougeL": {
                "precision": 0.69,
                "recall": 0.64,
                "f1": 0.66
            }
        },
        "bleu": {
            "bleu1": 0.68,
            "bleu2": 0.45,
            "bleu3": 0.32,
            "bleu4": 0.24,
            "overall": 0.42
        },
        "meteor": {
            "score": 0.58,
            "precision": 0.72,
            "recall": 0.49,
            "fragmentation": 0.23
        }
    }
}
```

## 📋 Best Practices

### Threshold Selection

**Conservative (High Quality)**

```python
thresholds = {
    "rouge1": 0.6,
    "rouge2": 0.4,
    "rougeL": 0.5,
    "bleu": 0.4,
    "meteor": 0.6
}
```

**Moderate (Balanced)**

```python
thresholds = {
    "rouge1": 0.4,
    "rouge2": 0.2,
    "rougeL": 0.3,
    "bleu": 0.2,
    "meteor": 0.4
}
```

**Permissive (High Recall)**

```python
thresholds = {
    "rouge1": 0.3,
    "rouge2": 0.1,
    "rougeL": 0.2,
    "bleu": 0.1,
    "meteor": 0.3
}
```

### Preprocessing Recommendations

```python
def preprocess_for_metrics(text):
    """Recommended preprocessing for metric evaluation."""
    import re

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text.strip())

    # Lowercase for case-insensitive comparison
    text = text.lower()

    # Remove extra punctuation (optional)
    text = re.sub(r'[^\w\s\.]', '', text)

    return text

@agent_test(criteria=['metrics'])
def test_with_preprocessing():
    actual_clean = preprocess_for_metrics(agent_output)
    reference_clean = preprocess_for_metrics(reference_text)

    return {
        "input": prompt,
        "actual": actual_clean,
        "reference": reference_clean,
        "metrics": {"rouge": {"variants": ["rouge1", "rougeL"]}}
    }
```

### Combining with Other Evaluators

```python
@agent_test(criteria=['metrics', 'similarity', 'llm_judge'])
def test_comprehensive_evaluation():
    """Combine metrics with other evaluators for complete assessment."""

    return {
        "input": prompt,
        "actual": agent_output,
        "expected": reference_output,  # For similarity
        "reference": reference_output,  # For metrics
        "evaluation_criteria": ["coherence", "fluency"],  # For LLM judge
        "metrics": {
            "rouge": {"variants": ["rouge1", "rougeL"]},
            "meteor": {"min_score": 0.4}
        }
    }
```

## 🚨 Troubleshooting

### Common Issues

**Low ROUGE Scores**

- Check for text preprocessing differences
- Verify reference quality and relevance
- Consider using ROUGE-L for structural similarity
- Adjust stemming and stopword settings

**BLEU Score Issues**

- Ensure adequate text length (BLEU requires sufficient n-grams)
- Enable smoothing for short texts
- Check for exact match requirements
- Consider alternative metrics for creative tasks

**METEOR Installation**

- Requires NLTK data: `nltk.download('wordnet')`
- May need Java runtime for full functionality
- Consider simplified configuration if installation fails

### Performance Optimization

```python
# Cache preprocessing results
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_preprocess(text):
    return preprocess_for_metrics(text)

# Batch processing for efficiency
@agent_test(criteria=['metrics'])
def test_batch_optimized():
    return {
        "test_cases": large_test_set,
        "metrics": {
            "rouge": {"variants": ["rouge1"]},  # Limit variants for speed
            "batch_size": 50  # Process in batches
        }
    }
```
