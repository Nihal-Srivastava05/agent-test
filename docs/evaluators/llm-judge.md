# LLM Judge Evaluator

The LLM Judge Evaluator uses AI models to evaluate outputs based on custom criteria like accuracy, creativity, and helpfulness. It provides human-like assessment for complex, subjective evaluation tasks.

## 🎯 Overview

The LLM Judge evaluator leverages large language models to assess agent outputs based on configurable criteria. It's ideal for:

- Subjective quality assessment
- Creative content evaluation
- Complex reasoning validation
- Multi-dimensional analysis
- Human-like judgment tasks

## ⚙️ Configuration

### Global Configuration (config.yaml)

```yaml
evaluators:
  - name: 'llm_judge'
    type: 'llm_as_judge'
    config:
      provider: 'openai' # openai, anthropic, gemini
      model: 'gpt-4' # Model to use for evaluation
      criteria: ['accuracy', 'relevance', 'clarity']
      temperature: 0.0 # Consistency in evaluation
      max_tokens: 1000 # Response length limit
    weight: 1.0
    enabled: true

# LLM provider configuration
llm:
  provider: 'openai'
  model: 'gpt-4'
  api_key: 'your-api-key' # Or use environment variable
  temperature: 0.0
```

### Environment Variables

```bash
# OpenAI
export OPENAI_API_KEY="your-openai-key"

# Anthropic
export ANTHROPIC_API_KEY="your-anthropic-key"

# Google Gemini
export GOOGLE_API_KEY="your-google-key"
export GEMINI_API_KEY="your-gemini-key"  # Alternative
```

## 🤖 Supported Providers

### OpenAI

```yaml
llm:
  provider: 'openai'
  model: 'gpt-4' # gpt-4, gpt-3.5-turbo
  api_key: '${OPENAI_API_KEY}'
```

**Recommended Models:**

- `gpt-4`: Best quality, most expensive
- `gpt-3.5-turbo`: Good balance of quality and cost

### Anthropic

```yaml
llm:
  provider: 'anthropic'
  model: 'claude-3-sonnet-20240229'
  api_key: '${ANTHROPIC_API_KEY}'
```

**Available Models:**

- `claude-3-opus-20240229`: Highest capability
- `claude-3-sonnet-20240229`: Balanced performance
- `claude-3-haiku-20240307`: Fastest, most cost-effective

### Google Gemini

```yaml
llm:
  provider: 'gemini'
  model: 'gemini-pro'
  api_key: '${GOOGLE_API_KEY}'
```

**Available Models:**

- `gemini-pro`: General purpose model
- `gemini-pro-vision`: Includes vision capabilities

## 📊 Built-in Criteria

### Standard Criteria

| Criterion      | Description            | Use Cases                   |
| -------------- | ---------------------- | --------------------------- |
| `accuracy`     | Factual correctness    | Q&A, information retrieval  |
| `relevance`    | Topic relevance        | Search, recommendations     |
| `clarity`      | Communication clarity  | Documentation, explanations |
| `creativity`   | Original thinking      | Content generation, stories |
| `helpfulness`  | Practical utility      | Instructions, advice        |
| `conciseness`  | Brevity and focus      | Summaries, abstracts        |
| `completeness` | Comprehensive coverage | Analysis, reports           |
| `coherence`    | Logical flow           | Essays, narratives          |
| `engagement`   | Reader interest        | Marketing, entertainment    |

### Domain-Specific Criteria

```python
# Custom criteria for specific domains
medical_criteria = [
    "medical_accuracy",
    "patient_safety",
    "professional_tone",
    "evidence_based"
]

legal_criteria = [
    "legal_accuracy",
    "citation_quality",
    "precedent_awareness",
    "risk_assessment"
]

technical_criteria = [
    "technical_accuracy",
    "implementation_feasibility",
    "best_practices",
    "security_considerations"
]
```

## 💡 Usage Examples

### Basic Usage

