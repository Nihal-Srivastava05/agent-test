# Core API Reference

This document provides detailed API reference for AgentTest's core classes and functions.

## 🧪 Main Decorator

### `agent_test()`

The primary decorator for marking functions as agent tests.

```python
def agent_test(
    criteria: Optional[Union[str, List[str]]] = None,
    tags: Optional[Union[str, List[str]]] = None,
    timeout: Optional[int] = None,
    retry_count: int = 0,
    **metadata
) -> Callable
```

#### Parameters

| Parameter     | Type                       | Default          | Description                  |
| ------------- | -------------------------- | ---------------- | ---------------------------- |
| `criteria`    | `str \| List[str] \| None` | `['similarity']` | Evaluation criteria to use   |
| `tags`        | `str \| List[str] \| None` | `[]`             | Test tags for categorization |
| `timeout`     | `int \| None`              | `300`            | Test timeout in seconds      |
| `retry_count` | `int`                      | `0`              | Number of retries on failure |
| `**metadata`  | `Any`                      | `{}`             | Additional test metadata     |

#### Returns

`Callable`: Decorated test function

#### Example

```python
from agent_test import agent_test

@agent_test(
    criteria=['similarity', 'llm_judge'],
    tags=['summarization', 'quality'],
    timeout=60,
    retry_count=2
)
def test_summarization():
    return {
        "input": "Long article...",
        "actual": agent_summary,
        "expected": "Expected summary..."
    }
```

## 🏃‍♂️ Test Execution

### `run_test()`

Execute a single test function.

```python
def run_test(
    test_func: Callable,
    config: Optional[Config] = None
) -> TestResult
```

#### Parameters

| Parameter   | Type             | Description              |
| ----------- | ---------------- | ------------------------ |
| `test_func` | `Callable`       | Test function to execute |
| `config`    | `Config \| None` | Configuration to use     |

#### Returns

`TestResult`: Test execution result

#### Example

```python
from agent_test import run_test, agent_test

@agent_test(criteria=['similarity'])
def my_test():
    return {"input": "test", "actual": "result", "expected": "result"}

result = run_test(my_test)
print(f"Test passed: {result.passed}")
```

## ⚙️ Configuration

### `Config`

Main configuration class for AgentTest.

```python
class Config:
    def __init__(
        self,
        project_name: str = "AgentTest Project",
        evaluators: List[EvaluatorConfig] = None,
        llm: Optional[LLMConfig] = None,
        git: Optional[GitConfig] = None,
        logging: Optional[LoggingConfig] = None
    )
```

#### Class Methods

##### `Config.load(path: Optional[str] = None) -> Config`

Load configuration from YAML file.

```python
# Load from default location (.agenttest/config.yaml)
config = Config.load()

# Load from specific path
config = Config.load("custom/config.yaml")
```

##### `Config.save(path: Optional[str] = None) -> None`

Save configuration to YAML file.

```python
config.save()  # Save to default location
config.save("backup/config.yaml")  # Save to specific path
```

#### Properties

| Property       | Type                    | Description                |
| -------------- | ----------------------- | -------------------------- |
| `project_name` | `str`                   | Project name               |
| `evaluators`   | `List[EvaluatorConfig]` | Evaluator configurations   |
| `llm`          | `LLMConfig \| None`     | LLM provider configuration |
| `git`          | `GitConfig \| None`     | Git integration settings   |
| `logging`      | `LoggingConfig \| None` | Logging configuration      |

### `EvaluatorConfig`

Configuration for individual evaluators.

```python
@dataclass
class EvaluatorConfig:
    name: str
    type: str
    config: Dict[str, Any] = field(default_factory=dict)
    weight: float = 1.0
    enabled: bool = True
```

### `LLMConfig`

Configuration for LLM providers.

```python
@dataclass
class LLMConfig:
    provider: str  # 'openai', 'anthropic', 'gemini'
    model: str
    api_key: Optional[str] = None
    temperature: float = 0.0
    max_tokens: Optional[int] = None
    timeout: float = 30.0
```

