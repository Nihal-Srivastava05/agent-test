"""
Project initialization for AgentTest.

Handles setting up new projects with templates and examples.
"""

from pathlib import Path

from ..utils.exceptions import AgentTestError
from .config import Config


def initialize_project(
    project_path: Path, template: str = "basic", overwrite: bool = False
) -> bool:
    """
    Initialize a new AgentTest project.

    Args:
        project_path: Directory to initialize
        template: Template to use (basic, langchain, llamaindex)
        overwrite: Whether to overwrite existing files

    Returns:
        True if successful, False otherwise
    """
    project_path = Path(project_path)
    agenttest_dir = project_path / ".agenttest"

    # Check if project already exists
    if agenttest_dir.exists() and not overwrite:
        raise AgentTestError(
            f"AgentTest project already exists in {project_path}. "
            "Use --overwrite to replace existing configuration."
        )

    try:
        # Create directory structure
        _create_directory_structure(project_path, template)

        # Create configuration file
        config = Config.create_default(template)
        config.save(agenttest_dir / "config.yaml")

        # Create example files
        _create_example_files(project_path, template)

        # Create templates
        _create_templates(project_path, template)

        return True

    except Exception as e:
        raise AgentTestError(f"Failed to initialize project: {e}")


def _create_directory_structure(project_path: Path, template: str) -> None:
    """Create the basic directory structure."""
    directories = [
        ".agenttest",
        ".agenttest/results",
        ".agenttest/templates",
        "tests",
        "examples",
    ]

    # Template-specific directories
    if template in ["langchain", "llamaindex"]:
        directories.extend(
            [
                "agents",
                "data",
            ]
        )

    for directory in directories:
        (project_path / directory).mkdir(parents=True, exist_ok=True)


def _create_example_files(project_path: Path, template: str) -> None:
    """Create example test files and agents."""

    # Create basic example test
    basic_test_content = '''"""
Example AgentTest test file.

This demonstrates basic testing patterns with the @agent_test decorator.
"""

from agenttest import agent_test, run_test


def simple_agent(input_text: str) -> str:
    """A simple agent that echoes the input with a prefix."""
    return f"Agent response: {input_text}"


@agent_test(criteria=["similarity", "llm_judge"])
def test_simple_agent():
    """Test the simple agent with basic input."""
    input_text = "Hello, world!"
    expected = "Agent response: Hello, world!"

    actual = simple_agent(input_text)

    # AgentTest will automatically evaluate using configured criteria
    return {
        "input": input_text,
        "expected": expected,
        "actual": actual
    }


@agent_test(criteria=["similarity"])
def test_agent_with_different_inputs():
    """Test agent with various inputs."""
    test_cases = [
        {
            "input": "What is AI?",
            "expected": "Agent response: What is AI?"
        },
        {
            "input": "How are you?",
            "expected": "Agent response: How are you?"
        }
    ]

    results = []
    for case in test_cases:
        actual = simple_agent(case["input"])
        results.append({
            "input": case["input"],
            "expected": case["expected"],
            "actual": actual
        })

    return results


if __name__ == "__main__":
    # You can run tests directly or use: agenttest run
    print("Example test - run with: agenttest run")
'''

    (project_path / "tests" / "test_example.py").write_text(basic_test_content)

    # Template-specific examples
    if template == "langchain":
        _create_langchain_examples(project_path)
    elif template == "llamaindex":
        _create_llamaindex_examples(project_path)


def _create_langchain_examples(project_path: Path) -> None:
    """Create LangChain-specific examples."""

    agent_content = '''"""
Example LangChain agent for AgentTest.
"""

try:
    from langchain.llms import OpenAI
    from langchain.chains import LLMChain
    from langchain.prompts import PromptTemplate
except ImportError:
    print("LangChain not installed. Install with: pip install agenttest[langchain]")
    raise


class SummarizerAgent:
    """A simple LangChain-based summarization agent."""

    def __init__(self):
        self.llm = OpenAI(temperature=0)

        prompt_template = PromptTemplate(
            input_variables=["text"],
            template="Please summarize the following text in 2-3 sentences:\\n\\n{text}\\n\\nSummary:"
        )

        self.chain = LLMChain(llm=self.llm, prompt=prompt_template)

    def summarize(self, text: str) -> str:
        """Summarize the given text."""
        return self.chain.run(text=text)


# Global instance for testing
summarizer = SummarizerAgent()


def run_summarization(text: str) -> str:
    """Function wrapper for the summarizer agent."""
    return summarizer.summarize(text)
'''

    (project_path / "agents" / "langchain_agent.py").write_text(agent_content)

    # LangChain test example
    test_content = '''"""
Example tests for LangChain agents.
"""

from agenttest import agent_test
from agents.langchain_agent import run_summarization


@agent_test(criteria=["similarity", "llm_judge"])
def test_summarization():
    """Test text summarization."""
    input_text = """
    Artificial Intelligence (AI) is a branch of computer science that aims to create
    intelligent machines capable of performing tasks that typically require human
    intelligence. These tasks include learning, reasoning, problem-solving, perception,
    and language understanding. AI has applications in various fields such as healthcare,
    finance, transportation, and entertainment.
    """

    actual = run_summarization(input_text)

    # For summarization, we don't have a fixed expected output
    # Instead, we rely on LLM-as-judge evaluation
    return {
        "input": input_text,
        "actual": actual,
        "evaluation_criteria": {
            "conciseness": "Summary should be 2-3 sentences",
            "accuracy": "Summary should capture main points",
            "clarity": "Summary should be clear and readable"
        }
    }


@agent_test(criteria=["llm_judge"])
def test_empty_input_handling():
    """Test how agent handles empty input."""
    input_text = ""
    actual = run_summarization(input_text)

    return {
        "input": input_text,
        "actual": actual,
        "evaluation_criteria": {
            "robustness": "Agent should handle empty input gracefully"
        }
    }
'''

    (project_path / "tests" / "test_langchain_agent.py").write_text(test_content)