```python
@agent_test(criteria=['llm_judge'])
def test_creative_writing():
    """Test creative writing quality."""
    prompt = "Write a short story about a robot learning to paint"
    story = creative_agent(prompt)

    return {
        "input": prompt,
        "actual": story,
        "evaluation_criteria": ["creativity", "coherence", "engagement"]
    }
```

### Advanced Configuration

```python
@agent_test(criteria=['llm_judge'])
def test_technical_explanation():
    """Test technical explanation quality."""
    question = "Explain how blockchain works"
    explanation = technical_agent(question)

    return {
        "input": question,
        "actual": explanation,
        "evaluation_criteria": ["accuracy", "clarity", "completeness"],
        "llm_judge_config": {
            "provider": "anthropic",
            "model": "claude-3-sonnet-20240229",
            "temperature": 0.1,
            "custom_prompt": "Evaluate this technical explanation focusing on accuracy and beginner-friendliness."
        }
    }
```

### Multi-Dimensional Assessment

```python
@agent_test(criteria=['llm_judge'])
def test_customer_support_response():
    """Test customer support quality across multiple dimensions."""
    customer_query = "I'm having trouble with my order delivery"
    response = support_agent(customer_query)

    return {
        "input": customer_query,
        "actual": response,
        "evaluation_criteria": [
            "helpfulness",
            "empathy",
            "professionalism",
            "problem_solving",
            "clarity"
        ],
        "context": {
            "customer_tier": "premium",
            "issue_severity": "medium",
            "expected_tone": "empathetic and solution-focused"
        }
    }
```

### Comparative Evaluation

```python
@agent_test(criteria=['llm_judge'])
def test_response_comparison():
    """Compare multiple agent responses."""
    question = "What are the benefits of renewable energy?"

    response_a = agent_a(question)
    response_b = agent_b(question)

    return {
        "input": question,
        "actual": response_a,
        "alternatives": [response_b],
        "evaluation_criteria": ["accuracy", "completeness", "persuasiveness"],
        "evaluation_type": "comparative"
    }
```

## 🔧 Advanced Features

### Custom Evaluation Prompts

```python
@agent_test(criteria=['llm_judge'])
def test_with_custom_prompt():
    """Use custom evaluation prompt for specialized assessment."""

    custom_prompt = """
    Evaluate the following marketing copy for an AI product:

    Input: {input}
    Output: {actual}

    Rate on a scale of 1-10 for:
    1. Persuasiveness - How compelling is the message?
    2. Clarity - How easy is it to understand?
    3. Credibility - How trustworthy does it sound?
    4. Target Audience Fit - How well does it match the intended audience?

    Provide specific feedback and an overall score.
    """

    return {
        "input": marketing_brief,
        "actual": marketing_copy,
        "llm_judge_config": {
            "custom_prompt": custom_prompt,
            "criteria": ["persuasiveness", "clarity", "credibility", "audience_fit"]
        }
    }
```

### Context-Aware Evaluation

```python
@agent_test(criteria=['llm_judge'])
def test_context_aware_evaluation():
    """Provide context for more accurate evaluation."""

    context = {
        "user_profile": "beginner programmer",
        "task_complexity": "intermediate",
        "expected_length": "2-3 paragraphs",
        "tone": "educational and encouraging"
    }

    return {
        "input": programming_question,
        "actual": agent_explanation,
        "evaluation_criteria": ["accuracy", "beginner_friendliness", "encouragement"],
        "context": context
    }
```

### Rubric-Based Evaluation

```python
@agent_test(criteria=['llm_judge'])
def test_with_rubric():
    """Use detailed rubric for consistent evaluation."""

    rubric = {
        "accuracy": {
            "excellent": "All facts are correct and up-to-date",
            "good": "Most facts are correct with minor inaccuracies",
            "fair": "Some correct information but notable errors",
            "poor": "Significant factual errors or outdated information"
        },
        "clarity": {
            "excellent": "Crystal clear, easy to understand for target audience",
            "good": "Generally clear with minor confusing points",
            "fair": "Somewhat unclear, requires effort to understand",
            "poor": "Confusing or difficult to follow"
        }
    }

    return {
        "input": complex_query,
        "actual": agent_response,
        "evaluation_criteria": ["accuracy", "clarity"],
        "rubric": rubric
    }
```

