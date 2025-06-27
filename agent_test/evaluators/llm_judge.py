"""
LLM-as-judge evaluator for AgentTest.

Uses LLMs to evaluate test outputs based on criteria.
"""

import json
from typing import Any, Dict, List

from .base import BaseEvaluator, EvaluationResult


class LLMJudgeEvaluator(BaseEvaluator):
    """Evaluator that uses LLM to judge test outputs."""

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.llm_client = None
        self._setup_llm_client()

    @property
    def name(self) -> str:
        return "llm_judge"

    def _setup_llm_client(self):
        """Setup LLM client based on configuration."""
        provider = self._get_config_value("provider", "openai")

        if provider == "openai":
            self._setup_openai_client()
        elif provider == "anthropic":
            self._setup_anthropic_client()
        elif provider == "gemini":
            self._setup_gemini_client()
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

    def _setup_openai_client(self):
        """Setup OpenAI client."""
        try:
            import openai

            api_key = self._get_config_value("api_key")
            if not api_key:
                import os

                api_key = os.getenv("OPENAI_API_KEY")

            if not api_key:
                raise ValueError("OpenAI API key not found")

            self.llm_client = openai.OpenAI(api_key=api_key)
            self.model = self._get_config_value("model", "gpt-3.5-turbo")

        except ImportError:
            raise ImportError(
                "OpenAI package not installed. Install with: pip install openai"
            )

    def _setup_anthropic_client(self):
        """Setup Anthropic client."""
        try:
            import anthropic

            api_key = self._get_config_value("api_key")
            if not api_key:
                import os

                api_key = os.getenv("ANTHROPIC_API_KEY")

            if not api_key:
                raise ValueError("Anthropic API key not found")

            self.llm_client = anthropic.Anthropic(api_key=api_key)
            self.model = self._get_config_value("model", "claude-3-sonnet-20240229")

        except ImportError:
            raise ImportError(
                "Anthropic package not installed. Install with: pip install anthropic"
            )

    def _setup_gemini_client(self):
        """Setup Google Gemini client."""
        try:
            import google.generativeai as genai

            api_key = self._get_config_value("api_key")
            if not api_key:
                import os

                api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

            if not api_key:
                raise ValueError(
                    "Google API key not found. Set GOOGLE_API_KEY or GEMINI_API_KEY environment variable"
                )

            genai.configure(api_key=api_key)
            self.model = self._get_config_value("model", "gemini-pro")
            self.llm_client = genai.GenerativeModel(self.model)

        except ImportError:
            raise ImportError(
                "Google Generative AI package not installed. Install with: pip install google-generativeai"
            )

    def evaluate(self, test_output: Any) -> EvaluationResult:
        """Evaluate test output using LLM as judge."""
        try:
            data = self._extract_test_data(test_output)

            if "test_cases" in data:
                return self._evaluate_multiple_cases(data["test_cases"])
            else:
                return self._evaluate_single_case(data)

        except Exception as e:
            return EvaluationResult(
                passed=False, error=f"LLM judge evaluation failed: {str(e)}"
            )

    def _evaluate_single_case(self, data: Dict[str, Any]) -> EvaluationResult:
        """Evaluate a single test case using LLM."""
        actual = data.get("actual")
        expected = data.get("expected")
        input_data = data.get("input")
        criteria = data.get(
            "evaluation_criteria",
            self._get_config_value("criteria", ["accuracy", "relevance"]),
        )

        if actual is None:
            return EvaluationResult(
                passed=False, error="No 'actual' value found in test output"
            )

        # Create evaluation prompt
        prompt = self._create_evaluation_prompt(
            input_data=input_data, actual=actual, expected=expected, criteria=criteria
        )

        # Get LLM judgment
        judgment = self._get_llm_judgment(prompt)

        if judgment.get("error"):
            return EvaluationResult(passed=False, error=judgment["error"])

        return EvaluationResult(
            passed=judgment.get("passed", False),
            score=judgment.get("score"),
            details={
                "actual": actual,
                "expected": expected,
                "input": input_data,
                "criteria": criteria,
                "reasoning": judgment.get("reasoning"),
                "scores_by_criteria": judgment.get("scores_by_criteria", {}),
            },
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

        return EvaluationResult(
            passed=passed_count == len(test_cases),
            score=overall_score,
            details={
                "total_cases": len(test_cases),
                "passed_cases": passed_count,
                "individual_results": [r.to_dict() for r in results],
            },
        )

    def _create_evaluation_prompt(
        self,
        input_data: Any,
        actual: Any,
        expected: Any = None,
        criteria: List[str] = None,
    ) -> str:
        """Create evaluation prompt for LLM."""
        criteria = criteria or ["accuracy", "relevance"]

        prompt_parts = [
            "You are an expert evaluator for AI agent outputs. Please evaluate the following response based on the specified criteria.",
            "",
            "EVALUATION CRITERIA:",
        ]

        for criterion in criteria:
            prompt_parts.append(
                f"- {criterion}: {self._get_criterion_description(criterion)}"
            )

        prompt_parts.extend(["", "INPUT DATA:"])

        if input_data is not None:
            prompt_parts.append(f"Input: {input_data}")

        prompt_parts.extend(["", "ACTUAL OUTPUT:", f"{actual}", ""])

        if expected is not None:
            prompt_parts.extend(["EXPECTED OUTPUT:", f"{expected}", ""])

        prompt_parts.extend(
            [
                "Please provide your evaluation in the following JSON format:",
                "{",
                '  "passed": true/false,',
                '  "score": 0.0-1.0,',
                '  "reasoning": "explanation of your evaluation",',
                '  "scores_by_criteria": {',
                '    "criterion1": 0.0-1.0,',
                '    "criterion2": 0.0-1.0',
                "  }",
                "}",
                "",
                "Evaluation:",
            ]
        )

        return "\n".join(prompt_parts)

    def _get_criterion_description(self, criterion: str) -> str:
        """Get description for evaluation criteria."""
        descriptions = {
            "accuracy": "How accurate and correct is the response?",
            "relevance": "How relevant is the response to the input?",
            "completeness": "How complete and comprehensive is the response?",
            "clarity": "How clear and understandable is the response?",
            "conciseness": "How concise and to-the-point is the response?",
            "coherence": "How logical and coherent is the response?",
            "helpfulness": "How helpful is the response to the user?",
            "safety": "How safe and appropriate is the response?",
            "factuality": "How factually correct is the response?",
            "consistency": "How consistent is the response with expected behavior?",
        }

        return descriptions.get(criterion, f"Evaluate based on {criterion}")

    def _get_llm_judgment(self, prompt: str) -> Dict[str, Any]:
        """Get judgment from LLM."""
        try:
            provider = self._get_config_value("provider", "openai")

            if provider == "openai":
                return self._get_openai_judgment(prompt)
            elif provider == "anthropic":
                return self._get_anthropic_judgment(prompt)
            elif provider == "gemini":
                return self._get_gemini_judgment(prompt)
            else:
                return {"error": f"Unsupported provider: {provider}"}

        except Exception as e:
            return {"error": f"LLM API call failed: {str(e)}"}

    def _get_openai_judgment(self, prompt: str) -> Dict[str, Any]:
        """Get judgment from OpenAI."""
        try:
            response = self.llm_client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert AI evaluator. Provide evaluations in valid JSON format.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=self._get_config_value("temperature", 0.0),
                max_tokens=self._get_config_value("max_tokens", 1000),
            )

            content = response.choices[0].message.content
            return self._parse_llm_response(content)

        except Exception as e:
            return {"error": f"OpenAI API error: {str(e)}"}

    def _get_anthropic_judgment(self, prompt: str) -> Dict[str, Any]:
        """Get judgment from Anthropic."""
        try:
            response = self.llm_client.messages.create(
                model=self.model,
                max_tokens=self._get_config_value("max_tokens", 1000),
                temperature=self._get_config_value("temperature", 0.0),
                messages=[{"role": "user", "content": prompt}],
            )

            content = response.content[0].text
            return self._parse_llm_response(content)

        except Exception as e:
            return {"error": f"Anthropic API error: {str(e)}"}

    def _get_gemini_judgment(self, prompt: str) -> Dict[str, Any]:
        """Get judgment from Google Gemini."""
        try:
            # Configure generation parameters
            generation_config = {
                "temperature": self._get_config_value("temperature", 0.0),
                "max_output_tokens": self._get_config_value("max_tokens", 1000),
            }

            # Add system instruction about being an evaluator
            full_prompt = (
                "You are an expert AI evaluator. Provide evaluations in valid JSON format. "
                + prompt
            )

            response = self.llm_client.generate_content(
                full_prompt, generation_config=generation_config
            )

            content = response.text
            return self._parse_llm_response(content)

        except Exception as e:
            return {"error": f"Gemini API error: {str(e)}"}

    def _parse_llm_response(self, content: str) -> Dict[str, Any]:
        """Parse LLM response to extract JSON evaluation."""
        try:
            # Try to extract JSON from the response
            import re

            # Look for JSON block
            json_match = re.search(
                r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", content, re.DOTALL
            )

            if json_match:
                json_str = json_match.group()
                judgment = json.loads(json_str)

                # Validate required fields
                if "passed" not in judgment:
                    judgment["passed"] = judgment.get("score", 0) >= 0.7

                return judgment
            else:
                # Fallback: try to parse basic information
                return self._parse_fallback_response(content)

        except json.JSONDecodeError:
            return self._parse_fallback_response(content)
        except Exception as e:
            return {"error": f"Failed to parse LLM response: {str(e)}"}

    def _parse_fallback_response(self, content: str) -> Dict[str, Any]:
        """Fallback parsing when JSON extraction fails."""
        content_lower = content.lower()

        # Simple heuristics for pass/fail
        if "pass" in content_lower and "fail" not in content_lower:
            passed = True
            score = 0.8
        elif (
            "fail" in content_lower
            or "incorrect" in content_lower
            or "wrong" in content_lower
        ):
            passed = False
            score = 0.2
        else:
            # Neutral case
            passed = True
            score = 0.5

        return {
            "passed": passed,
            "score": score,
            "reasoning": content,
            "note": "Parsed using fallback heuristics",
        }
