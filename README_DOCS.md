# AgentTest Documentation Setup

This repository includes comprehensive documentation built with [MkDocs](https://www.mkdocs.org/) and hosted on GitHub Pages.

## 📚 Documentation Structure

The documentation is organized in the `docs/` directory with the following structure:

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
├── examples/                   # Examples and tutorials
├── api/                        # API reference
├── stylesheets/               # Custom CSS
├── javascripts/               # Custom JavaScript
├── includes/                  # Reusable content
└── snippets/                  # Content snippets
```

## 🚀 Quick Start

### 1. Install Documentation Dependencies

```bash
# Install all documentation dependencies
pip install -e ".[docs]"

# Or use the helper script
./scripts/docs.sh install
```

### 2. Serve Documentation Locally

```bash
# Start development server
mkdocs serve

# Or use the helper script
./scripts/docs.sh serve
```

The documentation will be available at http://localhost:8000

### 3. Build Documentation

```bash
# Build static site
mkdocs build

# Or use the helper script
./scripts/docs.sh build
```

## 🛠️ Documentation Helper Script

We provide a convenient helper script at `scripts/docs.sh`:

```bash
# Start development server (default)
./scripts/docs.sh serve

# Build documentation
./scripts/docs.sh build

# Build with strict mode (fail on warnings)
./scripts/docs.sh build-strict

# Deploy to GitHub Pages
./scripts/docs.sh deploy

# Check for broken links
./scripts/docs.sh check-links

# Clean build artifacts
./scripts/docs.sh clean

# Install dependencies
./scripts/docs.sh install

# Show help
./scripts/docs.sh help
```

## 🌐 GitHub Pages Deployment

### Automatic Deployment

Documentation is automatically deployed to GitHub Pages when changes are pushed to the `main` branch. The deployment is handled by the GitHub Actions workflow in `.github/workflows/docs.yml`.

The documentation will be available at: `https://your-username.github.io/your-repo-name/`

### Manual Deployment

You can also deploy manually:

```bash
# Deploy to GitHub Pages
mkdocs gh-deploy

# Or use the helper script
./scripts/docs.sh deploy
```

### Setting Up GitHub Pages

1. **Enable GitHub Pages**:

   - Go to your repository settings
   - Navigate to "Pages" section
   - Select "GitHub Actions" as the source

2. **Configure Repository Secrets** (optional):

   - Add `GOOGLE_ANALYTICS_KEY` for analytics tracking

3. **Update Repository URLs**:
   - Edit `mkdocs.yml` to update the `site_url` and repository URLs
   - Update the `repo_name` and `repo_url` fields

## 🎨 Customization

### Theme Configuration

The documentation uses the Material theme with custom styling:

- **Colors**: Blue primary theme with light/dark mode support
- **Fonts**: Roboto for text, Roboto Mono for code
- **Features**: Navigation tabs, search, code copying, etc.

### Custom Assets

- **CSS**: `docs/stylesheets/extra.css` - Custom styling
- **JavaScript**: `docs/javascripts/extra.js` - Interactive features
- **Images**: Store in `docs/images/` (create as needed)

### Configuration Files

- **mkdocs.yml**: Main MkDocs configuration
- **pyproject.toml**: Python dependencies including docs extras
- **.github/workflows/docs.yml**: GitHub Actions deployment workflow

## 📝 Writing Documentation

### Markdown Extensions

The documentation supports advanced Markdown features:

- **Admonitions**: `!!! note "Title"`
- **Code highlighting**: Syntax highlighting for multiple languages
- **Tabs**: `=== "Tab Title"`
- **Mermaid diagrams**: ```mermaid
- **Abbreviations**: Hover definitions for acronyms
- **Footnotes**: `[^1]` syntax

### Custom CSS Classes

Use these classes for consistent styling:

- `.evaluator-similarity` - Blue highlight for similarity content
- `.evaluator-llm-judge` - Orange highlight for LLM judge content
- `.evaluator-metrics` - Green highlight for metrics content
- `.evaluator-patterns` - Purple highlight for pattern content

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

## 🔍 Search and Navigation

- **Full-text search**: Powered by MkDocs search plugin
- **Navigation tabs**: Main sections in top navigation
- **Table of contents**: Auto-generated for each page
- **Breadcrumbs**: Show current location in site hierarchy

## 🧪 Testing Documentation

### Build Validation

```bash
# Build with strict mode (fail on warnings)
mkdocs build --strict

# Check for broken links
./scripts/docs.sh check-links
```

### Link Checking

The documentation automatically validates internal links. For external links, consider using additional tools:

```bash
# Install link checker (if available)
pip install markdown-link-check

# Check links
find docs -name "*.md" -exec markdown-link-check {} \;
```

## 📊 Analytics

Google Analytics can be configured by:

1. Setting the `GOOGLE_ANALYTICS_KEY` environment variable
2. Adding it as a repository secret in GitHub
3. The analytics will be automatically included in the deployed site

## 🤝 Contributing to Documentation

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

## 🔗 Resources

- [MkDocs Documentation](https://www.mkdocs.org/)
- [Material Theme Docs](https://squidfunk.github.io/mkdocs-material/)
- [Markdown Guide](https://www.markdownguide.org/)
- [Python-Markdown Extensions](https://python-markdown.github.io/extensions/)

## 📞 Support

If you encounter issues with the documentation:

1. Check the [GitHub Actions workflow](https://github.com/your-username/your-repo-name/actions) for deployment status
2. Review the MkDocs build output for errors
3. Open an issue in the repository for help

---

**Happy documenting!** 📚✨
