"""
AgentTest: A pytest-like testing framework for AI agents and prompts.

A comprehensive testing framework designed specifically for AI agents,
providing evaluation, logging, and regression tracking capabilities.
"""

__version__ = "0.1.0"
__author__ = "AgentTest Contributors"
__license__ = "MIT"

from .core.config import Config
from .core.decorators import agent_test
from .core.runner import run_test
from .evaluators.registry import EvaluatorRegistry

# Public API
__all__ = [
    "agent_test",
    "run_test",
    "Config",
    "EvaluatorRegistry",
]
