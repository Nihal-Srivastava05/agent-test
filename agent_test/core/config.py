"""
Configuration management for AgentTest.

Handles loading and validation of configuration files using Pydantic.
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from dotenv import load_dotenv
from pydantic import BaseModel, Field, validator

# Load environment variables
load_dotenv()


class LLMConfig(BaseModel):
    """Configuration for LLM providers."""

    provider: str = Field(..., description="LLM provider (openai, anthropic, etc.)")
    model: str = Field(..., description="Model name")
    api_key: Optional[str] = Field(None, description="API key (can use env var)")
    api_base: Optional[str] = Field(None, description="Custom API base URL")
    temperature: float = Field(0.0, description="Temperature for generation")
    max_tokens: Optional[int] = Field(None, description="Max tokens for generation")

    @validator("api_key", pre=True, always=True)
    def resolve_api_key(cls, v, values):
        """Resolve API key from environment if not provided."""
        if v is None:
            provider = values.get("provider", "")
            env_var = f"{provider.upper()}_API_KEY"
            return os.getenv(env_var)
        return v


class EvaluatorConfig(BaseModel):
    """Configuration for evaluators."""

    name: str = Field(..., description="Evaluator name")
    type: str = Field(..., description="Evaluator type")
    config: Dict[str, Any] = Field(
        default_factory=dict, description="Evaluator-specific config"
    )
    weight: float = Field(1.0, description="Weight for composite scoring")
    enabled: bool = Field(True, description="Whether evaluator is enabled")


class AgentConfig(BaseModel):
    """Configuration for agents."""

    name: str = Field(..., description="Agent name")
    type: str = Field(..., description="Agent type (langchain, function, etc.)")
    path: str = Field(..., description="Path to agent implementation")
    config: Dict[str, Any] = Field(
        default_factory=dict, description="Agent-specific config"
    )


class TestConfig(BaseModel):
    """Configuration for test execution."""

    test_dirs: List[str] = Field(
        default=["tests"], description="Directories to search for tests"
    )
    test_patterns: List[str] = Field(
        default=["test_*.py"], description="Test file patterns"
    )
    parallel: bool = Field(False, description="Run tests in parallel")
    timeout: int = Field(300, description="Test timeout in seconds")
    retry_count: int = Field(0, description="Number of retries for failed tests")


class LoggingConfig(BaseModel):
    """Configuration for logging."""

    level: str = Field("INFO", description="Log level")
    file: Optional[str] = Field(None, description="Log file path")
    git_aware: bool = Field(True, description="Include git information in logs")
    results_dir: str = Field(
        ".agenttest/results", description="Directory for test results"
    )


class Config(BaseModel):
    """Main configuration class."""

    version: str = Field("1.0", description="Config file version")
    project_name: str = Field("AgentTest Project", description="Project name")

    # Core configurations
    llm: LLMConfig = Field(..., description="LLM configuration")
    evaluators: List[EvaluatorConfig] = Field(
        default_factory=list, description="Evaluator configurations"
    )
    agents: List[AgentConfig] = Field(
        default_factory=list, description="Agent configurations"
    )
    testing: TestConfig = Field(
        default_factory=TestConfig, description="Test execution configuration"
    )
    logging: LoggingConfig = Field(
        default_factory=LoggingConfig, description="Logging configuration"
    )

    # Additional settings
    plugins: List[str] = Field(
        default_factory=list, description="Plugin modules to load"
    )
    custom_evaluators: Dict[str, str] = Field(
        default_factory=dict, description="Custom evaluator mappings"
    )

    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> "Config":
        """Load configuration from file."""
        if config_path is None:
            config_path = cls._find_config_file()

        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        with open(config_path, "r") as f:
            config_data = yaml.safe_load(f)

        return cls(**config_data)

    def save(self, config_path: Optional[Path] = None) -> None:
        """Save configuration to file."""
        if config_path is None:
            config_path = Path(".agenttest") / "config.yaml"

        # Ensure directory exists
        config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(config_path, "w") as f:
            yaml.dump(self.dict(), f, default_flow_style=False, sort_keys=False)

    @staticmethod
    def _find_config_file() -> Path:
        """Find configuration file in current directory or parent directories."""
        current_dir = Path.cwd()

        # Look for .agenttest/config.yaml in current and parent directories
        while current_dir != current_dir.parent:
            config_path = current_dir / ".agenttest" / "config.yaml"
            if config_path.exists():
                return config_path
            current_dir = current_dir.parent

        # Default path if not found
        return Path(".agenttest") / "config.yaml"

    def get_evaluator(self, name: str) -> Optional[EvaluatorConfig]:
        """Get evaluator configuration by name."""
        for evaluator in self.evaluators:
            if evaluator.name == name:
                return evaluator
        return None

    def get_agent(self, name: str) -> Optional[AgentConfig]:
        """Get agent configuration by name."""
        for agent in self.agents:
            if agent.name == name:
                return agent
        return None

    @classmethod
    def create_default(cls, template: str = "basic") -> "Config":
        """Create a default configuration based on template."""
        base_config = {
            "version": "1.0",
            "project_name": "AgentTest Project",
            "llm": {"provider": "openai", "model": "gpt-3.5-turbo", "temperature": 0.0},
            "evaluators": [
                {
                    "name": "similarity",
                    "type": "string_similarity",
                    "config": {"method": "cosine", "threshold": 0.8},
                },
                {
                    "name": "llm_judge",
                    "type": "llm_as_judge",
                    "config": {"criteria": ["accuracy", "relevance"]},
                },
            ],
            "testing": {
                "test_dirs": ["tests"],
                "test_patterns": ["test_*.py", "*_test.py"],
                "parallel": False,
                "timeout": 300,
            },
            "logging": {
                "level": "INFO",
                "git_aware": True,
                "results_dir": ".agenttest/results",
            },
        }

        # Template-specific configurations
        if template == "langchain":
            base_config["agents"] = [
                {
                    "name": "default_agent",
                    "type": "langchain",
                    "path": "agents/langchain_agent.py",
                    "config": {},
                }
            ]
            base_config["evaluators"].extend(
                [
                    {
                        "name": "retrieval_relevance",
                        "type": "retrieval_evaluator",
                        "config": {"top_k": 5},
                    }
                ]
            )

        elif template == "llamaindex":
            base_config["agents"] = [
                {
                    "name": "default_agent",
                    "type": "llamaindex",
                    "path": "agents/llama_agent.py",
                    "config": {},
                }
            ]

        return cls(**base_config)
