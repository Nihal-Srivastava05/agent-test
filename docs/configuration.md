# Configuration Guide

AgentTest uses YAML-based configuration files to define evaluators, LLM providers, testing parameters, and more. This guide covers all configuration options and best practices.

## 📁 Configuration File Location

AgentTest looks for configuration in the following order:

1. `.agenttest/config.yaml` in current directory
2. `.agenttest/config.yaml` in parent directories (walking up)
3. Custom path specified with `--config` flag

## 📝 Basic Configuration Structure

```yaml
version: '1.0'
project_name: 'My Agent Project'

# LLM Configuration
llm:
  provider: 'openai'
  model: 'gpt-3.5-turbo'
  temperature: 0.0

# Evaluator Configurations
evaluators:
  - name: 'similarity'
    type: 'string_similarity'
    config:
      method: 'cosine'
      threshold: 0.8
    weight: 1.0
    enabled: true

# Testing Configuration
testing:
  test_dirs: ['tests']
  test_patterns: ['test_*.py']
  parallel: false
  timeout: 300

# Logging Configuration
logging:
  level: 'INFO'
  git_aware: true
  results_dir: '.agenttest/results'
```

## 🤖 LLM Configuration

Configure language model providers for LLM judge evaluators.

### Basic LLM Config

```yaml
llm:
  provider: 'openai' # openai, anthropic, gemini
  model: 'gpt-3.5-turbo' # Model name
  api_key: null # Optional, uses env vars by default
  temperature: 0.0 # Generation temperature
  max_tokens: null # Max tokens (optional)
```

### Provider-Specific Configurations

#### OpenAI

```yaml
llm:
  provider: 'openai'
  model: 'gpt-4' # gpt-3.5-turbo, gpt-4, gpt-4-turbo
  api_key: ${OPENAI_API_KEY} # Environment variable
  api_base: null # Custom API base URL
  temperature: 0.0
  max_tokens: 1000
```

**Supported Models:**

- `gpt-3.5-turbo` - Fast, cost-effective
- `gpt-4` - High quality, slower
- `gpt-4-turbo` - Latest GPT-4 variant
- `gpt-4o` - Optimized GPT-4

#### Anthropic

```yaml
llm:
  provider: 'anthropic'
  model: 'claude-3-sonnet-20240229'
  api_key: ${ANTHROPIC_API_KEY}
  temperature: 0.0
  max_tokens: 1000
```

**Supported Models:**

- `claude-3-haiku-20240307` - Fast, lightweight
- `claude-3-sonnet-20240229` - Balanced performance
- `claude-3-opus-20240229` - Highest capability

#### Google Gemini

```yaml
llm:
  provider: 'gemini'
  model: 'gemini-pro'
  api_key: ${GOOGLE_API_KEY}
  temperature: 0.0
  max_output_tokens: 1000
```

**Supported Models:**

- `gemini-pro` - General purpose
- `gemini-1.5-pro` - Latest version
- `gemini-1.5-flash` - Fast inference

### Environment Variables

AgentTest automatically resolves API keys from environment variables:

| Provider      | Environment Variables              |
| ------------- | ---------------------------------- |
| **OpenAI**    | `OPENAI_API_KEY`                   |
| **Anthropic** | `ANTHROPIC_API_KEY`                |
| **Google**    | `GOOGLE_API_KEY`, `GEMINI_API_KEY` |

## 📊 Evaluator Configuration

Configure multiple evaluators with specific settings and weights.

### Evaluator Structure

```yaml
evaluators:
  - name: 'evaluator_name' # Unique identifier
    type: 'evaluator_type' # Implementation type
    config: # Evaluator-specific configuration
      key: value
    weight: 1.0 # Weight in overall score (0-1)
    enabled: true # Enable/disable evaluator
```

### String Similarity Evaluator

```yaml
evaluators:
  - name: 'similarity'
    type: 'string_similarity'
    config:
      method: 'cosine' # cosine, levenshtein, jaccard, exact
      threshold: 0.8 # Pass threshold (0-1)
    weight: 1.0
    enabled: true
```

**Method Options:**

| Method        | Description              | Best For                  | Performance |
| ------------- | ------------------------ | ------------------------- | ----------- |
| `cosine`      | TF-IDF cosine similarity | General text comparison   | Medium      |
| `levenshtein` | Edit distance            | Exact matching with typos | Fast        |
| `jaccard`     | Set intersection/union   | Keyword similarity        | Fast        |
| `exact`       | Exact string match       | Precise outputs           | Very Fast   |

### LLM Judge Evaluator

```yaml
evaluators:
  - name: 'llm_judge'
    type: 'llm_as_judge'
    config:
      provider: 'openai' # Override global LLM config
      model: 'gpt-4'
      criteria: ['accuracy', 'relevance', 'clarity']
      temperature: 0.0
      threshold: 0.7 # Pass threshold
    weight: 1.0
    enabled: true
```

