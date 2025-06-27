"""
Tests for AgentTest core functionality.

These are pytest tests for the framework itself.
"""

import tempfile
from pathlib import Path

import pytest

from agent_test.core.config import Config
from agent_test.core.decorators import TestResult, TestResults, agent_test
from agent_test.evaluators.base import EvaluationResult, StringSimilarityEvaluator
from agent_test.evaluators.registry import EvaluatorRegistry


class TestConfig:
    """Test configuration management."""

    def test_default_config_creation(self):
        """Test creating default configuration."""
        config = Config.create_default("basic")

        assert config.version == "1.0"
        assert config.llm.provider == "openai"
        assert config.llm.model == "gpt-3.5-turbo"
        assert len(config.evaluators) >= 2  # At least similarity and llm_judge

    def test_langchain_template(self):
        """Test LangChain template configuration."""
        config = Config.create_default("langchain")

        assert len(config.agents) >= 1
        assert config.agents[0].type == "langchain"

    def test_config_save_load(self):
        """Test saving and loading configuration."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "test_config.yaml"

            # Create and save config
            original_config = Config.create_default("basic")
            original_config.save(config_path)

            # Load config
            loaded_config = Config.load(config_path)

            assert loaded_config.version == original_config.version
            assert loaded_config.llm.provider == original_config.llm.provider


class TestDecorators:
    """Test the @agent_test decorator."""

    def test_agent_test_decorator(self):
        """Test basic decorator functionality."""

        @agent_test(criteria=["similarity"], tags=["test"])
        def test_function():
            return {"input": "test", "actual": "result", "expected": "result"}

        # Check that function is marked
        assert hasattr(test_function, "_agenttest_marker")
        assert test_function._agenttest_marker is True

        # Check test case properties
        test_case = test_function._agenttest_case
        assert test_case.name == "test_function"
        assert "similarity" in test_case.criteria
        assert "test" in test_case.tags

    def test_test_results_collection(self):
        """Test TestResults collection."""
        results = TestResults()

        # Add some test results
        result1 = TestResult(test_name="test1", passed=True, score=0.9, duration=1.0)
        result2 = TestResult(
            test_name="test2", passed=False, duration=2.0, error="Test failed"
        )

        results.add_result(result1)
        results.add_result(result2)

        # Check summary
        assert len(results.test_results) == 2
        assert results.has_failures() is True
        assert results.get_pass_rate() == 50.0

        summary = results.get_summary()
        assert summary["total_tests"] == 2
        assert summary["passed"] == 1
        assert summary["failed"] == 1


class TestEvaluators:
    """Test evaluation engines."""

    def test_string_similarity_evaluator(self):
        """Test string similarity evaluation."""
        evaluator = StringSimilarityEvaluator({"method": "exact", "threshold": 1.0})

        # Test exact match
        test_output = {
            "input": "test",
            "actual": "hello world",
            "expected": "hello world",
        }

        result = evaluator.evaluate(test_output)
        assert result.passed is True
        assert result.score == 1.0

        # Test mismatch
        test_output_mismatch = {
            "input": "test",
            "actual": "hello world",
            "expected": "goodbye world",
        }

        result_mismatch = evaluator.evaluate(test_output_mismatch)
        assert result_mismatch.passed is False
        assert result_mismatch.score == 0.0

    def test_string_similarity_no_expected(self):
        """Test string similarity with no expected value."""
        evaluator = StringSimilarityEvaluator()

        test_output = {"input": "test", "actual": "some response"}

        result = evaluator.evaluate(test_output)
        assert result.passed is True  # Should pass when no expected value
        assert result.score == 1.0

    def test_evaluator_registry(self):
        """Test evaluator registry."""
        config = Config.create_default("basic")
        registry = EvaluatorRegistry(config)

        # Check default evaluators are registered
        assert registry.get_evaluator("similarity") is not None
        assert registry.get_evaluator("string_similarity") is not None  # Alias
        assert registry.get_evaluator("regex") is not None

        # Test custom evaluator registration
        custom_evaluator = StringSimilarityEvaluator()
        registry.register_evaluator("custom", custom_evaluator)

        assert registry.get_evaluator("custom") is custom_evaluator


class TestIntegration:
    """Integration tests."""

    def test_simple_agent_test_flow(self):
        """Test a simple end-to-end flow."""

        def simple_agent(text: str) -> str:
            return f"Processed: {text}"

        @agent_test(criteria=["similarity"])
        def test_simple_agent():
            input_text = "hello"
            expected = "Processed: hello"
            actual = simple_agent(input_text)

            return {"input": input_text, "expected": expected, "actual": actual}

        # Execute the test function
        result_data = test_simple_agent()

        # Check result structure
        assert "input" in result_data
        assert "expected" in result_data
        assert "actual" in result_data
        assert result_data["actual"] == "Processed: hello"

    def test_multiple_test_cases(self):
        """Test handling multiple test cases."""

        def echo_agent(text: str) -> str:
            return text

        @agent_test(criteria=["similarity"])
        def test_multiple_cases():
            cases = [
                {"input": "hello", "expected": "hello"},
                {"input": "world", "expected": "world"},
                {"input": "", "expected": ""},
            ]

            results = []
            for case in cases:
                actual = echo_agent(case["input"])
                results.append(
                    {
                        "input": case["input"],
                        "expected": case["expected"],
                        "actual": actual,
                    }
                )

            return results

        # Execute test
        result_data = test_multiple_cases()

        # Check structure
        assert isinstance(result_data, list)
        assert len(result_data) == 3

        for result in result_data:
            assert "input" in result
            assert "expected" in result
            assert "actual" in result


class TestErrorHandling:
    """Test error handling scenarios."""

    def test_missing_actual_value(self):
        """Test handling of missing actual value."""
        evaluator = StringSimilarityEvaluator()

        test_output = {
            "input": "test",
            "expected": "something",
            # Missing "actual"
        }

        result = evaluator.evaluate(test_output)
        assert result.passed is False
        assert result.error is not None
        assert "actual" in result.error

    def test_invalid_test_output(self):
        """Test handling of invalid test output."""
        evaluator = StringSimilarityEvaluator()

        # Test with non-dict output
        result = evaluator.evaluate("invalid output")

        # Should handle gracefully by converting to dict
        assert isinstance(result, EvaluationResult)


if __name__ == "__main__":
    pytest.main([__file__])
