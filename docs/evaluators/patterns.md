# Pattern Matching Evaluators

Pattern matching evaluators provide rule-based validation for structured outputs, required content, and format compliance. This includes the Contains Evaluator and Regex Evaluator for different types of pattern matching needs.

## 🎯 Overview

Pattern matching evaluators validate agent outputs against specific patterns, keywords, or structures. They're ideal for:

- Structured data validation
- Required content verification
- Format compliance checking
- Keyword presence testing
- Rule-based quality assurance

## 📝 Contains Evaluator

The Contains Evaluator checks if the output contains required words, phrases, or concepts.

### Configuration

```yaml
evaluators:
  - name: 'contains'
    type: 'contains_check'
    config:
      case_sensitive: false
      match_all: true # All items must be present
      partial_match: true # Allow substring matching
    weight: 1.0
    enabled: true
```

### Basic Usage

```python
@agent_test(criteria=['contains'])
def test_required_keywords():
    """Test if response contains required keywords."""
    prompt = "List the benefits of renewable energy"
    response = agent(prompt)

    return {
        "input": prompt,
        "actual": response,
        "contains": ["solar", "wind", "sustainable", "environment"]
    }
```

### Advanced Contains Patterns

#### Exact Phrases

```python
@agent_test(criteria=['contains'])
def test_exact_phrases():
    """Test for exact phrase matches."""
    return {
        "input": "Explain machine learning",
        "actual": agent_response,
        "contains": [
            "machine learning",
            "artificial intelligence",
            "data patterns",
            "predictive models"
        ]
    }
```

#### Case-Sensitive Matching

```python
@agent_test(criteria=['contains'])
def test_case_sensitive():
    """Test with case-sensitive requirements."""
    return {
        "input": "List Python libraries",
        "actual": agent_response,
        "contains": ["NumPy", "TensorFlow", "PyTorch"],  # Exact capitalization
        "contains_config": {
            "case_sensitive": True
        }
    }
```

#### Flexible Matching

```python
@agent_test(criteria=['contains'])
def test_flexible_matching():
    """Test with flexible matching requirements."""
    return {
        "input": "Describe data science workflow",
        "actual": agent_response,
        "contains": ["collect", "clean", "analyze", "visualize"],
        "contains_config": {
            "match_all": False,    # At least one must be present
            "min_matches": 2       # Minimum number of matches required
        }
    }
```

#### Domain-Specific Keywords

```python
@agent_test(criteria=['contains'])
def test_medical_terminology():
    """Test for domain-specific terminology."""
    medical_terms = [
        "diagnosis", "treatment", "symptoms",
        "patient", "medication", "therapy"
    ]

    return {
        "input": "Explain diabetes management",
        "actual": medical_agent_response,
        "contains": medical_terms,
        "contains_config": {
            "min_matches": 4,      # At least 4 medical terms
            "case_sensitive": False
        }
    }
```

## 🔍 Regex Evaluator

The Regex Evaluator validates outputs against regular expression patterns for structured data and format compliance.

### Configuration

```yaml
evaluators:
  - name: 'regex'
    type: 'regex_pattern'
    config:
      flags: ['IGNORECASE', 'MULTILINE']
      match_all: true # All patterns must match
      extract_groups: true # Extract matched groups
    weight: 1.0
    enabled: true
```

### Basic Usage

```python
@agent_test(criteria=['regex'])
def test_email_extraction():
    """Test if response contains valid email format."""
    return {
        "input": "Extract contact information",
        "actual": agent_response,
        "patterns": [r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"]
    }
```

### Common Regex Patterns

#### Contact Information

```python
@agent_test(criteria=['regex'])
def test_contact_patterns():
    """Test for various contact information patterns."""
    patterns = {
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "phone": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
        "url": r"https?://(?:[-\w.])+(?:\:[0-9]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:\#(?:[\w.])*)?)?",
        "zip_code": r"\b\d{5}(?:-\d{4})?\b"
    }

    return {
        "input": "Format contact details",
        "actual": agent_response,
        "patterns": list(patterns.values()),
        "pattern_names": list(patterns.keys())
    }
```

#### Structured Data

```python
@agent_test(criteria=['regex'])
def test_json_structure():
    """Test for valid JSON structure."""
    return {
        "input": "Return data as JSON",
        "actual": agent_response,
        "patterns": [
            r'^\s*\{.*\}\s*$',                    # Valid JSON object
            r'"[^"]+"\s*:\s*"[^"]*"',             # Key-value pairs
            r'"name"\s*:\s*"[^"]*"',              # Required name field
            r'"id"\s*:\s*\d+'                     # Required numeric ID
        ]
    }
```

#### Date and Time

