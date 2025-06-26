# CLI Commands Reference

AgentTest provides a comprehensive command-line interface with pytest-like functionality for AI agent testing. This guide covers all available commands and their options.

## 📋 Command Overview

| Command     | Purpose             | Common Usage                         |
| ----------- | ------------------- | ------------------------------------ |
| `init`      | Initialize project  | Set up new testing environment       |
| `run`       | Execute tests       | Run test suites with various options |
| `log`       | View test history   | Browse past test results             |
| `compare`   | Compare results     | Git-based performance comparison     |
| `generate`  | Auto-generate tests | AI-powered test creation             |
| `dashboard` | Web interface       | Visual test monitoring               |

## 🚀 agenttest init

Initialize a new AgentTest project with configuration and directory structure.

### Syntax

```bash
agenttest init [PATH] [OPTIONS]
```

### Parameters

| Parameter        | Type    | Default | Description               |
| ---------------- | ------- | ------- | ------------------------- |
| `PATH`           | Path    | `.`     | Directory to initialize   |
| `--template, -t` | String  | `basic` | Configuration template    |
| `--overwrite`    | Boolean | `false` | Overwrite existing config |

### Templates

| Template     | Description                         | Best For                |
| ------------ | ----------------------------------- | ----------------------- |
| `basic`      | Standard setup with core evaluators | General agent testing   |
| `langchain`  | Optimized for LangChain agents      | LangChain applications  |
| `llamaindex` | Optimized for LlamaIndex            | LlamaIndex applications |

### Examples

```bash
# Initialize in current directory
agenttest init

# Initialize new project
agenttest init ./my-agent-project

# Use LangChain template
agenttest init --template langchain

# Force overwrite existing config
agenttest init --overwrite
```

### Generated Structure

```
project/
├── .agenttest/
│   ├── config.yaml         # Main configuration
│   └── results/            # Test results storage
├── tests/
│   ├── __init__.py
│   └── test_example.py     # Sample test
└── .env                    # Environment variables
```

---

## 🧪 agenttest run

Execute test suites with comprehensive filtering and output options.

### Syntax

```bash
agenttest run [OPTIONS]
```

### Core Parameters

| Parameter       | Type    | Default     | Description               |
| --------------- | ------- | ----------- | ------------------------- |
| `--path, -p`    | Path    | `tests/`    | Test files or directory   |
| `--pattern`     | String  | `test_*.py` | File name pattern         |
| `--verbose, -v` | Boolean | `false`     | Detailed output           |
| `--quiet, -q`   | Boolean | `false`     | Minimal output            |
| `--ci`          | Boolean | `false`     | CI mode (exit on failure) |

### Output Parameters

| Parameter      | Type | Default | Description          |
| -------------- | ---- | ------- | -------------------- |
| `--output, -o` | Path | None    | Save results to file |
| `--log-output` | Path | None    | Export detailed logs |

### Filtering Parameters

| Parameter   | Type     | Default | Description                  |
| ----------- | -------- | ------- | ---------------------------- |
| `--tag, -t` | String[] | None    | Run tests with specific tags |

### Examples

#### Basic Usage

```bash
# Run all tests
agenttest run

# Run with verbose output
agenttest run --verbose

# Run specific test file
agenttest run --path tests/test_summarization.py

# Run tests matching pattern
agenttest run --pattern "*integration*"
```

#### Filtering Tests

```bash
# Run tests with specific tags
agenttest run --tag summarization --tag quality

# Run tests in specific directory
agenttest run --path tests/integration/
```

#### Output and Logging

```bash
# Save results to JSON
agenttest run --output results.json

# Export detailed logs
agenttest run --log-output debug.log

# Combined output
agenttest run --output results.json --log-output debug.log --verbose
```

#### CI/CD Integration

```bash
# CI mode (exits with error code on failure)
agenttest run --ci --quiet

# Generate reports for CI
agenttest run --ci --output ci-results.json --quiet
```

### Output Format

#### Standard Output

```
🧪 Running AgentTest suite...

📊 Test Results Summary:
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Test                          ┃ Status  ┃ Score   ┃ Duration     ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ test_summarization            │ ✅ PASS │ 0.873   │ 2.45s        │
│ test_qa_accuracy              │ ❌ FAIL │ 0.654   │ 1.23s        │
│ test_content_generation       │ ✅ PASS │ 0.912   │ 3.67s        │
└───────────────────────────────┴─────────┴─────────┴──────────────┘

📈 Overall Results:
• Total Tests: 3
• Passed: 2 (67%)
• Failed: 1 (33%)
• Average Score: 0.813
• Total Duration: 7.35s

❌ Failures Detected:
• test_qa_accuracy: Score 0.654 below threshold 0.7
  - similarity: 0.654 (threshold: 0.7)
  - Expected: "The answer is 42"
  - Actual: "I think the answer might be 42"
```

