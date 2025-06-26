# AgentTest Documentation

This directory contains the documentation for AgentTest, built with [MkDocs](https://www.mkdocs.org/) and the [Material theme](https://squidfunk.github.io/mkdocs-material/).

## 📁 Structure

```
docs/
├── README.md                    # Main documentation index
├── installation.md              # Installation guide
├── quickstart.md               # Quick start tutorial
├── configuration.md            # Configuration reference
├── writing-tests.md            # Test writing guide
├── cli-commands.md             # CLI reference
├── git-integration.md          # Git features
├── evaluators.md               # Evaluators overview
├── evaluators/                 # Evaluator-specific docs
│   ├── similarity.md
│   ├── llm-judge.md
│   ├── metrics.md
│   └── patterns.md
├── examples/                   # Examples and tutorials
│   └── basic.md
├── api/                        # API reference
│   └── core.md
├── stylesheets/               # Custom CSS
│   └── extra.css
├── javascripts/               # Custom JavaScript
│   └── extra.js
├── includes/                  # Reusable content
│   └── mkdocs.md
└── snippets/                  # Content snippets
    └── installation-note.md
```

## 🚀 Local Development

### Prerequisites

Install the documentation dependencies:

```bash
pip install -e ".[docs]"
```

### Running Locally

Start the development server:

```bash
mkdocs serve
```

The documentation will be available at http://localhost:8000

### Live Reload

MkDocs automatically reloads when you make changes to:

- Markdown files in `docs/`
- `mkdocs.yml` configuration
- CSS/JavaScript assets

## 🏗️ Building

Build the static site:

```bash
mkdocs build
```

The built site will be in the `site/` directory.

### Strict Mode

Build with strict mode (fails on warnings):

```bash
mkdocs build --strict
```

## 🚀 Deployment

### GitHub Pages

Documentation is automatically deployed to GitHub Pages when changes are pushed to the `main` branch. The workflow is defined in `.github/workflows/docs.yml`.

### Manual Deployment

You can also deploy manually:

```bash
mkdocs gh-deploy
```

## 📝 Writing Documentation

### Markdown Extensions

The documentation uses several Markdown extensions:

- **Admonitions**: `!!! note "Title"`
- **Code highlighting**: Syntax highlighting for multiple languages
- **Tabs**: `=== "Tab Title"`
- **Mermaid diagrams**: ```mermaid
- **Abbreviations**: Hover definitions for acronyms
- **Footnotes**: `[^1]` syntax

### Custom Styles

Custom CSS classes are available:

- `.evaluator-similarity` - Blue highlight for similarity content
- `.evaluator-llm-judge` - Orange highlight for LLM judge content
- `.evaluator-metrics` - Green highlight for metrics content
- `.evaluator-patterns` - Purple highlight for pattern content
- `.api-method` - Styling for API methods
- `.api-parameter` - Styling for API parameters

### Example Usage

```markdown
!!! tip "Pro Tip"
Use the similarity evaluator for general text comparison.

=== "Python"
`python
    @agent_test(criteria=['similarity'])
    def test_example():
        return {"input": "test", "actual": "result"}
    `

=== "YAML"
`yaml
    evaluators:
      - name: similarity
        type: string_similarity
    `
```

## 🎨 Customization

### Theme Configuration

The Material theme is configured in `mkdocs.yml`:

- **Colors**: Blue primary, supports light/dark mode
- **Fonts**: Roboto for text, Roboto Mono for code
- **Features**: Navigation tabs, instant loading, search suggestions

### Custom Assets

- **CSS**: `docs/stylesheets/extra.css`
- **JavaScript**: `docs/javascripts/extra.js`
- **Images**: Store in `docs/images/` (create as needed)

## 🔍 Search

The documentation includes:

- **Full-text search**: Powered by MkDocs search plugin
- **Search suggestions**: Auto-complete functionality
- **Search highlighting**: Results are highlighted in content

## 📊 Analytics

Google Analytics can be configured by setting the `GOOGLE_ANALYTICS_KEY` environment variable in GitHub repository secrets.

## 🧪 Testing Documentation

### Link Checking

MkDocs validates internal links automatically. External links can be checked with:

```bash
# Install link checker
pip install markdown-link-check

# Check links (if available)
find docs -name "*.md" -exec markdown-link-check {} \;
```

### Spelling

Consider using a spell checker:

```bash
# Install aspell or similar
brew install aspell  # macOS
sudo apt-get install aspell  # Ubuntu

# Check spelling
aspell check docs/README.md
```

## 📚 Resources

- [MkDocs Documentation](https://www.mkdocs.org/)
- [Material Theme Docs](https://squidfunk.github.io/mkdocs-material/)
- [Markdown Guide](https://www.markdownguide.org/)
- [Python-Markdown Extensions](https://python-markdown.github.io/extensions/)

## 🤝 Contributing

When contributing to documentation:

1. **Test locally**: Always run `mkdocs serve` to test changes
2. **Check links**: Ensure all internal links work
3. **Follow style**: Use consistent formatting and tone
4. **Add examples**: Include practical code examples
5. **Update navigation**: Add new pages to `mkdocs.yml` nav section

### Style Guide

- Use present tense ("AgentTest provides" not "AgentTest will provide")
- Use active voice ("Run the command" not "The command should be run")
- Keep sentences concise and clear
- Use code blocks for all code examples
- Include output examples where helpful
- Use admonitions for important notes, tips, and warnings