**Built-in Criteria:**

- `accuracy` - Factual correctness
- `relevance` - Topic relevance
- `clarity` - Communication clarity
- `creativity` - Original thinking
- `helpfulness` - Practical utility
- `conciseness` - Brevity
- `completeness` - Comprehensive coverage

### Metrics Evaluator

```yaml
evaluators:
  - name: 'metrics'
    type: 'nlp_metrics'
    config:
      rouge:
        variants: ['rouge1', 'rouge2', 'rougeL']
        min_score: 0.4
      bleu:
        n_grams: [1, 2, 3, 4]
        min_score: 0.3
      meteor:
        min_score: 0.5
    weight: 1.0
    enabled: true
```

### Contains Evaluator

```yaml
evaluators:
  - name: 'contains'
    type: 'contains_check'
    config:
      case_sensitive: false # Case-sensitive matching
      partial_match: true # Allow partial word matches
    weight: 1.0
    enabled: true
```

### Regex Evaluator

```yaml
evaluators:
  - name: 'regex'
    type: 'regex_pattern'
    config:
      flags: ['IGNORECASE'] # Regex flags
    weight: 1.0
    enabled: true
```

## 🧪 Testing Configuration

Configure test discovery, execution, and behavior.

```yaml
testing:
  test_dirs: ['tests', 'integration'] # Directories to search
  test_patterns: ['test_*.py', '*_test.py'] # File patterns
  parallel: false # Parallel execution
  timeout: 300 # Test timeout (seconds)
  retry_count: 0 # Retry failed tests
```

### Advanced Testing Options

```yaml
testing:
  test_dirs:
    - 'tests/unit'
    - 'tests/integration'
    - 'tests/e2e'
  test_patterns:
    - 'test_*.py'
    - '*_test.py'
    - 'test_*.yaml' # YAML test files
  parallel: true # Enable parallel execution
  max_workers: 4 # Number of parallel workers
  timeout: 600 # Longer timeout for complex tests
  retry_count: 2 # Retry failed tests up to 2 times
  retry_delay: 1.0 # Delay between retries (seconds)

  # Test filtering
  include_tags: ['smoke', 'regression']
  exclude_tags: ['slow', 'experimental']

  # Test environment
  environment:
    TEST_MODE: 'true'
    DEBUG_LEVEL: 'INFO'
```

## 📝 Logging Configuration

Configure logging behavior and output formats.

```yaml
logging:
  level: 'INFO' # DEBUG, INFO, WARNING, ERROR
  file: null # Log file path (optional)
  git_aware: true # Include git information
  results_dir: '.agenttest/results' # Results storage directory
  format: 'rich' # Output format

  # Advanced logging options
  console_output: true # Enable console output
  json_logs: false # JSON formatted logs
  log_evaluations: true # Log individual evaluations
  performance_tracking: true # Track performance metrics
```

### Log Levels

| Level     | Description             | Use Case               |
| --------- | ----------------------- | ---------------------- |
| `DEBUG`   | Detailed execution info | Development, debugging |
| `INFO`    | General information     | Normal operation       |
| `WARNING` | Warning messages        | Production monitoring  |
| `ERROR`   | Error messages only     | Production, CI/CD      |

## 🚀 Agent Configuration

Configure specific agents for testing (optional).

```yaml
agents:
  - name: 'chatbot'
    type: 'langchain'
    path: 'agents/chatbot.py'
    config:
      llm_provider: 'openai'
      memory_type: 'buffer'

  - name: 'summarizer'
    type: 'function'
    path: 'agents/summarizer.py'
    config:
      max_length: 100
      style: 'concise'
```

## 🔌 Plugin Configuration

Configure plugins and extensions.

```yaml
plugins:
  - 'custom_evaluators' # Custom evaluator modules
  - 'langchain_integration' # LangChain support
  - 'dashboard_extensions' # Dashboard plugins

custom_evaluators:
  sentiment: 'evaluators.sentiment.SentimentEvaluator'
  toxicity: 'evaluators.safety.ToxicityEvaluator'
```

## 🌍 Environment-Specific Configurations

### Development Configuration

```yaml
# .agenttest/config.dev.yaml
version: '1.0'
project_name: 'Agent Project (Development)'

llm:
  provider: 'openai'
  model: 'gpt-3.5-turbo' # Faster model for development
  temperature: 0.1

evaluators:
  - name: 'similarity'
    config:
      threshold: 0.7 # Lower threshold for development

testing:
  timeout: 120 # Shorter timeout
  retry_count: 0 # No retries in development

logging:
  level: 'DEBUG' # Verbose logging
  console_output: true
```

### Production Configuration