#### Verbose Output

```
🔍 SESSION: Starting test session (2024-06-26 14:30:15)
🔍 DISCOVERY: Found 3 test files in tests/
🔍 DISCOVERY: Discovered 5 test functions

🔍 TEST_START: test_summarization
  📊 Evaluation Results:
    • similarity: Score: 0.873, Passed: ✅
    • llm_judge: Score: 0.845, Passed: ✅
✅ TEST_PASS: test_summarization (2.45s)

🔍 TEST_START: test_qa_accuracy
  📊 Evaluation Results:
    • similarity: Score: 0.654, Passed: ❌
❌ TEST_FAIL: test_qa_accuracy (1.23s)
```

---

## 📚 agenttest log

View and browse test execution history with git integration.

### Syntax

```bash
agenttest log [OPTIONS]
```

### Parameters

| Parameter      | Type    | Default | Description                      |
| -------------- | ------- | ------- | -------------------------------- |
| `--limit, -l`  | Integer | `10`    | Number of runs to show           |
| `--commit, -c` | String  | None    | Show results for specific commit |
| `--branch, -b` | String  | None    | Show results for specific branch |

### Examples

```bash
# Show last 10 test runs
agenttest log

# Show last 20 runs
agenttest log --limit 20

# Show results for specific commit
agenttest log --commit abc123

# Show results for main branch
agenttest log --branch main
```

### Output Format

```
📚 Test History (last 10 runs):

┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Commit     ┃ Timestamp           ┃ Branch        ┃ Tests         ┃ Pass Rate     ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ e1c83a6d   │ 2024-06-26 14:45:12 │ main          │ 5 passed, 0   │ 100%          │
│ 95eadec3   │ 2024-06-26 14:38:33 │ main          │ 3 passed, 2   │ 60%           │
│ 7b2af91e   │ 2024-06-26 12:15:44 │ feature-123   │ 4 passed, 1   │ 80%           │
└────────────┴─────────────────────┴───────────────┴───────────────┴───────────────┘
```

---

## 🔄 agenttest compare

Compare test results between git commits or branches with detailed analysis.

### Syntax

```bash
agenttest compare BASE [TARGET] [OPTIONS]
```

### Parameters

| Parameter                 | Type    | Default  | Description                  |
| ------------------------- | ------- | -------- | ---------------------------- |
| `BASE`                    | String  | Required | Base commit/branch           |
| `TARGET`                  | String  | `HEAD`   | Target commit/branch         |
| `--metric, -m`            | String  | None     | Focus on specific evaluator  |
| `--filter, -f`            | String  | None     | Filter tests by name pattern |
| `--min-change, -c`        | Float   | `0.01`   | Minimum change threshold     |
| `--include-unchanged, -u` | Boolean | `false`  | Include unchanged tests      |
| `--detailed, -d`          | Boolean | `false`  | Show evaluator-level details |
| `--export, -e`            | Path    | None     | Export to JSON file          |

### Examples

#### Basic Comparison

```bash
# Compare current HEAD with previous commit
agenttest compare abc123

# Compare two specific commits
agenttest compare abc123 def456

# Compare branches
agenttest compare main feature-branch
```

#### Filtered Comparison

```bash
# Focus on similarity evaluator only
agenttest compare abc123 --metric similarity

# Filter tests by name
agenttest compare abc123 --filter "summarization"

# Show only significant changes (>5%)
agenttest compare abc123 --min-change 0.05
```

#### Detailed Analysis

```bash
# Show evaluator-level details
agenttest compare abc123 --detailed

# Include unchanged tests
agenttest compare abc123 --include-unchanged

# Export full comparison
agenttest compare abc123 --export comparison.json
```

#### Complex Filtering

```bash
# Combine multiple filters
agenttest compare abc123 def456 \
  --metric similarity \
  --filter "qa" \
  --min-change 0.02 \
  --detailed
```

### Output Format

#### Standard Comparison

