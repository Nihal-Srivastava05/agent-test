"""
Test runner for AgentTest.

Handles test discovery, execution, and evaluation.
"""

import importlib
import inspect
import sys
import time
import traceback
from pathlib import Path
from typing import List, Dict, Any, Optional, Union

from .config import Config
from .decorators import TestCase, TestResult, TestResults, get_registered_tests, is_agent_test
from ..evaluators.registry import EvaluatorRegistry
from ..utils.exceptions import TestDiscoveryError, TestExecutionError


class TestRunner:
    """Main test runner for AgentTest."""
    
    def __init__(self, config: Config):
        self.config = config
        self.evaluator_registry = EvaluatorRegistry(config)
    
    def run_tests(
        self,
        path: Optional[Path] = None,
        pattern: str = "test_*.py",
        tags: Optional[List[str]] = None,
        verbose: bool = False
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
        # Discover tests
        test_cases = self.discover_tests(path, pattern)
        
        # Filter by tags if specified
        if tags:
            test_cases = [tc for tc in test_cases if any(tag in tc.tags for tag in tags)]
        
        if not test_cases:
            return TestResults()
        
        results = TestResults()
        
        # Execute tests
        for test_case in test_cases:
            if verbose:
                print(f"Running {test_case.name}...")
            
            result = self.execute_test(test_case, verbose)
            results.add_result(result)
        
        # Add metadata
        results.metadata = {
            "config": self.config.dict(),
            "timestamp": time.time(),
            "pattern": pattern,
            "tags": tags,
            "verbose": verbose
        }
        
        return results
    
    def discover_tests(
        self, 
        path: Optional[Path] = None, 
        pattern: str = "test_*.py"
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
            if pattern.endswith('.py'):
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
                    raise TestDiscoveryError(f"Failed to discover tests in {test_file}: {e}")
        
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
            # Execute the test function
            test_output = test_case.function()
            
            # Evaluate the results
            evaluations = self._evaluate_test_output(test_output, test_case.criteria)
            
            # Determine if test passed
            passed = self._determine_pass_status(evaluations)
            
            # Calculate overall score
            score = self._calculate_overall_score(evaluations)
            
            duration = time.time() - start_time
            
            return TestResult(
                test_name=test_case.name,
                passed=passed,
                score=score,
                duration=duration,
                details={"output": test_output},
                evaluations=evaluations
            )
            
        except Exception as e:
            duration = time.time() - start_time
            error_msg = f"{type(e).__name__}: {str(e)}"
            
            if verbose:
                error_msg += f"\n{traceback.format_exc()}"
            
            return TestResult(
                test_name=test_case.name,
                passed=False,
                duration=duration,
                error=error_msg
            )
    
    def _evaluate_test_output(
        self, 
        test_output: Any, 
        criteria: List[str]
    ) -> Dict[str, Any]:
        """Evaluate test output using specified criteria."""
        evaluations = {}
        
        for criterion in criteria:
            try:
                evaluator = self.evaluator_registry.get_evaluator(criterion)
                if evaluator:
                    evaluation_result = evaluator.evaluate(test_output)
                    evaluations[criterion] = evaluation_result
                else:
                    evaluations[criterion] = {
                        "error": f"Evaluator '{criterion}' not found"
                    }
            except Exception as e:
                evaluations[criterion] = {
                    "error": f"Evaluation failed: {str(e)}"
                }
        
        return evaluations
    
    def _determine_pass_status(self, evaluations: Dict[str, Any]) -> bool:
        """Determine if test passed based on evaluations."""
        for criterion, result in evaluations.items():
            if isinstance(result, dict):
                if result.get("error"):
                    return False
                if "passed" in result and not result["passed"]:
                    return False
                if "score" in result:
                    # Use threshold from evaluator config or default 0.8
                    threshold = result.get("threshold", 0.8)
                    if result["score"] < threshold:
                        return False
        
        return True
    
    def _calculate_overall_score(self, evaluations: Dict[str, Any]) -> Optional[float]:
        """Calculate overall score from evaluations."""
        scores = []
        weights = []
        
        for criterion, result in evaluations.items():
            if isinstance(result, dict) and "score" in result and not result.get("error"):
                scores.append(result["score"])
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


def run_test(agent_func, input_data: Any, expected: Any = None, criteria: Optional[List[str]] = None) -> Dict[str, Any]:
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
        
        result = {
            "input": input_data,
            "actual": actual
        }
        
        if expected is not None:
            result["expected"] = expected
        
        return result
        
    except Exception as e:
        return {
            "input": input_data,
            "error": str(e),
            "actual": None
        } 