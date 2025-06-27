# Changelog

All notable changes to AgentTest will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Comprehensive documentation with MkDocs
- GitHub Pages deployment workflow
- Enhanced evaluator documentation
- API reference documentation
- Custom CSS and JavaScript for documentation

### Changed

- Improved documentation structure and navigation
- Enhanced code examples and usage patterns

## [0.1.0] - 2024-06-26

### Added

- Initial release of AgentTest framework
- Core testing decorators and runners
- Multiple evaluator types:
  - String similarity evaluator
  - LLM judge evaluator
  - NLP metrics evaluator (ROUGE, BLEU, METEOR)
  - Contains evaluator
  - Regex evaluator
- Git integration for performance tracking
- CLI interface with comprehensive commands
- Configuration system with YAML support
- Support for multiple LLM providers (OpenAI, Anthropic, Google Gemini)
- Test generation capabilities
- Rich console output and logging
- CI/CD integration support

### Features

- pytest-like decorator syntax
- Multiple evaluation criteria per test
- Tag-based test filtering
- Automatic test discovery
- Performance comparison across git commits
- Detailed test reporting and export
- Framework-agnostic design
- Support for LangChain and LlamaIndex

### Documentation

- Installation and setup guides
- Quick start tutorial
- Comprehensive API reference
- Configuration documentation
- Best practices and examples
- CLI command reference

## [0.0.1] - 2024-06-01

### Added

- Initial project setup
- Basic framework structure
- Core evaluator interface

---

## Release Notes

### Version 0.1.0

This is the initial stable release of AgentTest, providing a comprehensive testing framework for AI agents and prompts. The framework includes:

**Core Features:**

- Multiple evaluation methods for different testing needs
- Git-aware logging for performance tracking over time
- Rich CLI interface for easy test management
- Support for major LLM providers

**Evaluators:**

- **Similarity**: Text similarity using various algorithms (cosine, Levenshtein, Jaccard)
- **LLM Judge**: AI-powered evaluation with custom criteria
- **NLP Metrics**: Standard metrics like ROUGE, BLEU, and METEOR
- **Pattern Matching**: Regex and keyword-based validation

**Developer Experience:**

- Familiar pytest-like syntax
- Comprehensive documentation
- Rich console output with detailed error reporting
- Easy integration with existing CI/CD pipelines

**Getting Started:**

```bash
pip install agenttest
agenttest init
agenttest run
```

For detailed documentation, visit: https://nihal-srivastava05.github.io/agent-test/