```python
@agent_test(criteria=['regex'])
def test_datetime_formats():
    """Test for various date/time formats."""
    datetime_patterns = [
        r'\b\d{4}-\d{2}-\d{2}\b',                      # YYYY-MM-DD
        r'\b\d{2}/\d{2}/\d{4}\b',                      # MM/DD/YYYY
        r'\b\d{1,2}:\d{2}(?::\d{2})?\s*(?:AM|PM)\b',   # Time with AM/PM
        r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s+\d{4}\b'  # Month DD, YYYY
    ]

    return {
        "input": "Include current date and time",
        "actual": agent_response,
        "patterns": datetime_patterns,
        "regex_config": {
            "match_all": False,    # Any date format is acceptable
            "min_matches": 1
        }
    }
```

#### Code Validation

```python
@agent_test(criteria=['regex'])
def test_python_code():
    """Test for valid Python code patterns."""
    python_patterns = [
        r'def\s+\w+\s*\([^)]*\)\s*:',          # Function definition
        r'import\s+\w+|from\s+\w+\s+import',   # Import statements
        r'if\s+.*:\s*$',                       # If statements
        r'for\s+\w+\s+in\s+.*:\s*$',          # For loops
        r'return\s+.*$'                        # Return statements
    ]

    return {
        "input": "Write a Python function",
        "actual": agent_code,
        "patterns": python_patterns,
        "regex_config": {
            "flags": ["MULTILINE"],
            "min_matches": 2  # At least function def + one other construct
        }
    }
```

## 💡 Advanced Usage

### Combined Pattern Validation

```python
@agent_test(criteria=['contains', 'regex'])
def test_comprehensive_validation():
    """Combine contains and regex for thorough validation."""
    return {
        "input": "Create a user profile with contact info",
        "actual": agent_response,

        # Contains validation
        "contains": ["name", "email", "phone", "address"],

        # Regex validation
        "patterns": [
            r'"name"\s*:\s*"[^"]+\"',              # Name field
            r'"email"\s*:\s*"[^@]+@[^"]+\"',       # Email field
            r'"phone"\s*:\s*"\d{3}-\d{3}-\d{4}"'   # Phone field
        ]
    }
```

### Dynamic Pattern Generation

```python
@agent_test(criteria=['regex'])
def test_dynamic_patterns():
    """Generate patterns based on context."""

    def generate_patterns(domain):
        if domain == "finance":
            return [
                r'\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?',  # Currency
                r'\b\d{4}-\d{4}-\d{4}-\d{4}\b',       # Credit card
                r'\b\d{3}-\d{2}-\d{4}\b'              # SSN
            ]
        elif domain == "medical":
            return [
                r'\b\d{3}-\d{2}-\d{4}\b',             # Patient ID
                r'\b(?:mg|ml|g|kg|lb)\b',             # Medical units
                r'\b\d+/\d+\s*mmHg\b'                 # Blood pressure
            ]
        return []

    domain = "finance"
    patterns = generate_patterns(domain)

    return {
        "input": f"Generate {domain} report",
        "actual": agent_response,
        "patterns": patterns
    }
```

### Multi-Level Validation

```python
@agent_test(criteria=['regex'])
def test_multi_level_validation():
    """Validate at multiple structural levels."""

    validation_levels = {
        "document_structure": [
            r'^# .+$',                    # Title (H1)
            r'^## .+$',                   # Section headers (H2)
            r'^\d+\. .+$'                 # Numbered lists
        ],
        "content_quality": [
            r'\b\w{10,}\b',              # Complex words (10+ chars)
            r'[.!?]\s+[A-Z]',            # Proper sentence structure
            r'\b(?:however|therefore|furthermore|moreover)\b'  # Transition words
        ],
        "formatting": [
            r'\*\*[^*]+\*\*',            # Bold text
            r'`[^`]+`',                  # Code snippets
            r'\[[^\]]+\]\([^)]+\)'       # Markdown links
        ]
    }

    return {
        "input": "Write a technical blog post",
        "actual": agent_response,
        "patterns": [pattern for patterns in validation_levels.values() for pattern in patterns],
        "pattern_groups": validation_levels
    }
