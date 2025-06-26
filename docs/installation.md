# Installation & Setup

This guide covers how to install AgentTest and set up your testing environment.

## 📦 Installation Options

### Basic Installation

```bash
pip install agenttest
```

This installs the core functionality with support for:

- Basic evaluators (similarity, contains, regex)
- OpenAI, Anthropic, and Google Gemini LLM providers
- Git integration and logging
- Command-line interface

### Optional Dependencies

AgentTest supports additional packages for extended functionality:

```bash
# Install with LangChain support
pip install agenttest[langchain]

# Install with LlamaIndex support
pip install agenttest[llamaindex]

# Install with all optional dependencies
pip install agenttest[all]

# Development installation (includes testing tools)
pip install agenttest[dev]
```

### Dependency Overview

| Package           | Purpose                 | Optional Dependencies                                  |
| ----------------- | ----------------------- | ------------------------------------------------------ |
| **Core**          | Basic testing framework | `typer`, `pydantic`, `rich`, `gitpython`               |
| **LLM Providers** | AI evaluation support   | `openai`, `anthropic`, `google-generativeai`           |
| **NLP Metrics**   | Advanced metrics        | `nltk`, `rouge-score`, `scikit-learn`                  |
| **LangChain**     | LangChain agent testing | `langchain`, `langchain-openai`, `langchain-anthropic` |
| **LlamaIndex**    | LlamaIndex support      | `llama-index`                                          |

## 🔧 Environment Setup

### 1. API Keys Configuration

AgentTest supports multiple LLM providers. Set up the appropriate API keys:

```bash
# OpenAI
export OPENAI_API_KEY="your-openai-key"

# Anthropic
export ANTHROPIC_API_KEY="your-anthropic-key"

# Google Gemini
export GOOGLE_API_KEY="your-google-key"
# OR
export GEMINI_API_KEY="your-gemini-key"
```

You can also use a `.env` file in your project root:

```env
# .env file
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
GOOGLE_API_KEY=your-google-key
```

### 2. Initialize a New Project

```bash
# Initialize in current directory
agenttest init

# Initialize in specific directory
agenttest init ./my-agent-project

# Use specific template
agenttest init --template langchain

# Overwrite existing configuration
agenttest init --overwrite
```

Available templates:

- `basic` - Standard configuration with core evaluators
- `langchain` - Optimized for LangChain agents
- `llamaindex` - Optimized for LlamaIndex applications

### 3. Project Structure

After initialization, your project will have:

```
my-agent-project/
├── .agenttest/
│   ├── config.yaml         # Main configuration
│   └── results/            # Test results history
├── tests/
│   ├── __init__.py
│   └── test_example.py     # Sample test file
├── agents/                 # Your agent implementations
└── .env                    # Environment variables (optional)
```

## ⚙️ Basic Configuration

The `.agenttest/config.yaml` file contains your project configuration:

```yaml
version: '1.0'
project_name: 'My Agent Project'

# LLM Configuration
llm:
  provider: 'openai' # openai, anthropic, gemini
  model: 'gpt-3.5-turbo'
  temperature: 0.0

# Default Evaluators
evaluators:
  - name: 'similarity'
    type: 'string_similarity'
    config:
      method: 'cosine' # cosine, levenshtein, jaccard
      threshold: 0.8
    weight: 1.0
    enabled: true

  - name: 'llm_judge'
    type: 'llm_as_judge'
    config:
      criteria: ['accuracy', 'relevance']
      provider: 'openai' # Can override global LLM config
    weight: 1.0
    enabled: true

# Test Configuration
testing:
  test_dirs: ['tests']
  test_patterns: ['test_*.py', '*_test.py']
  parallel: false
  timeout: 300
  retry_count: 0

# Logging Configuration
logging:
  level: 'INFO'
  git_aware: true
  results_dir: '.agenttest/results'
```

## 🚀 Verification

Verify your installation:

```bash
# Check version
agenttest --version

# Run help
agenttest --help

# Test configuration
agenttest run --help
```

## 🔍 Troubleshooting

### Common Issues

**ImportError: No module named 'openai'**

```bash
pip install openai
```

**API Key Not Found**

- Ensure environment variables are set correctly
- Check `.env` file location and format
- Verify API key validity

**Configuration File Not Found**

```bash
# Reinitialize project
agenttest init --overwrite
```

**Permission Errors**

```bash
# Use virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
pip install agenttest
```

### Requirements

- **Python**: 3.8 or higher
- **Git**: Required for git integration features
- **Internet**: Required for LLM provider APIs

## 🔄 Upgrading

```bash
# Upgrade to latest version
pip install --upgrade agenttest

# Upgrade with all dependencies
pip install --upgrade agenttest[all]
```

## 🐳 Docker Support

You can also run AgentTest in Docker:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["agenttest", "run"]
```

```bash
# Build and run
docker build -t my-agent-tests .
docker run -e OPENAI_API_KEY=$OPENAI_API_KEY my-agent-tests
```

---

**Next Steps**: Once installed, check out the [Quick Start Guide](quickstart.md) to write your first test!
