"""
Test decorators for AgentTest.

Provides the @agent_test decorator similar to pytest's structure.
"""

import functools
import inspect
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Union

# Global registry for discovered tests
_test_registry: Dict[str, "TestCase"] = {}


@dataclass
class TestCase:
    """Represents a test case discovered by AgentTest."""

    name: str
    function: Callable
    criteria: List[str]
    tags: List[str] = field(default_factory=list)
    timeout: Optional[int] = None
    retry_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    module: Optional[str] = None
    file_path: Optional[str] = None


def agent_test(
    criteria: Optional[Union[str, List[str]]] = None,
    tags: Optional[Union[str, List[str]]] = None,
    timeout: Optional[int] = None,
    retry_count: int = 0,
    **metadata,
) -> Callable:
    """
    Decorator to mark functions as agent tests.

    Args:
        criteria: Evaluation criteria to use (e.g., ["similarity", "llm_judge"])
        tags: Tags for test categorization
        timeout: Test timeout in seconds
        retry_count: Number of retries on failure
        **metadata: Additional metadata for the test

    Returns:
        Decorated function

    Example:
        @agent_test(criteria=["similarity", "llm_judge"], tags=["summarization"])
        def test_my_agent():
            return {"input": "test", "actual": "result", "expected": "result"}
    """

    def decorator(func: Callable) -> Callable:
        # Normalize criteria
        if criteria is None:
            test_criteria = ["similarity"]  # Default evaluator
        elif isinstance(criteria, str):
            test_criteria = [criteria]
        else:
            test_criteria = list(criteria)

        # Normalize tags
        if tags is None:
            test_tags = []
        elif isinstance(tags, str):
            test_tags = [tags]
        else:
            test_tags = list(tags)

        # Get module and file information
        frame = inspect.currentframe().f_back
        module_name = frame.f_globals.get("__name__", "unknown")
        file_path = frame.f_globals.get("__file__", "unknown")

        # Create test case
        test_case = TestCase(
            name=func.__name__,
            function=func,
            criteria=test_criteria,
            tags=test_tags,
            timeout=timeout,
            retry_count=retry_count,
            metadata=metadata,
            module=module_name,
            file_path=file_path,
        )

        # Register the test
        test_id = f"{module_name}::{func.__name__}"
        _test_registry[test_id] = test_case

        # Mark the function as a test
        func._agenttest_marker = True
        func._agenttest_case = test_case

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator


def get_registered_tests() -> Dict[str, TestCase]:
    """Get all registered tests."""
    return _test_registry.copy()


def clear_test_registry() -> None:
    """Clear the test registry (useful for testing)."""
    global _test_registry
    _test_registry = {}


def is_agent_test(func: Callable) -> bool:
    """Check if a function is marked as an agent test."""
    return hasattr(func, "_agenttest_marker") and func._agenttest_marker


def get_test_case(func: Callable) -> Optional[TestCase]:
    """Get the test case for a function."""
    if hasattr(func, "_agenttest_case"):
        return func._agenttest_case
    return None


# Utility functions for test results
@dataclass
class TestResult:
    """Represents the result of a test execution."""

    test_name: str
    passed: bool
    score: Optional[float] = None
    duration: float = 0.0
    error: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)
    evaluations: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TestResults:
    """Collection of test results."""

    test_results: List[TestResult] = field(default_factory=list)
    summary: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_result(self, result: TestResult) -> None:
        """Add a test result."""
        self.test_results.append(result)

    def has_failures(self) -> bool:
        """Check if any tests failed."""
        return any(not result.passed for result in self.test_results)

    def get_pass_rate(self) -> float:
        """Get the pass rate as a percentage."""
        if not self.test_results:
            return 0.0
        passed = sum(1 for result in self.test_results if result.passed)
        return (passed / len(self.test_results)) * 100

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the test results."""
        total = len(self.test_results)
        passed = sum(1 for result in self.test_results if result.passed)
        failed = total - passed

        avg_score = None
        if self.test_results:
            scores = [r.score for r in self.test_results if r.score is not None]
            if scores:
                avg_score = sum(scores) / len(scores)

        total_duration = sum(result.duration for result in self.test_results)

        return {
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": self.get_pass_rate(),
            "average_score": avg_score,
            "total_duration": total_duration,
        }

    def save_to_file(self, file_path: str) -> None:
        """Save results to a JSON file."""
        import json
        from pathlib import Path

        data = {
            "summary": self.get_summary(),
            "metadata": self.metadata,
            "test_results": [
                {
                    "test_name": result.test_name,
                    "passed": result.passed,
                    "score": result.score,
                    "duration": result.duration,
                    "error": result.error,
                    "details": result.details,
                    "evaluations": result.evaluations,
                }
                for result in self.test_results
            ],
        }

        Path(file_path).write_text(json.dumps(data, indent=2))
