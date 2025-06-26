# AgentTest Documentation

**A pytest-like testing framework for AI agents and prompts**

AgentTest is a comprehensive testing framework designed specifically for AI agents, providing evaluation, logging, and regression tracking capabilities similar to pytest but tailored for AI/ML applications.

## 📚 Documentation Index

### Getting Started

- [Installation & Setup](installation.md) - How to install and configure AgentTest
- [Quick Start Guide](quickstart.md) - Your first test in 5 minutes
- [Configuration](configuration.md) - Complete configuration reference

### Core Concepts

- [Writing Tests](writing-tests.md) - How to structure and write agent tests
- [Evaluators](evaluators.md) - Understanding evaluation metrics and criteria
- [Test Execution](test-execution.md) - Running tests and interpreting results

### Advanced Features

- [Git Integration](git-integration.md) - Version tracking and comparison features
- [Logging & Debugging](logging.md) - Enhanced logging and debugging capabilities
- [CLI Commands](cli-commands.md) - Complete command-line interface reference

### Evaluator Reference

- [String Similarity](evaluators/similarity.md) - Text similarity evaluation
- [LLM Judge](evaluators/llm-judge.md) - AI-powered evaluation
- [NLP Metrics](evaluators/metrics.md) - ROUGE, BLEU, METEOR metrics
- [Pattern Matching](evaluators/patterns.md) - Regex and contains evaluators
- [Custom Evaluators](evaluators/custom.md) - Building your own evaluators

### Examples & Tutorials

- [Basic Examples](examples/basic.md) - Simple test cases
- [Advanced Scenarios](examples/advanced.md) - Complex evaluation patterns
- [Best Practices](examples/best-practices.md) - Testing strategies and patterns

### API Reference

- [Core API](api/core.md) - Core classes and functions
- [Decorators](api/decorators.md) - Test decoration and configuration
- [Results](api/results.md) - Test results and reporting

## 🚀 Key Features

- **pytest-like Syntax**: Familiar testing patterns for AI agents
- **Multiple Evaluators**: String similarity, LLM judges, NLP metrics, pattern matching
- **Git Integration**: Track performance across commits with detailed comparisons
- **Rich CLI**: Comprehensive command-line interface with filtering and export options
- **Enhanced Logging**: Detailed debugging and structured logging
- **Flexible Configuration**: YAML-based configuration with environment variable support
- **Multiple LLM Providers**: OpenAI, Anthropic, Google Gemini support

## 🏃‍♂️ Quick Example

```python
from agent_test import agent_test

@agent_test(criteria=['similarity', 'llm_judge'])
def test_summarization_quality():
    """Test if the agent can summarize text effectively."""
    return {
        "input": "Write a summary of the latest AI developments...",
        "actual": agent_response,
        "expected": "A concise summary highlighting key points...",
        "evaluation_criteria": ["accuracy", "conciseness", "relevance"]
    }
```

```bash
# Run tests with enhanced output
agenttest run --verbose --detailed

# Compare performance across git commits
agenttest compare abc123 HEAD --metric similarity --detailed

# Generate test reports
agenttest run --export results.json --log-output debug.log
```

## 🛠️ Installation

```bash
# Basic installation
pip install agenttest

# With optional dependencies
pip install agenttest[langchain,llamaindex]

# Development installation
pip install agenttest[dev,all]
```

## 🔗 Links

- **Repository**: [GitHub](https://github.com/agenttest-ai/agenttest)
- **Issues**: [Bug Reports & Feature Requests](https://github.com/agenttest-ai/agenttest/issues)
- **Examples**: [Sample Projects](https://github.com/agenttest-ai/agenttest/tree/main/examples)

---

_Need help? Check out our [Quick Start Guide](quickstart.md) or browse the [Examples](examples/basic.md)!_