```

## 📊 Configuration Options

### Contains Evaluator Options

| Option           | Type    | Default | Description                   |
| ---------------- | ------- | ------- | ----------------------------- |
| `case_sensitive` | Boolean | `false` | Case-sensitive matching       |
| `match_all`      | Boolean | `true`  | All items must be present     |
| `partial_match`  | Boolean | `true`  | Allow substring matching      |
| `min_matches`    | Integer | `null`  | Minimum number of matches     |
| `exact_match`    | Boolean | `false` | Require exact word boundaries |

### Regex Evaluator Options

| Option           | Type    | Default | Description                    |
| ---------------- | ------- | ------- | ------------------------------ |
| `flags`          | List    | `[]`    | Regex flags (IGNORECASE, etc.) |
| `match_all`      | Boolean | `true`  | All patterns must match        |
| `min_matches`    | Integer | `null`  | Minimum pattern matches        |
| `extract_groups` | Boolean | `false` | Extract matched groups         |
| `multiline`      | Boolean | `false` | Enable multiline mode          |

### Regex Flags

```python
# Available regex flags
regex_flags = [
    "IGNORECASE",    # Case-insensitive matching
    "MULTILINE",     # ^ and $ match line boundaries
    "DOTALL",        # . matches newlines
    "VERBOSE",       # Allow comments in patterns
    "ASCII",         # ASCII-only matching
    "LOCALE"         # Locale-dependent matching
]
```

## 🔍 Result Format

### Contains Evaluator Results

```python
{
    "passed": True,
    "score": 0.75,  # Percentage of required items found
    "threshold": 1.0,
    "details": {
        "required_items": ["solar", "wind", "sustainable", "environment"],
        "found_items": ["solar", "wind", "sustainable"],
        "missing_items": ["environment"],
        "match_count": 3,
        "total_required": 4,
        "case_sensitive": False
    }
}
```

### Regex Evaluator Results

```python
{
    "passed": True,
    "score": 1.0,
    "threshold": 1.0,
    "details": {
        "patterns": [
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        ],
        "matches": [
            {
                "pattern": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
                "found": True,
                "match_text": "user@example.com",
                "position": [45, 61],
                "groups": []
            }
        ],
        "total_patterns": 1,
        "successful_matches": 1
    }
}
```

## 📋 Best Practices

### Pattern Design

#### Contains Patterns

```python
# Good: Specific, relevant keywords
good_contains = ["machine learning", "neural networks", "deep learning"]

# Avoid: Too generic or common words
avoid_contains = ["the", "and", "is", "very"]

# Better: Domain-specific terms
domain_contains = ["convolutional", "backpropagation", "gradient descent"]
```

#### Regex Patterns

```python
# Good: Specific, well-escaped patterns
good_regex = r'\b\d{3}-\d{2}-\d{4}\b'  # SSN format

# Avoid: Overly broad patterns
avoid_regex = r'.*'  # Matches everything

# Better: Structured with groups
better_regex = r'\b(\d{3})-(\d{2})-(\d{4})\b'  # Capture groups
```

### Performance Optimization

```python
@agent_test(criteria=['regex'])
def test_optimized_patterns():
    """Optimize patterns for performance."""

    # Compile patterns once (done automatically by evaluator)
    optimized_patterns = [
        r'^[A-Z][a-z]+$',        # Simple character class
        r'\b\d+\b',              # Word boundaries for precision
        r'(?:cat|dog|bird)'      # Non-capturing groups
    ]

    return {
        "input": prompt,
        "actual": response,
        "patterns": optimized_patterns,
        "regex_config": {
            "flags": ["IGNORECASE"],  # Use flags efficiently
            "match_all": False        # Early exit when possible
        }
    }
```

### Error Handling

```python
@agent_test(criteria=['regex'])
def test_with_fallback():
    """Handle pattern matching errors gracefully."""

    primary_patterns = [r'\b\d{4}-\d{2}-\d{2}\b']  # ISO date
    fallback_patterns = [r'\b\d{1,2}/\d{1,2}/\d{4}\b']  # US date

    return {
        "input": "Include today's date",
        "actual": agent_response,
        "patterns": primary_patterns,
        "fallback_patterns": fallback_patterns,
        "regex_config": {
            "use_fallback": True
        }
    }
```

## 🚨 Troubleshooting

### Common Issues

**No Matches Found**

```python
# Debug with verbose output
@agent_test(criteria=['contains'])
def debug_contains():
    return {
        "input": prompt,
        "actual": response,
        "contains": ["keyword"],
        "contains_config": {
            "debug": True,           # Show detailed matching info
            "case_sensitive": False  # Check case sensitivity
        }
    }
```

**Regex Pattern Errors**

```python
# Test patterns separately
import re

def test_pattern(pattern, text):
    try:
        matches = re.findall(pattern, text)
        print(f"Pattern: {pattern}")
        print(f"Matches: {matches}")
        return len(matches) > 0
    except re.error as e:
        print(f"Regex error: {e}")
        return False
```

**Performance Issues**

```python
# Optimize for large texts
@agent_test(criteria=['regex'])
def test_performance_optimized():
    return {
        "input": prompt,
        "actual": large_response,
        "patterns": [r'\b\w+@\w+\.\w+\b'],  # Simple email pattern
        "regex_config": {
            "max_length": 10000,    # Limit text length
            "timeout": 5.0          # Pattern matching timeout
        }
    }
```

## 📚 Examples

See [Basic Examples](../examples/basic.md#pattern-matching-examples) for more pattern matching usage patterns.
