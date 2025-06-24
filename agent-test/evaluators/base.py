"""
Base evaluator classes for AgentTest.

Provides the interface and common functionality for all evaluators.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union, List
from dataclasses import dataclass


@dataclass
class EvaluationResult:
    """Result of an evaluation."""
    passed: bool
    score: Optional[float] = None
    threshold: Optional[float] = None
    details: Dict[str, Any] = None
    error: Optional[str] = None
    
    def __post_init__(self):
        if self.details is None:
            self.details = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "passed": self.passed,
            "score": self.score,
            "threshold": self.threshold,
            "details": self.details,
            "error": self.error
        }


class BaseEvaluator(ABC):
    """Base class for all evaluators."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize evaluator with configuration."""
        self.config = config or {}
    
    @abstractmethod
    def evaluate(self, test_output: Any) -> EvaluationResult:
        """
        Evaluate test output.
        
        Args:
            test_output: Output from test function
            
        Returns:
            EvaluationResult with score and pass/fail status
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the evaluator name."""
        pass
    
    def _extract_test_data(self, test_output: Any) -> Dict[str, Any]:
        """
        Extract standardized test data from various output formats.
        
        Args:
            test_output: Raw test output
            
        Returns:
            Dictionary with standardized keys: input, actual, expected, etc.
        """
        if isinstance(test_output, dict):
            return test_output
        elif isinstance(test_output, list):
            # Handle list of test cases
            return {"test_cases": test_output}
        else:
            # Single value output
            return {"actual": test_output}
    
    def _get_config_value(self, key: str, default: Any = None) -> Any:
        """Get configuration value with default."""
        return self.config.get(key, default)


class StringSimilarityEvaluator(BaseEvaluator):
    """Evaluator for string similarity comparison."""
    
    @property
    def name(self) -> str:
        return "string_similarity"
    
    def evaluate(self, test_output: Any) -> EvaluationResult:
        """Evaluate based on string similarity."""
        try:
            data = self._extract_test_data(test_output)
            
            if "test_cases" in data:
                # Handle multiple test cases
                return self._evaluate_multiple_cases(data["test_cases"])
            else:
                # Single test case
                return self._evaluate_single_case(data)
                
        except Exception as e:
            return EvaluationResult(
                passed=False,
                error=f"String similarity evaluation failed: {str(e)}"
            )
    
    def _evaluate_single_case(self, data: Dict[str, Any]) -> EvaluationResult:
        """Evaluate a single test case."""
        actual = data.get("actual")
        expected = data.get("expected")
        
        if actual is None:
            return EvaluationResult(
                passed=False,
                error="No 'actual' value found in test output"
            )
        
        if expected is None:
            # If no expected value, consider it passed (for open-ended tests)
            return EvaluationResult(
                passed=True,
                score=1.0,
                details={"reason": "No expected value provided"}
            )
        
        # Calculate similarity
        similarity = self._calculate_similarity(str(actual), str(expected))
        threshold = self._get_config_value("threshold", 0.8)
        
        return EvaluationResult(
            passed=similarity >= threshold,
            score=similarity,
            threshold=threshold,
            details={
                "actual": actual,
                "expected": expected,
                "similarity": similarity,
                "method": self._get_config_value("method", "cosine")
            }
        )
    
    def _evaluate_multiple_cases(self, test_cases: List[Dict]) -> EvaluationResult:
        """Evaluate multiple test cases."""
        results = []
        total_score = 0.0
        passed_count = 0
        
        for i, case in enumerate(test_cases):
            result = self._evaluate_single_case(case)
            results.append(result)
            
            if result.score is not None:
                total_score += result.score
            
            if result.passed:
                passed_count += 1
        
        overall_score = total_score / len(test_cases) if test_cases else 0.0
        threshold = self._get_config_value("threshold", 0.8)
        
        return EvaluationResult(
            passed=passed_count == len(test_cases),
            score=overall_score,
            threshold=threshold,
            details={
                "total_cases": len(test_cases),
                "passed_cases": passed_count,
                "individual_results": [r.to_dict() for r in results]
            }
        )
    
    def _calculate_similarity(self, actual: str, expected: str) -> float:
        """Calculate similarity between two strings."""
        method = self._get_config_value("method", "cosine")
        
        if method == "exact":
            return 1.0 if actual == expected else 0.0
        elif method == "levenshtein":
            return self._levenshtein_similarity(actual, expected)
        elif method == "jaccard":
            return self._jaccard_similarity(actual, expected)
        else:  # cosine (default)
            return self._cosine_similarity(actual, expected)
    
    def _cosine_similarity(self, text1: str, text2: str) -> float:
        """Calculate cosine similarity between two texts."""
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity
            
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform([text1, text2])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return float(similarity)
            
        except ImportError:
            # Fallback to simple word overlap
            return self._word_overlap_similarity(text1, text2)
    
    def _levenshtein_similarity(self, text1: str, text2: str) -> float:
        """Calculate Levenshtein similarity."""
        def levenshtein_distance(s1, s2):
            if len(s1) < len(s2):
                return levenshtein_distance(s2, s1)
            
            if len(s2) == 0:
                return len(s1)
            
            previous_row = range(len(s2) + 1)
            for i, c1 in enumerate(s1):
                current_row = [i + 1]
                for j, c2 in enumerate(s2):
                    insertions = previous_row[j + 1] + 1
                    deletions = current_row[j] + 1
                    substitutions = previous_row[j] + (c1 != c2)
                    current_row.append(min(insertions, deletions, substitutions))
                previous_row = current_row
            
            return previous_row[-1]
        
        max_len = max(len(text1), len(text2))
        if max_len == 0:
            return 1.0
        
        distance = levenshtein_distance(text1, text2)
        return 1.0 - (distance / max_len)
    
    def _jaccard_similarity(self, text1: str, text2: str) -> float:
        """Calculate Jaccard similarity."""
        set1 = set(text1.lower().split())
        set2 = set(text2.lower().split())
        
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        return intersection / union if union > 0 else 0.0
    
    def _word_overlap_similarity(self, text1: str, text2: str) -> float:
        """Simple word overlap similarity as fallback."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 and not words2:
            return 1.0
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1.intersection(words2))
        return intersection / max(len(words1), len(words2))


class RegexEvaluator(BaseEvaluator):
    """Evaluator for regex pattern matching."""
    
    @property
    def name(self) -> str:
        return "regex"
    
    def evaluate(self, test_output: Any) -> EvaluationResult:
        """Evaluate based on regex pattern matching."""
        try:
            import re
            
            data = self._extract_test_data(test_output)
            actual = data.get("actual")
            pattern = data.get("pattern") or self._get_config_value("pattern")
            
            if actual is None:
                return EvaluationResult(
                    passed=False,
                    error="No 'actual' value found in test output"
                )
            
            if not pattern:
                return EvaluationResult(
                    passed=False,
                    error="No regex pattern specified"
                )
            
            match = re.search(pattern, str(actual))
            passed = match is not None
            
            return EvaluationResult(
                passed=passed,
                score=1.0 if passed else 0.0,
                details={
                    "actual": actual,
                    "pattern": pattern,
                    "match": match.group() if match else None
                }
            )
            
        except Exception as e:
            return EvaluationResult(
                passed=False,
                error=f"Regex evaluation failed: {str(e)}"
            ) 