def _create_llamaindex_examples(project_path: Path) -> None:
    """Create LlamaIndex-specific examples."""

    agent_content = '''"""
Example LlamaIndex agent for AgentTest.
"""

try:
    from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
    from llama_index.llms import OpenAI
except ImportError:
    print("LlamaIndex not installed. Install with: pip install agenttest[llamaindex]")
    raise


class RAGAgent:
    """A simple RAG agent using LlamaIndex."""

    def __init__(self, data_dir: str = "data"):
        llm = OpenAI(model="gpt-3.5-turbo", temperature=0)
        service_context = ServiceContext.from_defaults(llm=llm)

        # Load documents from data directory
        try:
            documents = SimpleDirectoryReader(data_dir).load_data()
            self.index = VectorStoreIndex.from_documents(
                documents, service_context=service_context
            )
        except Exception:
            # If no documents, create empty index
            self.index = VectorStoreIndex([], service_context=service_context)

        self.query_engine = self.index.as_query_engine()

    def query(self, question: str) -> str:
        """Query the RAG system."""
        response = self.query_engine.query(question)
        return str(response)


# Global instance for testing
rag_agent = RAGAgent()


def run_query(question: str) -> str:
    """Function wrapper for the RAG agent."""
    return rag_agent.query(question)
'''

    (project_path / "agents" / "llama_agent.py").write_text(agent_content)

    # Create sample data file
    sample_data = """
AgentTest is a pytest-like testing framework for AI agents and prompts.

Key features:
- CLI-based test runner with pytest-like interface
- Git-aware logging and regression tracking
- Support for multiple agent frameworks (LangChain, LlamaIndex, custom)
- Built-in evaluation engines (string similarity, LLM-as-judge)
- Automated test case generation using AI
- Integration with CI/CD pipelines

AgentTest helps developers ensure their AI agents are reliable, performant, and free from regressions.
"""

    (project_path / "data" / "agenttest_info.txt").write_text(sample_data)


def _create_templates(project_path: Path, template: str) -> None:
    """Create template files for test generation."""

    python_test_template = '''"""
Generated test for {{ agent_name }}.

This test was automatically generated by AgentTest.
"""

from agenttest import agent_test
from {{ agent_module }} import {{ agent_function }}


{% for test_case in test_cases %}
@agent_test(criteria={{ criteria }})
def test_{{ agent_name }}_case_{{ loop.index }}():
    """{{ test_case.description }}"""
    input_data = {{ test_case.input | tojson }}
    {% if test_case.expected %}
    expected = {{ test_case.expected | tojson }}
    {% endif %}

    actual = {{ agent_function }}(input_data)

    return {
        "input": input_data,
        {% if test_case.expected %}
        "expected": expected,
        {% endif %}
        "actual": actual,
        {% if test_case.evaluation_criteria %}
        "evaluation_criteria": {{ test_case.evaluation_criteria | tojson }}
        {% endif %}
    }

{% endfor %}
'''

    yaml_test_template = """# Generated tests for {{ agent_name }}
# This file was automatically generated by AgentTest

agent: {{ agent_name }}
criteria: {{ criteria }}

test_cases:
{% for test_case in test_cases %}
  - name: "{{ test_case.name }}"
    description: "{{ test_case.description }}"
    input: {{ test_case.input | tojson }}
    {% if test_case.expected %}
    expected: {{ test_case.expected | tojson }}
    {% endif %}
    {% if test_case.evaluation_criteria %}
    evaluation_criteria: {{ test_case.evaluation_criteria | tojson }}
    {% endif %}
{% endfor %}
"""

    templates_dir = project_path / ".agenttest" / "templates"
    (templates_dir / "test_template.py.j2").write_text(python_test_template)
    (templates_dir / "test_template.yaml.j2").write_text(yaml_test_template)

    # Create .gitignore for the project
    gitignore_content = """# AgentTest
.agenttest/results/
.agenttest/.env

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
"""

    (project_path / ".gitignore").write_text(gitignore_content)