```
📊 Comparing abc123 → def456
Base: abc123 (2024-06-26T14:38:33)
Target: def456 (2024-06-26T14:45:12)

📊 Overall Summary Changes:
┏━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━┓
┃ Metric       ┃   Base ┃  Target ┃  Change ┃ % Change  ┃
┡━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━┩
│ Pass Rate    │   0.75 │    0.85 │  +0.100 │    +13.3% │
│ Average Score│   0.692│    0.751│  +0.059 │     +8.5% │
└──────────────┴────────┴─────────┴─────────┴───────────┘

🔍 Test Changes Overview
├── 📈 Improvements: 2
├── 📉 Regressions: 1
└── 🆕 New Tests: 0

📈 Improvements:
  • test_summarization: score: 0.734 → 0.856 (+0.122)
  • test_qa_accuracy: FAIL → PASS, score: 0.650 → 0.823 (+0.173)

📉 Regressions:
  • test_content_generation: score: 0.891 → 0.734 (-0.157)
```

#### Detailed Comparison

```bash
agenttest compare abc123 --detailed
```

```
🔍 Evaluator-Specific Changes:

  similarity:
    • test_summarization: 0.734 → 0.856 (+0.122)
    • test_qa_accuracy: 0.432 → 0.678 (+0.246)

  llm_judge:
    • test_summarization: 0.823 → 0.867 (+0.044)
    • test_content_generation: 0.912 → 0.745 (-0.167)
```

---

## 🤖 agenttest generate

Automatically analyze your code and generate comprehensive test cases with intelligent project structure understanding.

### Syntax

```bash
agenttest generate [FILE_PATH] [OPTIONS]
```

### Core Parameters

| Parameter        | Type    | Default  | Description                      |
| ---------------- | ------- | -------- | -------------------------------- |
| `FILE_PATH`      | String  | Required | Agent file to analyze and test   |
| `--count, -c`    | Integer | `5`      | Number of test cases to generate |
| `--format, -f`   | String  | `python` | Output format (python/yaml/json) |
| `--output, -o`   | Path    | None     | Save generated tests to file     |
| `--template, -t` | Path    | None     | Custom Jinja2 template           |

### Advanced Parameters

| Parameter         | Type    | Default | Description                      |
| ----------------- | ------- | ------- | -------------------------------- |
| `--no-llm`        | Boolean | `false` | Use fallback mode (no LLM)       |
| `--search-dirs`   | String  | None    | Additional directories to search |
| `--include-edge`  | Boolean | `true`  | Include edge case tests          |
| `--include-error` | Boolean | `true`  | Include error handling tests     |

### Intelligence Features

The generator automatically:

- 🔍 **Analyzes project structure** to generate correct imports
- 🎯 **Understands functions and classes** to create proper test calls
- 📝 **Generates realistic test data** based on parameter names and types
- 🧪 **Creates multiple test scenarios** (basic, edge cases, error handling)
- 🏗️ **Handles class instantiation** automatically for method testing

### Examples

#### Basic Generation

```bash
# Generate tests for a specific file
agenttest generate examples/agents_sample.py

# Generate more test cases
agenttest generate examples/agents_sample.py --count 10

# Generate with specific format
agenttest generate examples/agents_sample.py --format yaml
```

#### Advanced Generation

```bash
# Save to specific file
agenttest generate agents/my_agent.py --output tests/generated_test.py

# Use custom template
agenttest generate agents/my_agent.py --template custom_template.py.j2

# Generate without LLM (fallback mode)
agenttest generate agents/my_agent.py --no-llm --count 3
```

#### Multiple Files

```bash
# Generate for multiple files
agenttest generate examples/*.py --count 3

# Generate for specific patterns
agenttest generate "agents/*_agent.py" --count 2
```

### Output Formats

#### Python Format (Default)

Generates executable Python test files:

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

#### YAML Format

```yaml
agent: agents_sample
description: Generated tests for agents_sample
test_cases:
  - name: test_handle_customer_query_basic
    description: Test basic functionality of handle_customer_query
    function_to_test: handle_customer_query
    input_data:
      query: 'test query'
      customer_type: 'premium'
    expected_behavior: Should execute handle_customer_query successfully
```

#### JSON Format

```json
{
  "agent": "agents_sample",
  "description": "Generated tests for agents_sample",
  "test_cases": [
    {
      "name": "test_handle_customer_query_basic",
      "description": "Test basic functionality of handle_customer_query",
      "function_to_test": "handle_customer_query",
      "input_data": {
        "query": "test query",
        "customer_type": "premium"
      }
    }
  ]
}
```

### Generated Test Types

#### Function Tests

- **Basic functionality**: Normal operation with typical inputs
- **Edge cases**: Empty inputs, boundary values, null conditions
- **Error handling**: Invalid inputs and exception scenarios

