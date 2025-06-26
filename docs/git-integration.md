# Git Integration

AgentTest provides powerful git integration features that track test performance across commits, branches, and time. This enables regression detection, performance monitoring, and comparison workflows.

## 🔍 Overview

Git integration automatically:

- **Tracks Performance**: Records test results with git metadata
- **Enables Comparisons**: Compare results between commits/branches
- **Detects Regressions**: Identify performance degradations
- **Provides History**: Browse test results over time
- **Supports Workflows**: Integrate with CI/CD pipelines

## 📊 Automatic Test Tracking

Every test run is automatically logged with git information:

```bash
# Run tests - automatically logged with git metadata
agenttest run

# Results are stored with:
# - Commit hash
# - Branch name
# - Timestamp
# - Test outcomes
# - Evaluation scores
```

### Stored Information

Each test run includes:

| Field               | Description              | Example                                    |
| ------------------- | ------------------------ | ------------------------------------------ |
| `commit_hash`       | Full commit SHA          | `e1c83a6d4f2b8a9c7e5d3f1a8b6c4e2d9f7a5b3c` |
| `commit_hash_short` | Short commit SHA         | `e1c83a6d`                                 |
| `branch`            | Git branch name          | `main`, `feature-123`                      |
| `timestamp`         | Execution time           | `2024-06-26T14:45:12.789012`               |
| `author`            | Commit author            | `john.doe@example.com`                     |
| `message`           | Commit message           | `Fix: Improve summarization accuracy`      |
| `test_results`      | Individual test outcomes | Scores, pass/fail status                   |
| `summary`           | Overall test summary     | Pass rate, average score                   |

## 📚 Viewing Test History

### Basic History

```bash
# Show last 10 test runs
agenttest log

# Show last 20 runs
agenttest log --limit 20
```

### Filtered History

```bash
# Show results for specific commit
agenttest log --commit abc123

# Show results for specific branch
agenttest log --branch main

# Show results for feature branch
agenttest log --branch feature-summarization
```

### History Output

```
📚 Test History (last 10 runs):

┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Commit     ┃ Timestamp           ┃ Branch        ┃ Tests         ┃ Pass Rate     ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ e1c83a6d   │ 2024-06-26 14:45:12 │ main          │ 5 passed, 0   │ 100%          │
│ 95eadec3   │ 2024-06-26 14:38:33 │ main          │ 3 passed, 2   │ 60%           │
│ 7b2af91e   │ 2024-06-26 12:15:44 │ feature-123   │ 4 passed, 1   │ 80%           │
│ 4c9e8f1d   │ 2024-06-26 11:22:15 │ main          │ 5 passed, 0   │ 100%          │
│ 2a7b5e9f   │ 2024-06-25 16:45:33 │ develop       │ 4 passed, 1   │ 80%           │
└────────────┴─────────────────────┴───────────────┴───────────────┴───────────────┘
```

## 🔄 Performance Comparison

The `compare` command provides detailed analysis between any two git references.

### Basic Comparison

```bash
# Compare current commit with previous
agenttest compare HEAD~1

# Compare specific commits
agenttest compare abc123 def456

# Compare branches
agenttest compare main feature-branch
```

### Advanced Comparison Options

```bash
# Focus on specific evaluator
agenttest compare abc123 def456 --metric similarity

# Filter tests by name pattern
agenttest compare abc123 def456 --filter "summarization"

# Adjust sensitivity threshold
agenttest compare abc123 def456 --min-change 0.05

# Show detailed evaluator breakdown
agenttest compare abc123 def456 --detailed

# Include unchanged tests
agenttest compare abc123 def456 --include-unchanged

# Export results to JSON
agenttest compare abc123 def456 --export comparison.json
```

### Comparison Output

#### Summary Changes

```
📊 Comparing abc123 → def456
Base: abc123 (2024-06-26T14:38:33)
Target: def456 (2024-06-26T14:45:12)

📊 Overall Summary Changes:
┏━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━┓
┃ Metric       ┃   Base ┃  Target ┃  Change ┃ % Change  ┃
┡━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━┩
│ Pass Rate    │   0.75 │    0.85 │  +0.100 │    +13.3% │
│ Average Score│   0.692│    0.751│  +0.059 │     +8.5% │
│ Total Tests  │      4 │       5 │      +1 │    +25.0% │
└──────────────┴────────┴─────────┴─────────┴───────────┘
```

#### Test-Level Changes

