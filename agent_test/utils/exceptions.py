"""
Custom exceptions for AgentTest.

Provides specific exception types for different error scenarios.
"""


class AgentTestError(Exception):
    """Base exception for all AgentTest errors."""

    pass


class ConfigurationError(AgentTestError):
    """Raised when there's an issue with configuration."""

    pass


class TestDiscoveryError(AgentTestError):
    """Raised when test discovery fails."""

    pass


class TestExecutionError(AgentTestError):
    """Raised when test execution fails."""

    pass


class EvaluationError(AgentTestError):
    """Raised when evaluation fails."""

    pass


class GitError(AgentTestError):
    """Raised when git operations fail."""

    pass


class AgentLoadError(AgentTestError):
    """Raised when agent loading fails."""

    pass


class GenerationError(AgentTestError):
    """Raised when test generation fails."""

    pass