#### Class Tests

- **Constructor tests**: Object creation with proper arguments
- **Method tests**: Instance method calls with realistic data
- **Integration tests**: Multi-method workflows

### Customization

#### Custom Templates

Create `.agenttest/templates/test_template.py.j2`:

```jinja2
"""
Custom test template for {{ agent_name }}.
"""

from agent_test import agent_test
{%- if agent_module_path %}
from {{ agent_module_path }} import *
{%- endif %}

{%- for test_case in test_cases %}
@agent_test(
    criteria=[{%- for criterion in test_case.evaluation_criteria.keys() -%}"{{ criterion }}"{%- if not loop.last %}, {% endif -%}{%- endfor -%}],
    tags={{ test_case.tags | tojson }}
)
def {{ test_case.name }}():
    """{{ test_case.description }}"""
    # Your custom test logic here
    pass
{%- endfor %}
```

#### Configuration

Set generation preferences in `.agenttest/config.yaml`:

```yaml
generation:
  default_count: 5
  include_edge_cases: true
  include_error_handling: true
  default_format: python

llm:
  provider: openai
  model: gpt-4
  temperature: 0.7
  max_tokens: 3000
```

### Formats

| Format   | Description           | File Extension |
| -------- | --------------------- | -------------- |
| `python` | Python test functions | `.py`          |
| `yaml`   | YAML test cases       | `.yaml`        |
| `json`   | JSON test data        | `.json`        |

### Examples

```bash
# Generate 5 test cases for an agent
agenttest generate --agent my_agent.py

# Generate 10 tests and save to file
agenttest generate --agent my_agent.py --count 10 --output tests/generated_tests.py

# Generate YAML format tests
agenttest generate --agent my_agent.py --format yaml --output test_cases.yaml
```

---

## 🖥️ agenttest dashboard

Launch a web-based dashboard for monitoring test results and performance.

### Syntax

```bash
agenttest dashboard [OPTIONS]
```

### Parameters

| Parameter    | Type    | Default     | Description |
| ------------ | ------- | ----------- | ----------- |
| `--port, -p` | Integer | `8080`      | Server port |
| `--host`     | String  | `localhost` | Server host |

### Examples

```bash
# Start dashboard on default port
agenttest dashboard

# Use custom port
agenttest dashboard --port 3000

# Bind to all interfaces
agenttest dashboard --host 0.0.0.0 --port 8080
```

### Dashboard Features

- **Test Results Timeline**: Visual performance tracking
- **Evaluator Breakdown**: Per-evaluator performance analysis
- **Git Integration**: Commit-based result comparison
- **Filter and Search**: Find specific tests and patterns
- **Export Options**: Download results and reports

---

## 🌟 Advanced Usage Patterns

### CI/CD Pipeline Integration

```bash
# .github/workflows/test.yml
- name: Run AgentTest
  run: |
    agenttest run --ci --output results.json
    agenttest compare ${{ github.event.before }} HEAD --export comparison.json
```

### Development Workflow

```bash
# Quick development loop
agenttest run --path tests/test_new_feature.py --verbose

# Check regression before commit
agenttest compare HEAD~1 HEAD --detailed

# Monitor specific evaluator
agenttest run --verbose | grep similarity
```

### Batch Processing

```bash
# Run multiple test suites
for suite in unit integration e2e; do
  agenttest run --path tests/$suite/ --output results-$suite.json
done

# Compare across branches
for branch in main develop feature-123; do
  git checkout $branch
  agenttest run --quiet --output results-$branch.json
done
```

### Performance Monitoring

```bash
# Track performance over time
agenttest log --limit 50 > performance-history.txt

# Generate detailed comparison reports
agenttest compare $(git rev-parse HEAD~10) HEAD \
  --detailed \
  --export performance-report.json
```

## 🔧 Global Options

These options work with all commands:

| Option      | Description            |
| ----------- | ---------------------- |
| `--help`    | Show command help      |
| `--version` | Show AgentTest version |
| `--config`  | Use custom config file |

### Examples

```bash
# Show version
agenttest --version

# Use custom configuration
agenttest run --config /path/to/custom-config.yaml

# Get help for any command
agenttest compare --help
```

## 🔗 Related Documentation

- [Configuration](configuration.md) - Configuration file options
- [Writing Tests](writing-tests.md) - Test structure and patterns
- [Git Integration](git-integration.md) - Version control features
- [Evaluators](evaluators.md) - Understanding evaluation metrics