## 🔍 Evaluator Registry

### `EvaluatorRegistry`

Registry for managing and accessing evaluators.

```python
class EvaluatorRegistry:
    def __init__(self, config: Config)
```

#### Methods

##### `get_evaluator(name: str) -> Optional[BaseEvaluator]`

Get an evaluator by name.

```python
registry = EvaluatorRegistry(config)
similarity_evaluator = registry.get_evaluator('similarity')
```

##### `register_evaluator(name: str, evaluator: BaseEvaluator) -> None`

Register a custom evaluator.

```python
custom_evaluator = MyCustomEvaluator(config)
registry.register_evaluator('custom', custom_evaluator)
```

##### `list_evaluators() -> Dict[str, str]`

List all available evaluators.

```python
evaluators = registry.list_evaluators()
# Returns: {'similarity': 'StringSimilarityEvaluator', ...}
```

##### `evaluate_with_multiple(test_output: Any, criteria: List[str]) -> Dict[str, Any]`

Evaluate with multiple evaluators.

```python
results = registry.evaluate_with_multiple(
    test_output=test_data,
    criteria=['similarity', 'llm_judge']
)
```

## 📊 Test Results

### `TestResult`

Represents the result of a single test execution.

```python
@dataclass
class TestResult:
    test_name: str
    passed: bool
    score: Optional[float] = None
    duration: float = 0.0
    error: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)
    evaluations: Dict[str, Any] = field(default_factory=dict)
```

#### Properties

| Property      | Type             | Description                   |
| ------------- | ---------------- | ----------------------------- |
| `test_name`   | `str`            | Name of the test              |
| `passed`      | `bool`           | Whether test passed           |
| `score`       | `float \| None`  | Overall test score (0-1)      |
| `duration`    | `float`          | Test execution time (seconds) |
| `error`       | `str \| None`    | Error message if failed       |
| `details`     | `Dict[str, Any]` | Additional test details       |
| `evaluations` | `Dict[str, Any]` | Individual evaluator results  |

### `TestResults`

Collection of multiple test results.

```python
@dataclass
class TestResults:
    test_results: List[TestResult] = field(default_factory=list)
    summary: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
```

#### Methods

##### `add_result(result: TestResult) -> None`

Add a test result to the collection.

```python
results = TestResults()
results.add_result(test_result)
```

##### `has_failures() -> bool`

Check if any tests failed.

```python
if results.has_failures():
    print("Some tests failed!")
```

##### `get_pass_rate() -> float`

Get the pass rate as a percentage.

```python
pass_rate = results.get_pass_rate()
print(f"Pass rate: {pass_rate:.1f}%")
```

##### `get_summary() -> Dict[str, Any]`

Get a summary of test results.

```python
summary = results.get_summary()
# Returns:
# {
#     "total_tests": 10,
#     "passed": 8,
#     "failed": 2,
#     "pass_rate": 80.0,
#     "average_score": 0.85,
#     "total_duration": 45.2
# }
```

##### `save_to_file(file_path: str) -> None`

Save results to a JSON file.

```python
results.save_to_file("test_results.json")
```

## 🏃‍♂️ Test Runner

### `TestRunner`

Main class for discovering and running tests.

```python
class TestRunner:
    def __init__(self, config: Config)
```

#### Methods

##### `run_tests() -> TestResults`

Discover and run all tests.

```python
def run_tests(
    self,
    path: Optional[Path] = None,
    pattern: str = "test_*.py",
    tags: Optional[List[str]] = None,
    verbose: bool = False
) -> TestResults
```

**Parameters:**

| Parameter | Type                | Default       | Description           |
| --------- | ------------------- | ------------- | --------------------- |
| `path`    | `Path \| None`      | `None`        | Path to test files    |
| `pattern` | `str`               | `"test_*.py"` | File pattern to match |
| `tags`    | `List[str] \| None` | `None`        | Filter by tags        |
| `verbose` | `bool`              | `False`       | Enable verbose output |

**Example:**