```
🔍 Test Changes Overview
├── 📈 Improvements: 2
├── 📉 Regressions: 1
├── 🆕 New Tests: 1
└── 🗑️ Removed Tests: 0

📈 Improvements:
  • test_summarization: score: 0.734 → 0.856 (+0.122)
  • test_qa_accuracy: FAIL → PASS, score: 0.650 → 0.823 (+0.173)

📉 Regressions:
  • test_content_generation: score: 0.891 → 0.734 (-0.157)

🆕 New Tests:
  • test_new_feature: PASS, score: 0.912
```

#### Detailed Evaluator Analysis

```bash
agenttest compare abc123 def456 --detailed
```

```
🔍 Evaluator-Specific Changes:

  similarity:
    • test_summarization: 0.734 → 0.856 (+0.122)
    • test_qa_accuracy: 0.432 → 0.678 (+0.246)
    • test_content_generation: 0.891 → 0.734 (-0.157)

  llm_judge:
    • test_summarization: 0.823 → 0.867 (+0.044)
    • test_qa_accuracy: 0.712 → 0.845 (+0.133)
    • test_content_generation: 0.912 → 0.745 (-0.167)
```

## 🚀 Development Workflows

### Pre-Commit Checks

```bash
# Check for regressions before committing
agenttest compare HEAD~1 HEAD --detailed

# Fail if significant regressions detected
agenttest compare HEAD~1 HEAD --min-change 0.05 | grep "📉 Regressions: 0" || exit 1
```

### Feature Development

```bash
# Start feature branch
git checkout -b feature-new-capability

# Develop and test iteratively
agenttest run --verbose

# Compare with main branch before merge
agenttest compare main feature-new-capability --detailed

# Check specific evaluator performance
agenttest compare main feature-new-capability --metric llm_judge
```

### Release Validation

```bash
# Compare release candidate with previous release
agenttest compare v1.2.0 v1.3.0-rc1 --detailed --export release-comparison.json

# Validate no regressions in core functionality
agenttest compare v1.2.0 v1.3.0-rc1 --filter "core" --min-change 0.02
```

## 🔧 CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/agent-tests.yml
name: Agent Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0 # Fetch full history for comparisons

      - name: Set up Python
        uses: actions/setup-python@v3
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install agenttest

      - name: Run tests
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          agenttest run --ci --output results.json

      - name: Compare with main (for PRs)
        if: github.event_name == 'pull_request'
        run: |
          agenttest compare origin/main HEAD \
            --detailed \
            --export comparison.json \
            --min-change 0.02

      - name: Upload results
        uses: actions/upload-artifact@v3
        with:
          name: test-results
          path: |
            results.json
            comparison.json

      - name: Comment PR with results
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const comparison = JSON.parse(fs.readFileSync('comparison.json', 'utf8'));

            const comment = `## 🧪 Agent Test Results

            ### Summary Changes
            - **Pass Rate**: ${comparison.summary_changes.pass_rate?.change || 'N/A'}
            - **Average Score**: ${comparison.summary_changes.average_score?.change || 'N/A'}

            ### Changes
            - 📈 Improvements: ${comparison.improvements.length}
            - 📉 Regressions: ${comparison.regressions.length}
            - 🆕 New Tests: ${comparison.new_tests.length}
            `;

            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comment
            });
```

### GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  - test
  - compare

agent_tests:
  stage: test
  script:
    - pip install agenttest
    - agenttest run --ci --output results.json
  artifacts:
    reports:
      junit: results.json
    paths:
      - results.json
    expire_in: 1 week
  only:
    - main
    - develop
    - merge_requests

compare_performance:
  stage: compare
  script:
    - agenttest compare $CI_MERGE_REQUEST_TARGET_BRANCH_NAME $CI_COMMIT_SHA --detailed --export comparison.json
  artifacts:
    paths:
      - comparison.json
  only:
    - merge_requests
```

## 📊 Performance Monitoring

### Long-term Tracking

```bash
# Generate performance trend report
agenttest log --limit 50 --branch main > performance-history.txt

# Compare performance over time windows
agenttest compare $(git rev-parse HEAD~20) HEAD --detailed --export trend-analysis.json
```

### Automated Monitoring Script

