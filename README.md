# AgentTest 🧪

> A pytest-like testing framework for AI agents and prompts

[![PyPI version](https://badge.fury.io/py/agenttest.svg)](https://badge.fury.io/py/agenttest)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

AgentTest is a comprehensive testing framework designed specifically for AI agents, providing evaluation, logging, and regression tracking capabilities with a pytest-like interface.

## 🚀 Key Features

- **🤖 Intelligent Auto Test Generation**: Automatically analyze your code and generate comprehensive test cases with proper imports and function calls
- **🧪 Pytest-like Interface**: Familiar CLI and decorator-based testing
- **🧠 Smart Code Analysis**: Understands project structure, classes, functions, and generates realistic test data
- **📊 Multiple Evaluation Engines**: String similarity, LLM-as-judge, regex, and more
- **🔄 Git-Aware Logging**: Track test results with commit information for regression analysis
- **🔗 Framework Agnostic**: Works with LangChain, LlamaIndex, OpenAI, Anthropic, and custom agents
- **📈 Regression Tracking**: Compare test results across commits and branches
- **⚡ CI/CD Integration**: Built for continuous integration workflows

## 📦 Installation

```bash
# Basic installation
pip install agenttest
```

## 🏁 Quick Start

### 1. Initialize a New Project

```bash
# Initialize in current directory
agenttest init

# Or use a framework template
agenttest init --template langchain
agenttest init --template llamaindex
```

### 2. Write Your First Test

Create `tests/test_my_agent.py`:

```python
from agenttest import agent_test

def simple_agent(input_text: str) -> str:
    """A simple agent that echoes the input with a prefix."""
    return f"Agent response: {input_text}"

@agent_test(criteria=["similarity", "llm_judge"])
def test_simple_agent():
    """Test the simple agent with basic input."""
    input_text = "Hello, world!"
    expected = "Agent response: Hello, world!"

    actual = simple_agent(input_text)

    return {
        "input": input_text,
        "expected": expected,
        "actual": actual
    }

@agent_test(criteria=["llm_judge"], tags=["edge_case"])
def test_empty_input():
    """Test agent with empty input."""
    actual = simple_agent("")

    return {
        "input": "",
        "actual": actual,
        "evaluation_criteria": {
            "robustness": "Agent should handle empty input gracefully"
        }
    }
```

### 3. Run Tests

```bash
# Run all tests
agenttest run

# Run with verbose output
agenttest run --verbose

# Run specific tests by tag
agenttest run --tag edge_case

# Run in CI mode (exit with error on failures)
agenttest run --ci
```

### 4. Generate Tests Automatically ✨

AgentTest can automatically analyze your code and generate comprehensive test cases:

```bash
# Auto-generate tests for a specific file
agenttest generate examples/agents_sample.py --count 5

# Generate tests with specific format
agenttest generate examples/agents_sample.py --format python --count 3

# Generate tests for multiple files
agenttest generate examples/*.py --count 2

# Save generated tests to a file
agenttest generate agents/my_agent.py --output tests/generated_tests.py
```

**What makes it intelligent?**

- 🔍 **Analyzes project structure** to generate correct imports
- 🎯 **Understands functions and classes** to create proper test calls
- 📝 **Generates realistic test data** based on parameter names and types
- 🧪 **Creates multiple test scenarios** (basic, edge cases, error handling)
- 🏗️ **Handles class instantiation** automatically for method testing

**Example generated test:**

```python
@agent_test(
    criteria=["execution", "output_type", "functionality"],
    tags=["basic", "function"]
)
def test_handle_customer_query_basic():
    """Test basic functionality of handle_customer_query"""
    input_data = {
        "query": "test query",
        "customer_type": "premium",
        "urgency": "high"
    }

    # Automatically generated function call
    actual = handle_customer_query(**input_data)

    return {
        "input": input_data,
        "actual": actual,
        "evaluation_criteria": {
            "execution": "Function should execute without errors",
            "output_type": "Should return appropriate type"
        }
    }
```

### 5. View Test History

```bash
# Show recent test runs
agenttest log

# Show runs for specific commit
agenttest log --commit abc123

# Compare results between commits
agenttest compare HEAD~1 HEAD
```

## 📖 Detailed Usage

### Test Decorators

The `@agent_test` decorator supports various options:

```python
@agent_test(
    criteria=["similarity", "llm_judge", "regex"],  # Evaluation methods
    tags=["integration", "slow"],                   # Test categorization
    timeout=30,                                     # Test timeout in seconds
    retry_count=2                                   # Retries on failure
)
def test_complex_agent():
    # Your test logic here
    pass
```

### Evaluation Criteria

AgentTest supports multiple built-in evaluators:

#### String Similarity

```python
@agent_test(criteria=["similarity"])
def test_with_similarity():
    return {
        "input": "What is AI?",
        "expected": "Artificial Intelligence is...",
        "actual": agent_response
    }
```

#### LLM-as-Judge

```python
@agent_test(criteria=["llm_judge"])
def test_with_llm_judge():
    return {
        "input": "Summarize this article",
        "actual": agent_response,
        "evaluation_criteria": {
            "accuracy": "Summary should capture key points",
            "conciseness": "Should be 2-3 sentences"
        }
    }
```

#### Custom Evaluators

```python
@agent_test(criteria=["regex"])
def test_with_regex():
    return {
        "input": "Generate a phone number",
        "actual": agent_response,
        "pattern": r"\d{3}-\d{3}-\d{4}"  # Phone number pattern
    }
```

### Configuration

Edit `.agenttest/config.yaml` to customize your setup:

```yaml
version: '1.0'
project_name: 'My AI Project'

llm:
  provider: 'openai' # or "anthropic" or "gemini"
  model: 'gpt-3.5-turbo' # or 'claude-3-sonnet-20240229' or 'gemini-pro'
  temperature: 0.0

evaluators:
  - name: 'similarity'
    type: 'string_similarity'
    config:
      method: 'cosine'
      threshold: 0.8

  - name: 'llm_judge'
    type: 'llm_as_judge'
    config:
      criteria: ['accuracy', 'relevance']

testing:
  test_dirs: ['tests']
  test_patterns: ['test_*.py', '*_test.py']
  parallel: false
  timeout: 300

logging:
  level: 'INFO'
  git_aware: true
  results_dir: '.agenttest/results'
```

### Framework Integration

#### LangChain Example

```python
from agenttest import agent_test
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

# Your LangChain agent
def create_summarizer():
    llm = OpenAI(temperature=0)
    prompt = PromptTemplate(
        input_variables=["text"],
        template="Summarize: {text}"
    )
    return LLMChain(llm=llm, prompt=prompt)

@agent_test(criteria=["llm_judge"])
def test_langchain_summarizer():
    chain = create_summarizer()
    text = "Long article content..."
    result = chain.run(text=text)

    return {
        "input": text,
        "actual": result,
        "evaluation_criteria": {
            "conciseness": "Summary should be brief",
            "accuracy": "Should capture main points"
        }
    }
```

#### Custom Agent Example

```python
import openai
from agenttest import agent_test

class CustomAgent:
    def __init__(self):
        self.client = openai.OpenAI()

    def process(self, query: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": query}]
        )
        return response.choices[0].message.content

# Gemini Agent Example
import google.generativeai as genai

class GeminiAgent:
    def __init__(self):
        genai.configure(api_key="your-google-api-key")
        self.model = genai.GenerativeModel('gemini-pro')

    def process(self, query: str) -> str:
        response = self.model.generate_content(query)
        return response.text

@agent_test(criteria=["similarity", "llm_judge"])
def test_custom_agent():
    agent = CustomAgent()
    query = "What is the capital of France?"
    result = agent.process(query)

    return {
        "input": query,
        "actual": result,
        "expected": "Paris",
        "evaluation_criteria": {
            "factuality": "Answer should be factually correct"
        }
    }

@agent_test(criteria=["llm_judge"])
def test_gemini_agent():
    agent = GeminiAgent()
    query = "Explain photosynthesis in simple terms"
    result = agent.process(query)

    return {
        "input": query,
        "actual": result,
        "evaluation_criteria": {
            "clarity": "Explanation should be clear and simple",
            "accuracy": "Scientific information should be accurate",
            "completeness": "Should cover the main aspects of photosynthesis"
        }
    }
```

## 🔧 Advanced Features

### Git Integration

AgentTest automatically tracks git information with each test run:

- Commit hash and branch
- Changed files
- Author and timestamp
- Test result history

```bash
# View test history
agenttest log --limit 20

# Compare between branches
agenttest compare main feature/new-model

# Compare specific commits
agenttest compare abc123 def456
```

### CI/CD Integration

#### GitHub Actions Example

```yaml
name: AgentTest CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9

      - name: Install dependencies
        run: |
          pip install agenttest[all]
          pip install -r requirements.txt

      - name: Run AgentTest
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
        run: |
          agenttest run --ci --verbose

      - name: Upload test results
        uses: actions/upload-artifact@v2
        with:
          name: test-results
          path: .agenttest/results/
```

### Test Generation

AgentTest can automatically generate test cases by analyzing your agent code:

```bash
# Generate tests for all discovered agents
agenttest generate

# Generate for specific agent with custom count
agenttest generate --agent agents/my_agent.py --count 10

# Generate in different formats
agenttest generate --agent agents/my_agent.py --format yaml
agenttest generate --agent agents/my_agent.py --format json
```

## 📚 Documentation

AgentTest includes comprehensive documentation built with MkDocs and hosted on GitHub Pages.

### 🌐 Online Documentation

Visit the full documentation at: **https://your-username.github.io/your-repo-name/**

### 🏠 Local Documentation

You can also run the documentation locally:

```bash
# Install documentation dependencies
pip install -e ".[docs]"

# Serve documentation locally
mkdocs serve
# Or use the helper script
./scripts/docs.sh serve
```

The documentation includes:

- **Installation & Setup**: Complete installation guide
- **Quick Start**: Get started in 5 minutes
- **Auto Test Generation**: Comprehensive guide to intelligent test generation
- **User Guide**: Configuration, writing tests, CLI commands
- **Evaluators**: Detailed guide for all evaluation methods
- **Examples**: Practical examples and tutorials
- **API Reference**: Complete API documentation
- **Git Integration**: Advanced git-aware features

### 📝 Documentation Development

To contribute to documentation:

```bash
# Build documentation
./scripts/docs.sh build

# Build with strict mode (fail on warnings)
./scripts/docs.sh build-strict

# Deploy to GitHub Pages
./scripts/docs.sh deploy
```

See [README_DOCS.md](README_DOCS.md) for detailed documentation setup instructions.

## 📚 API Reference

### Core Functions

- `@agent_test()`: Decorator to mark test functions
- `run_test()`: Utility to run individual tests programmatically

### CLI Commands

- `agenttest init`: Initialize new project
- `agenttest run`: Run tests
- `agenttest generate`: Generate test cases
- `agenttest log`: View test history
- `agenttest compare`: Compare test results

### Configuration Classes

- `Config`: Main configuration management
- `LLMConfig`: LLM provider settings
- `EvaluatorConfig`: Evaluator configurations

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/Nihal-Srivastava05/agent-test
cd agenttest

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
black agenttest/
isort agenttest/
flake8 agenttest/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by pytest's excellent design
- Built for the AI agent development community
- Special thanks to all contributors

## 🆘 Support

- 📖 [Documentation](https://nihal-srivastava05.github.io/agent-test/)
- 🐛 [Issue Tracker](https://github.com/Nihal-Srivastava05/agent-test/issues)
- 💬 [Discussions](https://github.com/Nihal-Srivastava05/agent-test/discussions)
- 📧 [Email Support](mailto:nihal.srivastava05@gmail.com)

---

**AgentTest** - Making AI agent testing as easy as `pytest` 🧪✨