```python
runner = TestRunner(config)
results = runner.run_tests(
    path=Path("tests/"),
    pattern="test_*.py",
    tags=["integration"],
    verbose=True
)
```

##### `discover_tests() -> List[TestCase]`

Discover test functions in files.

```python
def discover_tests(
    self,
    path: Optional[Path] = None,
    pattern: str = "test_*.py"
) -> List[TestCase]
```

## 📝 Test Case

### `TestCase`

Represents a discovered test case.

```python
@dataclass
class TestCase:
    name: str
    function: Callable
    criteria: List[str]
    tags: List[str] = field(default_factory=list)
    timeout: Optional[int] = None
    retry_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    module: Optional[str] = None
    file_path: Optional[str] = None
```

## 🔧 Utility Functions

### Test Registry Functions

#### `get_registered_tests() -> Dict[str, TestCase]`

Get all registered test cases.

```python
from agent_test.core.decorators import get_registered_tests

tests = get_registered_tests()
for test_id, test_case in tests.items():
    print(f"Test: {test_case.name}")
```

#### `clear_test_registry() -> None`

Clear the test registry (useful for testing).

```python
from agent_test.core.decorators import clear_test_registry

clear_test_registry()
```

#### `is_agent_test(func: Callable) -> bool`

Check if a function is marked as an agent test.

```python
from agent_test.core.decorators import is_agent_test

if is_agent_test(my_function):
    print("This is an agent test")
```

#### `get_test_case(func: Callable) -> Optional[TestCase]`

Get the test case for a function.

```python
from agent_test.core.decorators import get_test_case

test_case = get_test_case(my_test_function)
if test_case:
    print(f"Test criteria: {test_case.criteria}")
```

## 🚨 Exceptions

### `AgentTestError`

Base exception for AgentTest errors.

```python
class AgentTestError(Exception):
    """Base exception for AgentTest."""
    pass
```

### `EvaluationError`

Exception for evaluation-related errors.

```python
class EvaluationError(AgentTestError):
    """Exception for evaluation errors."""
    pass
```

### `ConfigurationError`

Exception for configuration-related errors.

```python
class ConfigurationError(AgentTestError):
    """Exception for configuration errors."""
    pass
```

### `GenerationError`

Exception for test generation errors.

```python
class GenerationError(AgentTestError):
    """Exception for test generation errors."""
    pass
```

## 📖 Usage Examples

### Basic Test Setup

```python
from agent_test import agent_test, Config, TestRunner

# Configure AgentTest
config = Config.load()

# Define a test
@agent_test(criteria=['similarity'])
def test_my_agent():
    return {
        "input": "Hello",
        "actual": "Hello world",
        "expected": "Hello world"
    }

# Run tests
runner = TestRunner(config)
results = runner.run_tests()

# Check results
if results.has_failures():
    print("Tests failed!")
else:
    print("All tests passed!")
```

### Custom Evaluator Registration

```python
from agent_test import Config, EvaluatorRegistry
from agent_test.evaluators.base import BaseEvaluator, EvaluationResult

class CustomEvaluator(BaseEvaluator):
    @property
    def name(self) -> str:
        return "custom"

    def evaluate(self, test_output) -> EvaluationResult:
        # Custom evaluation logic
        return EvaluationResult(passed=True, score=1.0)

# Register custom evaluator
config = Config.load()
registry = EvaluatorRegistry(config)
registry.register_evaluator('custom', CustomEvaluator())
```

### Advanced Configuration

```python
from agent_test import Config, EvaluatorConfig, LLMConfig

# Create configuration programmatically
config = Config(
    project_name="My AI Project",
    evaluators=[
        EvaluatorConfig(
            name="similarity",
            type="string_similarity",
            config={"threshold": 0.8},
            weight=1.0
        ),
        EvaluatorConfig(
            name="llm_judge",
            type="llm_as_judge",
            config={"criteria": ["accuracy", "clarity"]},
            weight=2.0
        )
    ],
    llm=LLMConfig(
        provider="openai",
        model="gpt-4",
        temperature=0.0
    )
)

# Save configuration
config.save(".agenttest/config.yaml")
```