## 📈 Best Practices

### Criteria Selection

**For Content Generation:**

```python
criteria = ["creativity", "relevance", "engagement", "originality"]
```

**For Technical Documentation:**

```python
criteria = ["accuracy", "completeness", "clarity", "usefulness"]
```

**For Customer Support:**

```python
criteria = ["helpfulness", "empathy", "professionalism", "problem_solving"]
```

**For Educational Content:**

```python
criteria = ["accuracy", "clarity", "engagement", "pedagogical_value"]
```

### Temperature Settings

- **0.0**: Maximum consistency, deterministic evaluation
- **0.1-0.3**: Slight variation while maintaining consistency
- **0.5-0.7**: More creative evaluation, good for subjective criteria
- **>0.8**: High variation, use carefully

### Cost Optimization

```python
# Use more cost-effective models for simpler evaluations
@agent_test(criteria=['llm_judge'])
def test_cost_optimized():
    return {
        "input": simple_query,
        "actual": agent_response,
        "evaluation_criteria": ["relevance"],
        "llm_judge_config": {
            "model": "gpt-3.5-turbo",  # Cheaper than gpt-4
            "max_tokens": 200          # Limit response length
        }
    }
```

### Batch Evaluation

```python
@agent_test(criteria=['llm_judge'])
def test_batch_evaluation():
    """Evaluate multiple responses efficiently."""

    test_cases = [
        {"input": q1, "actual": a1},
        {"input": q2, "actual": a2},
        {"input": q3, "actual": a3}
    ]

    return {
        "test_cases": test_cases,
        "evaluation_criteria": ["accuracy", "helpfulness"],
        "llm_judge_config": {
            "batch_mode": True,  # Process multiple cases in one call
            "temperature": 0.0
        }
    }
```

## 🔍 Result Format

The LLM Judge evaluator returns detailed results:

```python
{
    "passed": True,
    "score": 0.85,
    "threshold": 0.7,
    "details": {
        "overall_assessment": "The response demonstrates good accuracy and clarity...",
        "criteria_scores": {
            "accuracy": 0.9,
            "clarity": 0.8,
            "helpfulness": 0.85
        },
        "feedback": {
            "strengths": ["Factually correct", "Well-structured"],
            "improvements": ["Could be more concise", "Add examples"]
        },
        "reasoning": "The response accurately addresses the question..."
    },
    "metadata": {
        "model_used": "gpt-4",
        "tokens_used": 450,
        "evaluation_time": 2.3
    }
}
```

## 🚨 Troubleshooting

### Common Issues

**API Key Errors**

```bash
# Set environment variables
export OPENAI_API_KEY="your-key"
# Or configure in config.yaml
```

**Rate Limiting**

```python
# Add delays between requests
llm_judge_config = {
    "rate_limit_delay": 1.0,  # Seconds between requests
    "max_retries": 3
}
```

**Inconsistent Evaluations**

```python
# Use lower temperature for consistency
llm_judge_config = {
    "temperature": 0.0,
    "seed": 42  # For reproducible results (if supported)
}
```

**High Costs**

```python
# Optimize for cost
llm_judge_config = {
    "model": "gpt-3.5-turbo",  # Cheaper model
    "max_tokens": 300,         # Limit response length
    "batch_size": 5            # Process multiple items together
}
```

### Performance Tips

1. **Cache Results**: Store evaluation results to avoid re-evaluation
2. **Batch Processing**: Group similar evaluations together
3. **Model Selection**: Use appropriate model for task complexity
4. **Prompt Optimization**: Clear, specific prompts get better results
5. **Fallback Strategy**: Have backup evaluators for API failures