```bash
#!/bin/bash
# monitor-performance.sh

# Get current and previous commit
CURRENT=$(git rev-parse HEAD)
PREVIOUS=$(git rev-parse HEAD~1)

# Run comparison
agenttest compare $PREVIOUS $CURRENT \
  --detailed \
  --min-change 0.02 \
  --export comparison.json

# Check for significant regressions
REGRESSIONS=$(cat comparison.json | jq '.regressions | length')

if [ $REGRESSIONS -gt 0 ]; then
  echo "⚠️  Performance regressions detected!"
  agenttest compare $PREVIOUS $CURRENT --detailed
  exit 1
else
  echo "✅ No significant performance regressions detected"
fi
```

## 🔍 Debugging Performance Issues

### Identify Problem Areas

```bash
# Focus on specific evaluator that's regressing
agenttest compare abc123 def456 --metric similarity --detailed

# Look at specific test patterns
agenttest compare abc123 def456 --filter "summarization" --detailed

# Find tests with largest score drops
agenttest compare abc123 def456 --min-change 0.1 --detailed
```

### Historical Analysis

```bash
# Find when performance started declining
for commit in $(git rev-list --reverse HEAD~10..HEAD); do
  echo "Checking commit: $commit"
  agenttest compare HEAD~10 $commit --quiet | grep "Average Score"
done

# Bisect performance issues
git bisect start HEAD HEAD~10
# Use agenttest compare in bisect script
```

## 🗂️ Data Storage

### File Structure

```
.agenttest/results/
├── index.json                    # Master index of all runs
├── 20240626_144512_e1c83a6d.json # Individual test run results
├── 20240626_143833_95eadec3.json
└── 20240626_122144_7b2af91e.json
```

### Index Format

```json
{
  "runs": [
    {
      "timestamp": "2024-06-26T14:45:12.789012",
      "commit_hash": "e1c83a6d4f2b8a9c7e5d3f1a8b6c4e2d9f7a5b3c",
      "commit_hash_short": "e1c83a6d",
      "branch": "main",
      "summary": {
        "total_tests": 5,
        "passed": 5,
        "failed": 0,
        "pass_rate": 100.0,
        "average_score": 0.887
      },
      "filename": "20240626_144512_e1c83a6d.json"
    }
  ],
  "by_commit": {
    "e1c83a6d": [...],
    "95eadec3": [...]
  },
  "by_branch": {
    "main": [...],
    "feature-123": [...]
  }
}
```

### Individual Result Format

```json
{
  "timestamp": "2024-06-26T14:45:12.789012",
  "git_info": {
    "commit_hash": "e1c83a6d4f2b8a9c7e5d3f1a8b6c4e2d9f7a5b3c",
    "commit_hash_short": "e1c83a6d",
    "branch": "main",
    "author": "john.doe@example.com",
    "message": "Fix: Improve summarization accuracy"
  },
  "summary": {
    "total_tests": 5,
    "passed": 5,
    "failed": 0,
    "pass_rate": 100.0,
    "average_score": 0.887,
    "total_duration": 12.45
  },
  "test_results": [
    {
      "test_name": "test_summarization",
      "passed": true,
      "score": 0.856,
      "duration": 2.45,
      "evaluations": {
        "similarity": { "score": 0.834, "passed": true },
        "llm_judge": { "score": 0.878, "passed": true }
      }
    }
  ]
}
```

## 🔧 Configuration

Enable git integration in configuration:

```yaml
logging:
  git_aware: true # Enable git integration
  results_dir: '.agenttest/results' # Results storage location
```

### Advanced Git Options

```yaml
logging:
  git_aware: true
  results_dir: '.agenttest/results'
  git_config:
    track_author: true # Include commit author
    track_message: true # Include commit message
    track_changes: true # Include file changes
    max_history: 100 # Limit stored results
    cleanup_days: 30 # Auto-cleanup old results
```

## 🛠️ Best Practices

### 1. Commit Hygiene

- Make atomic commits for better tracking
- Use descriptive commit messages
- Tag releases for easy comparison

### 2. Branch Strategy

- Test feature branches before merging
- Compare with target branch regularly
- Use meaningful branch names

### 3. Performance Monitoring

- Set up automated comparison checks
- Monitor long-term trends
- Investigate regressions quickly

### 4. CI/CD Integration

- Include comparison in PR workflows
- Fail builds on significant regressions
- Generate comparison reports

### 5. Data Management

- Regular cleanup of old results
- Export important comparisons
- Back up critical performance data

## 🔗 Related Documentation

- [CLI Commands](cli-commands.md) - Detailed command reference
- [Configuration](configuration.md) - Git integration configuration
- [Writing Tests](writing-tests.md) - Test structure for tracking
- Enhanced logging features (built-in)
