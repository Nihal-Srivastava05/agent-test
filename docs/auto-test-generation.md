# Auto Test Generation

AgentTest provides powerful automatic test generation capabilities that can analyze your agent code and create comprehensive test cases with minimal manual effort. The test generator uses advanced code analysis and optional LLM integration to understand your project structure and generate intelligent, contextual tests.

## Overview

The auto test generator automatically:

- **Analyzes project structure** to understand code organization
- **Generates correct imports** based on file locations and dependencies
- **Creates realistic test data** based on function signatures and parameter names
- **Produces proper function calls** for both standalone functions and class methods
- **Handles class instantiation** automatically for method testing
- **Creates comprehensive coverage** including basic, edge case, and error scenarios

## Quick Start

### Basic Usage

```bash
# Generate tests for a specific file
agenttest generate examples/agents_sample.py --count 5

# Generate tests with specific format
agenttest generate examples/agents_sample.py --format python --count 3

# Generate tests for multiple files
agenttest generate examples/*.py --count 2
```

### Programmatic Usage

```python
from agent_test.generators.test_generator import TestGenerator
from agent_test.core.config import Config

# Load configuration
config = Config.load()

# Create generator
generator = TestGenerator(config)

# Generate tests
test_code = generator.generate_tests(
    agent_path="examples/agents_sample.py",
    count=5,
    format="python"
)

print(test_code)
```

## Configuration

### LLM Configuration

For enhanced test generation, configure an LLM provider in your `.agenttest/config.yaml`:

```yaml
llm:
  provider: 'openai' # or "anthropic", "gemini"
  model: 'gpt-4'
  api_key: '${OPENAI_API_KEY}' # or set directly
  temperature: 0.7
  max_tokens: 3000
```

### Fallback Mode

If no LLM is configured, the generator uses intelligent fallback based on code analysis:

```python
# The generator will automatically use fallback mode
generator = TestGenerator(config)  # Works without LLM configuration
```

## Generated Test Structure

### Function Tests

For standalone functions, the generator creates tests like:

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
    expected_behavior = "Should execute handle_customer_query successfully"

    # Call the function being tested
    actual = handle_customer_query(**input_data)

    return {
        "input": input_data,
        "expected_behavior": expected_behavior,
        "actual": actual,
        "evaluation_criteria": {
            "execution": "Function should execute without errors",
            "output_type": "Should return appropriate type",
            "functionality": "Should perform expected operation"
        }
    }
```

### Class Tests

For classes, the generator creates both constructor and method tests:

```python
@agent_test(
    criteria=["instantiation", "attributes"],
    tags=["basic", "class", "constructor"]
)
def test_customersupportagent_creation():
    """Test creation of CustomerSupportAgent object"""
    input_data = {"api_key": "test_api_key"}
    expected_behavior = "Should create CustomerSupportAgent instance successfully"

    # Call the function being tested
    actual = CustomerSupportAgent(**input_data)

    return {
        "input": input_data,
        "expected_behavior": expected_behavior,
        "actual": actual,
        "evaluation_criteria": {
            "instantiation": "Object should be created successfully",
            "attributes": "Object attributes should be set correctly"
        }
    }

@agent_test(
    criteria=["method_execution", "return_value"],
    tags=["method", "class"]
)
def test_customersupportagent_classify_query():
    """Test classify_query method of CustomerSupportAgent"""
    input_data = {"query": "test query for method"}
    expected_behavior = "Should execute classify_query method successfully"

    # Call the function being tested
    instance = CustomerSupportAgent(api_key="test_api_key")
    actual = instance.classify_query(query="test query for method")

    return {
        "input": input_data,
        "expected_behavior": expected_behavior,
        "actual": actual,
        "evaluation_criteria": {
            "method_execution": "Method should execute without errors",
            "return_value": "Should return appropriate value"
        }
    }
```

## Advanced Features

### Project Structure Analysis

The generator automatically analyzes your project structure:

```python
# Example analysis output
{
    "project_root": "/path/to/project",
    "module_path": "examples.agents_sample",
    "relative_path": "examples/agents_sample.py",
    "package_structure": {
        "packages": ["examples", "agent_test"],
        "modules": ["examples.agents_sample", "agent_test.core.config"]
    }
}
```

### Intelligent Import Generation

Based on the analysis, proper imports are generated:

```python
from agent_test import agent_test
from examples.agents_sample import *
import google.generativeai  # Auto-detected dependency
```

### Smart Input Data Generation

The generator creates realistic test data based on parameter analysis:

```python
# Parameter name recognition
{
    "query": "test query",           # Recognized as query parameter
    "api_key": "test_api_key",      # Recognized as API key
    "config": {"setting": "value"}, # Recognized as configuration
    "count": 5,                     # Recognized as numeric parameter
    "data": {"key": "value"}        # Recognized as data structure
}
```

## Output Formats

### Python Format (Default)

Generates executable Python test files:

```python
generator.generate_tests(
    agent_path="path/to/agent.py",
    format="python"
)
```

### YAML Format

Generates structured YAML for further processing:

```python
generator.generate_tests(
    agent_path="path/to/agent.py",
    format="yaml"
)
```

### JSON Format

Generates JSON for integration with other tools:

```python
generator.generate_tests(
    agent_path="path/to/agent.py",
    format="json"
)
```

## Test Types Generated

### Basic Functionality Tests

- Normal operation with typical inputs
- Successful execution scenarios
- Expected return value validation

### Edge Case Tests

- Empty or null inputs
- Boundary value conditions
- Minimal valid inputs

### Error Handling Tests

- Invalid input types
- Missing required parameters
- Exception scenarios

### Performance Tests

- Large input handling
- Resource usage validation
- Timeout scenarios

## Customization

### Custom Templates

Create custom test templates in `.agenttest/templates/`:

```jinja2
# .agenttest/templates/test_template.py.j2
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

