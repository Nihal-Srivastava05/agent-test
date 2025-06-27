"""
Test runner for AgentTest.

Handles test discovery, execution, and evaluation.
"""

import importlib
import sys
import time
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..evaluators.registry import EvaluatorRegistry
from ..utils.exceptions import TestDiscoveryError
from .config import Config
from .decorators import TestCase, TestResult, TestResults, get_registered_tests
from .logging import get_logger, setup_logger


class TestRunner:
    """Main test runner for AgentTest."""

    def __init__(self, config: Config):
        self.config = config
        self.evaluator_registry = EvaluatorRegistry(config)
        self.logger = get_logger()

    def run_tests(
        self,
        path: Optional[Path] = None,
        pattern: str = "test_*.py",
        tags: Optional[List[str]] = None,
        verbose: bool = False,
    ) -> TestResults:
        """
        Run tests based on discovery criteria.

        Args:
            path: Path to test files or directory
            pattern: File pattern for test discovery
            tags: Only run tests with these tags
            verbose: Enable verbose output

        Returns:
            TestResults object containing all results
        """
        # Setup logger for this run
        self.logger = setup_logger(verbose=verbose, quiet=False)

        # Log session start
        self.logger.session_started(
            {"pattern": pattern, "tags": tags, "path": str(path) if path else None}
        )

        # Discover tests
        if path:
            self.logger.discovery_started(str(path), pattern)
        else:
            self.logger.discovery_started("test directories", pattern)

        test_cases = self.discover_tests(path, pattern)

        # Filter by tags if specified
        if tags:
            test_cases = [
                tc for tc in test_cases if any(tag in tc.tags for tag in tags)
            ]

        self.logger.discovery_completed(len(test_cases), len(test_cases))

        if not test_cases:
            self.logger.warning("DISCOVERY", "No tests found matching criteria")
            return TestResults()

        results = TestResults()

        # Execute tests
        for i, test_case in enumerate(test_cases):
            self.logger.test_started(test_case.name, len(test_cases))

            result = self.execute_test(test_case, verbose)
            results.add_result(result)

            # Log test completion
            self.logger.test_completed(
                test_case.name,
                result.passed,
                result.duration,
                result.score,
                result.error,
            )

        # Add metadata
        results.metadata = {
            "config": self.config.dict(),
            "timestamp": time.time(),
            "pattern": pattern,
            "tags": tags,
            "verbose": verbose,
        }

        # Log session completion
        self.logger.session_completed(results.get_summary())

        return results

    def discover_tests(
        self, path: Optional[Path] = None, pattern: str = "test_*.py"
    ) -> List[TestCase]:
        """
        Discover test cases in the specified path.

        Args:
            path: Path to search for tests
            pattern: File pattern to match

        Returns:
            List of discovered test cases
        """
        if path is None:
            # Use configured test directories
            test_dirs = [Path(d) for d in self.config.testing.test_dirs]
        elif path.is_file():
            # Single file
            test_dirs = [path.parent]
            pattern = path.name
        else:
            # Directory
            test_dirs = [path]

        test_cases = []

        for test_dir in test_dirs:
            if not test_dir.exists():
                continue

            # Find test files
            if pattern.endswith(".py"):
                # Specific file pattern
                test_files = list(test_dir.glob(pattern))
            else:
                # Multiple patterns
                test_files = []
                for pat in self.config.testing.test_patterns:
                    test_files.extend(test_dir.glob(pat))

            # Import modules and discover tests
            for test_file in test_files:
                try:
                    module_tests = self._import_and_discover(test_file)
                    test_cases.extend(module_tests)
                except Exception as e:
                    raise TestDiscoveryError(
                        f"Failed to discover tests in {test_file}: {e}"
                    )

        return test_cases

    def _import_and_discover(self, test_file: Path) -> List[TestCase]:
        """Import a test file and discover test functions."""
        # Add the test file's directory to Python path
        test_dir = test_file.parent
        if str(test_dir) not in sys.path:
            sys.path.insert(0, str(test_dir))

        try:
            # Import the module
            module_name = test_file.stem
            spec = importlib.util.spec_from_file_location(module_name, test_file)
            module = importlib.util.module_from_spec(spec)

            # Clear registry before importing to avoid conflicts
            from .decorators import clear_test_registry

            clear_test_registry()

            # Execute the module to register tests
            spec.loader.exec_module(module)

            # Get registered tests
            registered_tests = get_registered_tests()

            # Convert to TestCase objects with updated file path
            test_cases = []
            for test_id, test_case in registered_tests.items():
                test_case.file_path = str(test_file)
                test_cases.append(test_case)

            return test_cases

        except Exception as e:
            raise TestDiscoveryError(f"Failed to import {test_file}: {e}")
        finally:
            # Remove from path
            if str(test_dir) in sys.path:
                sys.path.remove(str(test_dir))

    def execute_test(self, test_case: TestCase, verbose: bool = False) -> TestResult:
        """
        Execute a single test case.

        Args:
            test_case: Test case to execute
            verbose: Enable verbose output

        Returns:
            TestResult object
        """
        start_time = time.time()

        try:
            if verbose:
                print(f"  📝 Executing test function: {test_case.name}")

            # Execute the test function
            test_output = test_case.function()

            if verbose:
                print(f"  📊 Evaluating with criteria: {test_case.criteria}")

            # Evaluate the results
            evaluations = self._evaluate_test_output(
                test_output, test_case.criteria, verbose
            )

            # Determine if test passed
            passed = self._determine_pass_status(evaluations)

            # Calculate overall score
            score = self._calculate_overall_score(evaluations)

            duration = time.time() - start_time

            # Create detailed test result
            result = TestResult(
                test_name=test_case.name,
                passed=passed,
                score=score,
                duration=duration,
                evaluations=evaluations,
                details={
                    "test_output": test_output,
                    "criteria": test_case.criteria,
                    "tags": test_case.tags,
                    "file_path": test_case.file_path,
                    "timeout": test_case.timeout,
                },
            )

            if verbose:
                status = "✅ PASSED" if passed else "❌ FAILED"
                print(f"  {status} - Score: {score}, Duration: {duration:.3f}s")
                if not passed:
                    print(
                        f"  💥 Failure reason: {self._get_failure_summary(evaluations)}"
                    )

            return result

        except Exception as e:
            duration = time.time() - start_time
            error_message = f"Test execution failed: {str(e)}"

            if verbose:
                print(f"  ❌ EXCEPTION: {error_message}")
                print("  📍 Traceback:")
                traceback.print_exc()

            return TestResult(
                test_name=test_case.name,
                passed=False,
                score=None,
                duration=duration,
                error=error_message,
                evaluations={},
                details={
                    "exception_type": type(e).__name__,
                    "traceback": traceback.format_exc(),
                    "criteria": test_case.criteria,
                    "tags": test_case.tags,
                    "file_path": test_case.file_path,
                },
            )

    def _get_failure_summary(self, evaluations: Dict[str, Any]) -> str:
        """Get a brief summary of why the test failed."""
        failure_reasons = []

        for criterion, result in evaluations.items():
            if isinstance(result, dict):
                if result.get("error"):
                    failure_reasons.append(f"{criterion}: {result['error']}")
                elif not result.get("passed", True):
                    if "details" in result and "reason" in result["details"]:
                        failure_reasons.append(
                            f"{criterion}: {result['details']['reason']}"
                        )
                    elif "score" in result and "threshold" in result:
                        failure_reasons.append(
                            f"{criterion}: Score {result['score']:.3f} below threshold {result['threshold']}"
                        )
                    else:
                        failure_reasons.append(f"{criterion}: Failed evaluation")

        return (
            "; ".join(failure_reasons) if failure_reasons else "Unknown failure reason"
        )

    def _evaluate_test_output(
        self, test_output: Any, criteria: List[str], verbose: bool = False
    ) -> Dict[str, Any]:
        """Evaluate test output using specified criteria."""
        evaluations = {}

        for criterion in criteria:
            try:
                if verbose:
                    print(f"    🔍 Running {criterion} evaluator...")

                evaluator = self.evaluator_registry.get_evaluator(criterion)
                if evaluator:
                    evaluation_result = evaluator.evaluate(test_output)

                    # Convert EvaluationResult to dict if needed
                    if hasattr(evaluation_result, "to_dict"):
                        evaluations[criterion] = evaluation_result.to_dict()
                    else:
                        evaluations[criterion] = evaluation_result

                    if verbose:
                        result_dict = evaluations[criterion]
                        if result_dict.get("passed"):
                            print(f"    ✅ {criterion}: PASSED")
                        else:
                            print(f"    ❌ {criterion}: FAILED")
                            if result_dict.get("error"):
                                print(f"       Error: {result_dict['error']}")
                            elif "score" in result_dict and "threshold" in result_dict:
                                print(
                                    f"       Score: {result_dict['score']:.3f}, Threshold: {result_dict['threshold']}"
                                )
                else:
                    error_msg = f"Evaluator '{criterion}' not found"
                    evaluations[criterion] = {"error": error_msg}
                    if verbose:
                        print(f"    ❌ {criterion}: {error_msg}")

            except Exception as e:
                error_msg = f"Evaluation failed: {str(e)}"
                evaluations[criterion] = {"error": error_msg}
                if verbose:
                    print(f"    ❌ {criterion}: {error_msg}")
                    traceback.print_exc()

        return evaluations

    def _determine_pass_status(self, evaluations: Dict[str, Any]) -> bool:
        """Determine if test passed based on evaluations."""
        for criterion, result in evaluations.items():
            if isinstance(result, dict):
                if result.get("error"):
                    return False
                if "passed" in result and not result["passed"]:
                    return False
                if "score" in result and result["score"] is not None:
                    # Use threshold from evaluator config or default 0.8
                    threshold = result.get("threshold", 0.8)
                    if threshold is not None and result["score"] < threshold:
                        return False

        return True

    def _calculate_overall_score(self, evaluations: Dict[str, Any]) -> Optional[float]:
        """Calculate overall score from evaluations."""
        scores = []
        weights = []

        for criterion, result in evaluations.items():
            if (
                isinstance(result, dict)
                and "score" in result
                and not result.get("error")
            ):
                score = result["score"]
                if score is not None:  # Only include non-None scores
                    scores.append(score)
                    # Get weight from evaluator config
                    evaluator_config = self.config.get_evaluator(criterion)
                    weight = evaluator_config.weight if evaluator_config else 1.0
                    weights.append(weight)

        if not scores:
            return None

        # Weighted average
        if weights:
            weighted_sum = sum(score * weight for score, weight in zip(scores, weights))
            total_weight = sum(weights)
            return weighted_sum / total_weight
        else:
            return sum(scores) / len(scores)


def run_test(
    agent_func,
    input_data: Any,
    expected: Any = None,
    criteria: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Utility function to run a single test directly.

    Args:
        agent_func: Function to test
        input_data: Input to pass to the function
        expected: Expected output (optional)
        criteria: Evaluation criteria to use

    Returns:
        Test result data
    """
    try:
        actual = agent_func(input_data)

        result = {"input": input_data, "actual": actual}

        if expected is not None:
            result["expected"] = expected

        return result

    except Exception as e:
        return {"input": input_data, "error": str(e), "actual": None}
