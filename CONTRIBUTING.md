# Contributing to AgentTest

Thank you for your interest in contributing to AgentTest! We welcome contributions from the community.

## 🚀 Getting Started

### Development Setup

1. **Fork and Clone**

   ```bash
   git clone https://github.com/yourusername/agenttest.git
   cd agenttest
   ```

2. **Create Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Development Dependencies**

   ```bash
   pip install -e ".[dev]"
   ```

4. **Install Pre-commit Hooks**
   ```bash
   pre-commit install
   ```

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=agenttest

# Run specific test file
pytest tests/test_agenttest_core.py

# Run AgentTest on itself (dogfooding!)
agenttest run
```

## 🔧 Development Workflow

1. **Create a Branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**

   - Write your code
   - Add tests for new functionality
   - Update documentation if needed

3. **Run Quality Checks**

   ```bash
   # Format code
   black agenttest/
   isort agenttest/

   # Check linting
   flake8 agenttest/

   # Type checking
   mypy agenttest/

   # Run tests
   pytest
   ```

4. **Commit and Push**

   ```bash
   git add .
   git commit -m "feat: add your feature description"
   git push origin feature/your-feature-name
   ```

5. **Create Pull Request**
   - Open a PR from your fork
   - Fill out the PR template
   - Ensure all CI checks pass

## 📝 Code Style

We follow these conventions:

- **Python**: PEP 8 with Black formatting
- **Line Length**: 88 characters
- **Import Sorting**: isort
- **Type Hints**: Encouraged for new code
- **Docstrings**: Google style

### Example Function

```python
def evaluate_agent_output(
    actual: str,
    expected: str,
    criteria: List[str]
) -> EvaluationResult:
    """Evaluate agent output against expected result.

    Args:
        actual: The actual output from the agent
        expected: The expected output
        criteria: List of evaluation criteria to apply

    Returns:
        EvaluationResult containing score and details

    Raises:
        EvaluationError: If evaluation fails
    """
    # Implementation here
    pass
```

## 🎯 What to Contribute

### High Priority Areas

- **New Evaluators**: String similarity, semantic similarity, custom metrics
- **Framework Integrations**: LangChain, LlamaIndex, Hugging Face
- **CLI Improvements**: Better error messages, progress bars
- **Documentation**: Tutorials, examples, API docs
- **Performance**: Parallel test execution, caching

### Evaluator Development

To add a new evaluator:

1. **Create Evaluator Class**

   ```python
   # agenttest/evaluators/my_evaluator.py
   from .base import BaseEvaluator, EvaluationResult

   class MyEvaluator(BaseEvaluator):
       @property
       def name(self) -> str:
           return "my_evaluator"

       def evaluate(self, test_output: Any) -> EvaluationResult:
           # Your evaluation logic
           pass
   ```

2. **Register in Registry**

   ```python
   # agenttest/evaluators/registry.py
   from .my_evaluator import MyEvaluator

   # Add to _register_default_evaluators method
   my_config = self._get_evaluator_config("my_evaluator")
   self._evaluators["my_evaluator"] = MyEvaluator(my_config)
   ```

3. **Add Tests**

   ```python
   # tests/test_my_evaluator.py
   def test_my_evaluator():
       evaluator = MyEvaluator()
       result = evaluator.evaluate(test_data)
       assert result.passed is True
   ```

4. **Update Documentation**
   - Add to README.md
   - Add example usage
   - Update API docs

### Framework Integration

To add support for a new framework:

1. **Create Adapter**

   ```python
   # agenttest/adapters/my_framework.py
   class MyFrameworkAdapter:
       def load_agent(self, config: dict):
           """Load agent from framework"""
           pass

       def run_agent(self, agent, input_data):
           """Run agent with input"""
           pass
   ```

2. **Add Template**
   ```python
   # Update agenttest/core/init.py
   def _create_my_framework_examples(project_path: Path):
       # Create framework-specific examples
       pass
   ```

## 🐛 Bug Reports

When reporting bugs, please include:

- **Environment**: Python version, OS, AgentTest version
- **Steps to Reproduce**: Minimal code example
- **Expected vs Actual**: What should happen vs what happens
- **Logs**: Any error messages or stack traces

Use this template:

````markdown
## Bug Description

Brief description of the issue

## Environment

- AgentTest version:
- Python version:
- OS:

## Steps to Reproduce

1. Step one
2. Step two
3. Step three

## Expected Behavior

What you expected to happen

## Actual Behavior

What actually happened

## Code Example

```python
# Minimal reproducible example
```
````

## Error Output

```
# Any error messages or stack traces
```

````

## 💡 Feature Requests

For feature requests:

1. **Check existing issues** to avoid duplicates
2. **Describe the problem** you're trying to solve
3. **Propose a solution** with examples
4. **Consider alternatives** and trade-offs

## 📋 Pull Request Guidelines

### PR Checklist

- [ ] Code follows style guidelines
- [ ] Tests added for new functionality
- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated (for significant changes)
- [ ] No breaking changes (or clearly documented)

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Refactoring

## Testing
- [ ] Added tests for new functionality
- [ ] All existing tests pass
- [ ] Manual testing performed

## Documentation
- [ ] Updated README.md
- [ ] Updated docstrings
- [ ] Added examples

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] No breaking changes
````

## 🏆 Recognition

Contributors will be:

- Added to `CONTRIBUTORS.md`
- Mentioned in release notes
- Invited to our contributors Discord
- Eligible for contributor swag

## ❓ Questions?

- 💬 [Discussions](https://github.com/agenttest-ai/agenttest/discussions)
- 📧 [Email](mailto:contributors@agenttest.ai)
- 🐛 [Issues](https://github.com/agenttest-ai/agenttest/issues)

## 📜 Code of Conduct

Please note that this project is released with a [Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

---

**Thank you for contributing to AgentTest!** 🎉
