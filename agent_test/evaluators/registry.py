"""
Evaluator registry for AgentTest.

Manages and provides access to all available evaluators.
"""

from typing import Any, Dict, Optional

from ..core.config import Config
from .base import (
    BaseEvaluator,
    ContainsEvaluator,
    RegexEvaluator,
    StringSimilarityEvaluator,
)
from .llm_judge import LLMJudgeEvaluator
from .metrics import MetricsEvaluator


class EvaluatorRegistry:
    """Registry for managing evaluators."""

    def __init__(self, config: Config):
        self.config = config
        self._evaluators: Dict[str, BaseEvaluator] = {}
        self._register_default_evaluators()

    def _register_default_evaluators(self):
        """Register default evaluators."""
        # String similarity evaluator
        similarity_config = self._get_evaluator_config("similarity")
        self._evaluators["similarity"] = StringSimilarityEvaluator(similarity_config)
        self._evaluators["string_similarity"] = self._evaluators["similarity"]  # Alias

        # Regex evaluator
        regex_config = self._get_evaluator_config("regex")
        self._evaluators["regex"] = RegexEvaluator(regex_config)

        # Metrics evaluator (ROUGE, BLEU, METEOR)
        metrics_config = self._get_evaluator_config("metrics")
        self._evaluators["metrics"] = MetricsEvaluator(metrics_config)

        # Contains evaluator (from base module)
        contains_config = self._get_evaluator_config("contains")
        self._evaluators["contains"] = ContainsEvaluator(contains_config)

        # LLM judge evaluator
        llm_config = self._get_evaluator_config("llm_judge")
        if llm_config:
            # Add global LLM config
            if hasattr(self.config, "llm"):
                llm_config.update(
                    {
                        "provider": self.config.llm.provider,
                        "model": self.config.llm.model,
                        "api_key": self.config.llm.api_key,
                        "temperature": self.config.llm.temperature,
                    }
                )
        else:
            llm_config = {}
            if hasattr(self.config, "llm"):
                llm_config = {
                    "provider": self.config.llm.provider,
                    "model": self.config.llm.model,
                    "api_key": self.config.llm.api_key,
                    "temperature": self.config.llm.temperature,
                }

        try:
            self._evaluators["llm_judge"] = LLMJudgeEvaluator(llm_config)
        except Exception as e:
            # LLM judge might fail if API keys are not available
            # This is okay for MVP - other evaluators will still work
            print(f"Warning: Could not initialize LLM judge evaluator: {e}")

    def _get_evaluator_config(self, evaluator_name: str) -> Dict[str, Any]:
        """Get configuration for a specific evaluator."""
        for evaluator_config in self.config.evaluators:
            if (
                evaluator_config.name == evaluator_name
                or evaluator_config.type == evaluator_name
            ):
                return evaluator_config.config
        return {}

    def get_evaluator(self, name: str) -> Optional[BaseEvaluator]:
        """Get an evaluator by name."""
        return self._evaluators.get(name)

    def register_evaluator(self, name: str, evaluator: BaseEvaluator):
        """Register a custom evaluator."""
        self._evaluators[name] = evaluator

    def list_evaluators(self) -> Dict[str, str]:
        """List all available evaluators."""
        return {
            name: evaluator.__class__.__name__
            for name, evaluator in self._evaluators.items()
        }

    def evaluate_with_multiple(
        self, test_output: Any, criteria: list
    ) -> Dict[str, Any]:
        """Evaluate test output with multiple evaluators."""
        results = {}

        for criterion in criteria:
            evaluator = self.get_evaluator(criterion)
            if evaluator:
                try:
                    result = evaluator.evaluate(test_output)
                    results[criterion] = result.to_dict()
                except Exception as e:
                    results[criterion] = {
                        "error": f"Evaluation failed: {str(e)}",
                        "passed": False,
                    }
            else:
                results[criterion] = {
                    "error": f"Evaluator '{criterion}' not found",
                    "passed": False,
                }

        return results


# Additional specialized evaluators


class MetricEvaluator(BaseEvaluator):
    """Evaluator for numeric metrics."""

    @property
    def name(self) -> str:
        return "metric"

    def evaluate(self, test_output: Any) -> dict:
        """Evaluate based on numeric metrics."""
        try:
            from .base import EvaluationResult

            data = self._extract_test_data(test_output)
            actual = data.get("actual")
            expected = data.get("expected")
            metric_type = self._get_config_value("type", "mse")
            threshold = self._get_config_value("threshold", 0.1)

            if actual is None or expected is None:
                return EvaluationResult(
                    passed=False,
                    error="Both 'actual' and 'expected' values required for metric evaluation",
                )

            try:
                actual_val = float(actual)
                expected_val = float(expected)
            except (ValueError, TypeError):
                return EvaluationResult(
                    passed=False, error="Values must be numeric for metric evaluation"
                )

            if metric_type == "mse":
                error = (actual_val - expected_val) ** 2
                score = max(0, 1 - error)
            elif metric_type == "mae":
                error = abs(actual_val - expected_val)
                score = max(0, 1 - error)
            elif metric_type == "relative":
                if expected_val == 0:
                    error = abs(actual_val)
                else:
                    error = abs((actual_val - expected_val) / expected_val)
                score = max(0, 1 - error)
            else:
                return EvaluationResult(
                    passed=False, error=f"Unknown metric type: {metric_type}"
                )

            passed = error <= threshold

            return EvaluationResult(
                passed=passed,
                score=score,
                threshold=threshold,
                details={
                    "actual": actual_val,
                    "expected": expected_val,
                    "error": error,
                    "metric_type": metric_type,
                },
            )

        except Exception as e:
            from .base import EvaluationResult

            return EvaluationResult(
                passed=False, error=f"Metric evaluation failed: {str(e)}"
            )


# Removed - using ContainsEvaluator from base.py instead


# Register additional evaluators in the default registry
def register_additional_evaluators(registry: EvaluatorRegistry):
    """Register additional specialized evaluators."""

    # Metric evaluator
    metric_config = registry._get_evaluator_config("metric")
    registry.register_evaluator("metric", MetricEvaluator(metric_config))

    # Contains evaluator (already registered in _register_default_evaluators)
    # No need to register again


# Monkey patch to add additional evaluators
def _patched_init(self, config: Config):
    """Patched init to include additional evaluators."""
    self.config = config
    self._evaluators: Dict[str, BaseEvaluator] = {}
    self._register_default_evaluators()
    register_additional_evaluators(self)


# Apply the patch
EvaluatorRegistry.__init__ = _patched_init