### Custom Evaluators

Specify custom evaluation criteria:

```python
# In your configuration
evaluators = [
    {
        "name": "custom_accuracy",
        "type": "custom_evaluator",
        "config": {"threshold": 0.9}
    }
]
```

## CLI Commands

### Generate Command

```bash
# Basic generation
agenttest generate <file_path>

# With options
agenttest generate <file_path> \
    --count 10 \
    --format python \
    --output tests/generated_test.py

# Multiple files
agenttest generate examples/*.py --count 3

# With custom template
agenttest generate <file_path> \
    --template custom_template.py.j2
```

### Discover Command

Find agent files automatically:

```bash
# Discover agents in current directory
agenttest discover

# Discover in specific directories
agenttest discover --dirs agents src examples

# Generate tests for discovered agents
agenttest discover --generate --count 5
```

## Integration Examples

### CI/CD Integration

```yaml
# .github/workflows/test-generation.yml
name: Auto Test Generation
on: [push, pull_request]

jobs:
  generate-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install AgentTest
        run: pip install agent-test

      - name: Generate Tests
        run: |
          agenttest generate agents/*.py --count 5
          agenttest run tests/
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: generate-tests
        name: Generate Tests
        entry: agenttest generate
        language: system
        files: '^agents/.*\.py$'
        args: ['--count', '3']
```

## Best Practices

### 1. Code Organization

Structure your code for better test generation:

```python
# Good: Clear function signatures with type hints
def process_query(query: str, max_results: int = 10) -> List[str]:
    """Process a user query and return results."""
    pass

# Good: Well-documented classes
class Agent:
    """An AI agent for processing queries."""

    def __init__(self, api_key: str, model: str = "gpt-4"):
        """Initialize the agent with API credentials."""
        pass
```

### 2. Meaningful Names

Use descriptive parameter names:

```python
# Good: Descriptive parameter names
def analyze_sentiment(text: str, confidence_threshold: float = 0.8):
    pass

# Avoid: Generic parameter names
def analyze(data, threshold):
    pass
```

### 3. Docstrings

Include comprehensive docstrings:

```python
def generate_response(query: str, context: dict) -> str:
    """
    Generate a response to a user query.

    Args:
        query: The user's question or request
        context: Additional context for response generation

    Returns:
        Generated response text

    Raises:
        ValueError: If query is empty
        APIError: If external API call fails
    """
    pass
```

### 4. Configuration

Maintain clean configuration:

```yaml
# .agenttest/config.yaml
version: '1.0'
project_name: 'My Agent Project'

llm:
  provider: 'openai'
  model: 'gpt-4'
  temperature: 0.7

testing:
  test_dirs: ['tests', 'generated_tests']
  parallel: true
  timeout: 300
```

## Troubleshooting

### Common Issues

**Import Errors in Generated Tests**

```bash
# Check module path detection
agenttest analyze <file_path>

# Verify project structure
ls -la .agenttest/
```

**LLM API Errors**

```bash
# Test API connectivity
export OPENAI_API_KEY="your-key"
agenttest test-llm

# Use fallback mode
agenttest generate <file_path> --no-llm
```

**Template Errors**

```bash
# Validate template syntax
agenttest validate-template <template_path>

# Use default template
rm .agenttest/templates/test_template.py.j2
```

### Debug Mode

Enable debug output for troubleshooting:

```bash
agenttest generate <file_path> --debug
```

```python
import logging
logging.basicConfig(level=logging.DEBUG)

generator = TestGenerator(config)
```

## Performance Considerations

### Large Codebases

For large projects, consider:

```bash
# Generate tests incrementally
agenttest generate agents/ --batch-size 10

# Use parallel processing
agenttest generate agents/ --parallel --workers 4

# Filter by file patterns
agenttest generate "agents/*_agent.py" --count 3
```

### LLM Token Usage

Optimize token usage:

```yaml
llm:
  max_tokens: 2000 # Reduce for simpler tests
  temperature: 0.3 # Lower for more consistent output
```

## Examples

See the `examples/` directory for complete examples:

- `examples/agents_sample.py` - Sample agent code
- `examples/tests/enhanced_generated_test.py` - Generated test example
- `examples/.agenttest/` - Configuration examples

## API Reference

For detailed API documentation, see:

- [CLI Reference](cli-commands.md)
