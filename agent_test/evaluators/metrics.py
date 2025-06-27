"""
Metrics evaluator for AgentTest.

Provides support for common NLP evaluation metrics like ROUGE, BLEU, and METEOR.
"""

from typing import Any, Dict

from .base import BaseEvaluator, EvaluationResult


class MetricsEvaluator(BaseEvaluator):
    """Evaluator for NLP metrics like ROUGE, BLEU, METEOR."""

    @property
    def name(self) -> str:
        return "metrics"

    def evaluate(self, test_output: Any) -> EvaluationResult:
        """Evaluate using specified NLP metrics."""
        try:
            data = self._extract_test_data(test_output)

            actual = data.get("actual", "")
            reference = data.get("reference", data.get("expected", ""))
            metrics_config = data.get("metrics", {})

            if not actual or not reference:
                return EvaluationResult(
                    passed=False,
                    error="Both 'actual' and 'reference' texts are required for metrics evaluation",
                )

            if not metrics_config:
                return EvaluationResult(
                    passed=False, error="No metrics configuration found in test output"
                )

            # Evaluate all requested metrics
            metric_results = {}
            overall_passed = True
            overall_score = 0.0
            metric_count = 0

            for metric_name, metric_config in metrics_config.items():
                if metric_name == "rouge":
                    result = self._evaluate_rouge(actual, reference, metric_config)
                elif metric_name == "bleu":
                    result = self._evaluate_bleu(actual, reference, metric_config)
                elif metric_name == "meteor":
                    result = self._evaluate_meteor(actual, reference, metric_config)
                else:
                    result = {
                        "passed": False,
                        "error": f"Unknown metric: {metric_name}",
                        "score": 0.0,
                    }

                metric_results[metric_name] = result

                if not result["passed"]:
                    overall_passed = False

                if "score" in result:
                    overall_score += result["score"]
                    metric_count += 1

            # Calculate average score and threshold
            final_score = overall_score / metric_count if metric_count > 0 else 0.0

            # Calculate average threshold from all metrics
            total_threshold = 0.0
            threshold_count = 0
            for metric_result in metric_results.values():
                if isinstance(metric_result, dict) and "threshold" in metric_result:
                    total_threshold += metric_result["threshold"]
                    threshold_count += 1

            average_threshold = (
                total_threshold / threshold_count if threshold_count > 0 else None
            )

            return EvaluationResult(
                passed=overall_passed,
                score=final_score,
                threshold=average_threshold,
                details={
                    "actual": actual,
                    "reference": reference,
                    "metric_results": metric_results,
                    "overall_score": final_score,
                },
            )

        except Exception as e:
            return EvaluationResult(
                passed=False, error=f"Metrics evaluation failed: {str(e)}"
            )

    def _evaluate_rouge(
        self, actual: str, reference: str, config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Evaluate using ROUGE metrics."""
        try:
            # Try to import rouge-score library
            try:
                from rouge_score import rouge_scorer

                has_rouge = True
            except ImportError:
                has_rouge = False

            if not has_rouge:
                # Fallback to simple word overlap approximation
                return self._rouge_fallback(actual, reference, config)

            # Use proper ROUGE scoring
            variants = config.get("variants", ["rouge1", "rouge2", "rougeL"])
            min_score = config.get("min_score", 0.4)

            # Map variants to correct rouge-score format
            rouge_variants = []
            for variant in variants:
                if variant in ["rouge-1", "rouge1"]:
                    rouge_variants.append("rouge1")
                elif variant in ["rouge-2", "rouge2"]:
                    rouge_variants.append("rouge2")
                elif variant in ["rouge-l", "rougeL", "rouge_l"]:
                    rouge_variants.append("rougeL")
                else:
                    rouge_variants.append(variant)

            scorer = rouge_scorer.RougeScorer(rouge_variants, use_stemmer=True)
            scores = scorer.score(reference, actual)

            # Calculate average F1 score across variants
            f1_scores = [scores[variant].fmeasure for variant in rouge_variants]
            avg_score = sum(f1_scores) / len(f1_scores)

            return {
                "passed": avg_score >= min_score,
                "score": avg_score,
                "threshold": min_score,
                "details": {
                    "rouge_scores": {
                        variant: {
                            "precision": scores[variant].precision,
                            "recall": scores[variant].recall,
                            "f1": scores[variant].fmeasure,
                        }
                        for variant in rouge_variants
                    },
                    "average_f1": avg_score,
                },
            }

        except Exception as e:
            return {
                "passed": False,
                "error": f"ROUGE evaluation failed: {str(e)}",
                "score": 0.0,
            }

    def _rouge_fallback(
        self, actual: str, reference: str, config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Fallback ROUGE implementation using word overlap."""
        min_score = config.get("min_score", 0.4)

        # Tokenize
        actual_words = set(actual.lower().split())
        reference_words = set(reference.lower().split())

        # Calculate overlap
        overlap = len(actual_words & reference_words)

        # Calculate precision and recall first
        precision = overlap / len(actual_words) if actual_words else 0
        recall = overlap / len(reference_words) if reference_words else 0

        # Simple F1-like score
        if precision + recall == 0:
            score = 0.0
        else:
            score = 2 * (precision * recall) / (precision + recall)

        return {
            "passed": score >= min_score,
            "score": score,
            "threshold": min_score,
            "details": {
                "method": "word_overlap_fallback",
                "precision": precision,
                "recall": recall,
                "f1": score,
                "note": "Install rouge-score package for proper ROUGE evaluation",
            },
        }

    def _evaluate_bleu(
        self, actual: str, reference: str, config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Evaluate using BLEU score."""
        try:
            # Try to import nltk for BLEU
            try:
                import nltk
                from nltk.translate.bleu_score import SmoothingFunction, sentence_bleu

                # Download required NLTK data if not available
                try:
                    nltk.data.find("tokenizers/punkt")
                except LookupError:
                    nltk.download("punkt", quiet=True)

                has_nltk = True
            except ImportError:
                has_nltk = False

            if not has_nltk:
                return self._bleu_fallback(actual, reference, config)

            min_score = config.get("min_score", 0.3)
            use_smoothing = config.get("smoothing", True)

            # Tokenize
            reference_tokens = reference.lower().split()
            actual_tokens = actual.lower().split()

            # Calculate BLEU score
            smoothing_function = SmoothingFunction().method1 if use_smoothing else None
            bleu_score = sentence_bleu(
                [reference_tokens], actual_tokens, smoothing_function=smoothing_function
            )

            return {
                "passed": bleu_score >= min_score,
                "score": bleu_score,
                "threshold": min_score,
                "details": {"bleu_score": bleu_score, "smoothing": use_smoothing},
            }

        except Exception as e:
            return {
                "passed": False,
                "error": f"BLEU evaluation failed: {str(e)}",
                "score": 0.0,
            }

    def _bleu_fallback(
        self, actual: str, reference: str, config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Fallback BLEU implementation."""
        min_score = config.get("min_score", 0.3)

        # Simple n-gram overlap approximation
        actual_words = actual.lower().split()
        reference_words = reference.lower().split()

        # Calculate 1-gram precision
        matches = 0
        for word in actual_words:
            if word in reference_words:
                matches += 1

        precision = matches / len(actual_words) if actual_words else 0

        # Apply length penalty (simplified)
        length_penalty = (
            min(1.0, len(actual_words) / len(reference_words)) if reference_words else 0
        )

        bleu_approx = precision * length_penalty

        return {
            "passed": bleu_approx >= min_score,
            "score": bleu_approx,
            "threshold": min_score,
            "details": {
                "method": "simple_approximation",
                "precision": precision,
                "length_penalty": length_penalty,
                "score": bleu_approx,
                "note": "Install nltk package for proper BLEU evaluation",
            },
        }

    def _evaluate_meteor(
        self, actual: str, reference: str, config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Evaluate using METEOR score."""
        try:
            # Try to import nltk for METEOR
            try:
                import nltk
                from nltk.translate.meteor_score import meteor_score

                # Download required NLTK data
                try:
                    nltk.data.find("corpora/wordnet")
                except LookupError:
                    nltk.download("wordnet", quiet=True)

                has_nltk = True
            except ImportError:
                has_nltk = False

            if not has_nltk:
                return self._meteor_fallback(actual, reference, config)

            min_score = config.get("min_score", 0.4)

            # Calculate METEOR score
            meteor_score_val = meteor_score(
                [reference.lower().split()], actual.lower().split()
            )

            return {
                "passed": meteor_score_val >= min_score,
                "score": meteor_score_val,
                "threshold": min_score,
                "details": {"meteor_score": meteor_score_val},
            }

        except Exception as e:
            return {
                "passed": False,
                "error": f"METEOR evaluation failed: {str(e)}",
                "score": 0.0,
            }

    def _meteor_fallback(
        self, actual: str, reference: str, config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Fallback METEOR implementation."""
        min_score = config.get("min_score", 0.4)

        # Simple word overlap with order consideration
        actual_words = actual.lower().split()
        reference_words = reference.lower().split()

        # Calculate matches
        matches = 0
        for word in actual_words:
            if word in reference_words:
                matches += 1

        # Precision and recall
        precision = matches / len(actual_words) if actual_words else 0
        recall = matches / len(reference_words) if reference_words else 0

        # F-mean (simplified METEOR approximation)
        if precision + recall == 0:
            meteor_approx = 0.0
        else:
            meteor_approx = (precision * recall) / (0.5 * precision + 0.5 * recall)

        return {
            "passed": meteor_approx >= min_score,
            "score": meteor_approx,
            "threshold": min_score,
            "details": {
                "method": "simple_approximation",
                "precision": precision,
                "recall": recall,
                "score": meteor_approx,
                "note": "Install nltk package for proper METEOR evaluation",
            },
        }