```yaml
# .agenttest/config.prod.yaml
version: '1.0'
project_name: 'Agent Project (Production)'

llm:
  provider: 'openai'
  model: 'gpt-4' # Higher quality model
  temperature: 0.0

evaluators:
  - name: 'similarity'
    config:
      threshold: 0.85 # Higher threshold for production

  - name: 'llm_judge'
    config:
      criteria: ['accuracy', 'safety', 'relevance']

testing:
  timeout: 600 # Longer timeout
  retry_count: 2 # Retry failed tests
  parallel: true # Parallel execution

logging:
  level: 'INFO' # Standard logging
  json_logs: true # Structured logs
  git_aware: true
```

### CI/CD Configuration

```yaml
# .agenttest/config.ci.yaml
version: '1.0'
project_name: 'Agent Project (CI/CD)'

llm:
  provider: 'openai'
  model: 'gpt-3.5-turbo' # Cost-effective for CI

evaluators:
  - name: 'similarity'
    config:
      threshold: 0.8

testing:
  timeout: 300
  parallel: true
  max_workers: 2 # Limited parallelism in CI

logging:
  level: 'WARNING' # Minimal logging
  console_output: false # No console output in CI
  json_logs: true
  results_dir: 'ci-results'
```

## 📊 Configuration Templates

### Basic Template

```yaml
version: '1.0'
project_name: 'Basic Agent Testing'

llm:
  provider: 'openai'
  model: 'gpt-3.5-turbo'
  temperature: 0.0

evaluators:
  - name: 'similarity'
    type: 'string_similarity'
    config:
      threshold: 0.8
    weight: 1.0
    enabled: true

testing:
  test_dirs: ['tests']
  test_patterns: ['test_*.py']
  timeout: 300

logging:
  level: 'INFO'
  git_aware: true
```

### Comprehensive Template

```yaml
version: '1.0'
project_name: 'Comprehensive Agent Testing'

llm:
  provider: 'openai'
  model: 'gpt-4'
  temperature: 0.0

evaluators:
  - name: 'similarity'
    type: 'string_similarity'
    config:
      method: 'cosine'
      threshold: 0.8
    weight: 0.3
    enabled: true

  - name: 'llm_judge'
    type: 'llm_as_judge'
    config:
      criteria: ['accuracy', 'relevance', 'clarity']
      threshold: 0.7
    weight: 0.4
    enabled: true

  - name: 'contains'
    type: 'contains_check'
    config:
      case_sensitive: false
    weight: 0.1
    enabled: true

  - name: 'metrics'
    type: 'nlp_metrics'
    config:
      rouge:
        variants: ['rouge1', 'rougeL']
        min_score: 0.4
    weight: 0.2
    enabled: true

testing:
  test_dirs: ['tests', 'integration']
  test_patterns: ['test_*.py', '*_test.py']
  parallel: true
  timeout: 600
  retry_count: 1

logging:
  level: 'INFO'
  git_aware: true
  performance_tracking: true
  json_logs: true
```

## 🔧 Configuration Validation

AgentTest validates configuration files on startup. Common validation errors:

### Required Fields

- `version` - Configuration version
- `llm.provider` - LLM provider
- `llm.model` - Model name

### Valid Values

- `llm.provider`: `openai`, `anthropic`, `gemini`
- `logging.level`: `DEBUG`, `INFO`, `WARNING`, `ERROR`
- `evaluator.weight`: 0.0 to 1.0

### Example Validation Error

```
❌ Configuration Error:
  - llm.provider: 'invalid_provider' is not a valid provider
  - evaluators[0].weight: 1.5 is greater than maximum allowed value 1.0
  - testing.timeout: must be a positive integer
```

## 🔗 Configuration Inheritance

You can extend configurations using inheritance:

```yaml
# base-config.yaml
version: "1.0"
llm:
  provider: "openai"
  temperature: 0.0

# specific-config.yaml
extends: "base-config.yaml"
project_name: "Specific Project"
llm:
  model: "gpt-4"              # Overrides base config
```

## 🛠️ Configuration Best Practices

### 1. Environment-Specific Configs

- Separate configs for dev/staging/prod
- Use environment variables for secrets
- Lower thresholds in development

### 2. Evaluator Selection

- Start with similarity evaluator
- Add LLM judge for subjective quality
- Use metrics for specific NLP tasks
- Combine multiple evaluators for robustness

### 3. Performance Optimization

- Use faster models in CI/CD
- Enable parallel execution for large test suites
- Adjust timeouts based on test complexity

### 4. Security

- Never commit API keys
- Use environment variables
- Restrict permissions in production

### 5. Monitoring

- Enable git integration
- Use structured logging in production
- Track performance metrics over time

## 🔗 Related Documentation

- [Installation](installation.md) - Setting up configuration
- [Evaluators](evaluators.md) - Detailed evaluator options
- [CLI Commands](cli-commands.md) - Using configuration with commands
- [Git Integration](git-integration.md) - Git-aware configuration
