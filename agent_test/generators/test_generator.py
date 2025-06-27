"""
Test generator for AgentTest.

Automatically generates test cases using LLMs by analyzing agent code and docstrings.
"""

import ast
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from jinja2 import Template

from ..core.config import Config
from ..utils.exceptions import GenerationError


class TestGenerator:
    """Generates test cases automatically using LLM analysis."""

    def __init__(self, config: Config):
        self.config = config
        self.llm_client = None
        self._setup_llm_client()

    def _setup_llm_client(self):
        """Setup LLM client for test generation."""
        if not hasattr(self.config, "llm"):
            raise GenerationError("LLM configuration required for test generation")

        provider = self.config.llm.provider

        if provider == "openai":
            self._setup_openai_client()
        elif provider == "anthropic":
            self._setup_anthropic_client()
        elif provider == "gemini":
            self._setup_gemini_client()
        else:
            raise GenerationError(f"Unsupported LLM provider: {provider}")

    def _setup_openai_client(self):
        """Setup OpenAI client."""
        try:
            import openai

            api_key = self.config.llm.api_key
            if not api_key:
                import os

                api_key = os.getenv("OPENAI_API_KEY")

            if not api_key:
                raise GenerationError("OpenAI API key not found")

            self.llm_client = openai.OpenAI(api_key=api_key)
            self.model = self.config.llm.model

        except ImportError:
            raise GenerationError(
                "OpenAI package not installed. Install with: pip install openai"
            )

    def _setup_anthropic_client(self):
        """Setup Anthropic client."""
        try:
            import anthropic

            api_key = self.config.llm.api_key
            if not api_key:
                import os

                api_key = os.getenv("ANTHROPIC_API_KEY")

            if not api_key:
                raise GenerationError("Anthropic API key not found")

            self.llm_client = anthropic.Anthropic(api_key=api_key)
            self.model = self.config.llm.model

        except ImportError:
            raise GenerationError(
                "Anthropic package not installed. Install with: pip install anthropic"
            )

    def _setup_gemini_client(self):
        """Setup Google Gemini client."""
        try:
            import google.generativeai as genai

            api_key = self.config.llm.api_key
            if not api_key:
                import os

                api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

            if not api_key:
                print("Warning: No LLM API key found. Using fallback test generation.")
                self.llm_client = None
                return

            genai.configure(api_key=api_key)
            self.llm_client = genai.GenerativeModel(
                self.config.llm.model or "gemini-pro"
            )
            self.model = self.config.llm.model or "gemini-pro"

        except ImportError:
            raise GenerationError(
                "Google Generative AI package not installed. Install with: pip install google-generativeai"
            )

    def discover_agents(self, search_dirs: Optional[List[str]] = None) -> List[str]:
        """Discover agent files in the project."""
        if search_dirs is None:
            search_dirs = ["agents", "src", "."]

        agent_files = []

        for search_dir in search_dirs:
            search_path = Path(search_dir)
            if search_path.exists():
                # Look for Python files that might contain agents
                for file_path in search_path.rglob("*.py"):
                    if self._is_agent_file(file_path):
                        agent_files.append(str(file_path))

        return agent_files

    def _is_agent_file(self, file_path: Path) -> bool:
        """Check if a file likely contains agent code."""
        # Skip test files and __init__.py
        if file_path.name.startswith("test_") or file_path.name == "__init__.py":
            return False

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Look for agent-related patterns
            agent_indicators = [
                "agent",
                "Agent",
                "chain",
                "Chain",
                "llm",
                "LLM",
                "openai",
                "anthropic",
                "langchain",
                "llama_index",
            ]

            content_lower = content.lower()
            return any(
                indicator.lower() in content_lower for indicator in agent_indicators
            )

        except Exception:
            return False

    def generate_tests(
        self, agent_path: str, count: int = 5, format: str = "python"
    ) -> str:
        """Generate test cases for an agent."""
        # Analyze the agent
        agent_info = self._analyze_agent(agent_path)

        # Generate test cases using LLM or fallback
        test_cases = self._generate_test_cases_with_llm(agent_info, count)

        # Format the output
        if format == "python":
            return self._format_as_python(agent_info, test_cases)
        elif format == "yaml":
            return self._format_as_yaml(agent_info, test_cases)
        elif format == "json":
            return self._format_as_json(agent_info, test_cases)
        else:
            raise GenerationError(f"Unsupported format: {format}")

    def _analyze_agent(self, agent_path: str) -> Dict[str, Any]:
        """Analyze agent code to extract relevant information."""
        file_path = Path(agent_path)

        if not file_path.exists():
            raise GenerationError(f"Agent file not found: {agent_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source_code = f.read()

            # Parse the AST
            tree = ast.parse(source_code)

            # Extract information
            info = {
                "file_path": str(file_path),
                "module_name": file_path.stem,
                "source_code": source_code,
                "functions": [],
                "classes": [],
                "imports": [],
                "docstring": ast.get_docstring(tree) or "",
                "project_structure": self._analyze_project_structure(file_path),
                "import_analysis": self._analyze_imports_and_dependencies(
                    file_path, tree
                ),
            }

            # Extract functions and classes
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_info = {
                        "name": node.name,
                        "docstring": ast.get_docstring(node) or "",
                        "args": [arg.arg for arg in node.args.args],
                        "returns": (
                            getattr(node.returns, "id", None) if node.returns else None
                        ),
                        "is_public": not node.name.startswith("_"),
                        "is_standalone": True,  # Top-level function
                        "signature": self._extract_function_signature(node),
                    }
                    info["functions"].append(func_info)

                elif isinstance(node, ast.ClassDef):
                    class_info = {
                        "name": node.name,
                        "docstring": ast.get_docstring(node) or "",
                        "methods": [],
                        "is_public": not node.name.startswith("_"),
                        "constructor_args": None,
                    }

                    # Extract methods and constructor
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            method_info = {
                                "name": item.name,
                                "docstring": ast.get_docstring(item) or "",
                                "args": [arg.arg for arg in item.args.args],
                                "is_public": not item.name.startswith("_"),
                                "is_constructor": item.name == "__init__",
                                "signature": self._extract_function_signature(item),
                            }
                            class_info["methods"].append(method_info)

                            # Store constructor arguments for object creation
                            if item.name == "__init__":
                                class_info["constructor_args"] = [
                                    arg.arg
                                    for arg in item.args.args
                                    if arg.arg != "self"
                                ]

                    info["classes"].append(class_info)

                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        info["imports"].append(alias.name)

                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    for alias in node.names:
                        info["imports"].append(f"{module}.{alias.name}")

            return info

        except Exception as e:
            raise GenerationError(f"Failed to analyze agent: {str(e)}")

    def _analyze_project_structure(self, file_path: Path) -> Dict[str, Any]:
        """Analyze project structure to understand import paths."""
        project_root = self._find_project_root(file_path)
        relative_path = file_path.relative_to(project_root)

        # Build module path
        module_parts = list(relative_path.parts[:-1])  # Exclude filename
        if relative_path.stem != "__init__":
            module_parts.append(relative_path.stem)

        module_path = ".".join(module_parts) if module_parts else relative_path.stem

        return {
            "project_root": str(project_root),
            "relative_path": str(relative_path),
            "module_path": module_path,
            "package_structure": self._analyze_package_structure(project_root),
            "is_package": (project_root / "__init__.py").exists(),
        }

    def _find_project_root(self, file_path: Path) -> Path:
        """Find the project root directory."""
        current = file_path.parent

        # Look for common project indicators
        project_indicators = [
            "pyproject.toml",
            "setup.py",
            "requirements.txt",
            ".git",
            ".gitignore",
            "README.md",
            "README.rst",
        ]

        while current != current.parent:
            if any((current / indicator).exists() for indicator in project_indicators):
                return current
            current = current.parent

        # Fallback to current directory
        return file_path.parent

    def _analyze_package_structure(self, project_root: Path) -> Dict[str, Any]:
        """Analyze package structure for better imports."""
        packages = []
        modules = []

        for py_file in project_root.rglob("*.py"):
            if py_file.name == "__init__.py":
                package_path = py_file.parent.relative_to(project_root)
                if package_path != Path("."):
                    packages.append(str(package_path).replace(os.sep, "."))
            else:
                module_path = py_file.relative_to(project_root)
                module_name = str(module_path.with_suffix("")).replace(os.sep, ".")
                modules.append(module_name)

        return {"packages": packages, "modules": modules}

    def _analyze_imports_and_dependencies(
        self, file_path: Path, tree: ast.AST
    ) -> Dict[str, Any]:
        """Analyze imports to understand what needs to be imported for tests."""
        imports = {
            "standard_library": [],
            "third_party": [],
            "local": [],
            "from_imports": {},
            "required_for_tests": [],
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    import_type = self._classify_import(alias.name)
                    imports[import_type].append(alias.name)

            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                import_type = self._classify_import(module)

                if module not in imports["from_imports"]:
                    imports["from_imports"][module] = []

                for alias in node.names:
                    imports["from_imports"][module].append(alias.name)

        # Determine what imports are needed for testing
        imports["required_for_tests"] = self._determine_test_imports(file_path, imports)

        return imports

    def _classify_import(self, module_name: str) -> str:
        """Classify import as standard library, third party, or local."""
        if not module_name:
            return "local"

        # Standard library modules (partial list)
        stdlib_modules = {
            "os",
            "sys",
            "json",
            "re",
            "datetime",
            "time",
            "random",
            "math",
            "collections",
            "itertools",
            "functools",
            "pathlib",
            "typing",
            "dataclasses",
            "enum",
            "abc",
            "asyncio",
            "threading",
            "multiprocessing",
        }

        root_module = module_name.split(".")[0]

        if root_module in stdlib_modules:
            return "standard_library"
        elif root_module in [
            "openai",
            "anthropic",
            "google",
            "langchain",
            "llama_index",
        ]:
            return "third_party"
        else:
            return "local"

    def _determine_test_imports(
        self, file_path: Path, imports: Dict[str, Any]
    ) -> List[str]:
        """Determine what imports are needed for testing."""
        required = []

        # Always need the agent_test decorator
        required.append("from agent_test import agent_test")

        # Add imports for the module being tested
        project_structure = self._analyze_project_structure(file_path)
        module_path = project_structure["module_path"]

        if module_path:
            required.append(f"from {module_path} import *")

        # Add any third-party dependencies that might be needed
        for module in imports["third_party"]:
            if module in ["openai", "anthropic", "google.generativeai"]:
                required.append(f"import {module}")

        return required

    def _extract_function_signature(self, node: ast.FunctionDef) -> Dict[str, Any]:
        """Extract detailed function signature information."""
        signature = {
            "name": node.name,
            "args": [],
            "defaults": [],
            "has_varargs": node.args.vararg is not None,
            "has_kwargs": node.args.kwarg is not None,
            "return_annotation": None,
        }

        # Extract arguments with their types if annotated
        for i, arg in enumerate(node.args.args):
            arg_info = {
                "name": arg.arg,
                "annotation": (
                    getattr(arg.annotation, "id", None) if arg.annotation else None
                ),
                "has_default": i >= len(node.args.args) - len(node.args.defaults),
            }
            signature["args"].append(arg_info)

        # Extract default values
        for default in node.args.defaults:
            if isinstance(default, ast.Constant):
                signature["defaults"].append(default.value)
            else:
                signature["defaults"].append("...")

        # Extract return annotation
        if node.returns:
            signature["return_annotation"] = getattr(node.returns, "id", None)

        return signature

    def _generate_test_cases_with_llm(
        self, agent_info: Dict[str, Any], count: int
    ) -> List[Dict[str, Any]]:
        """Generate test cases using LLM or fallback."""
        if self.llm_client is None:
            print("No LLM client available, using enhanced fallback test generation...")
            return self._create_enhanced_fallback_test_cases(agent_info, count)

        try:
            prompt = self._create_generation_prompt(agent_info, count)
            response = self._get_llm_response(prompt)
            test_cases = self._parse_llm_test_cases(response)

            if not test_cases:
                test_cases = self._create_enhanced_fallback_test_cases(
                    agent_info, count
                )

            return test_cases[:count]  # Limit to requested count

        except Exception as e:
            print(f"Warning: LLM generation failed: {e}")
            return self._create_enhanced_fallback_test_cases(agent_info, count)

    def _create_enhanced_fallback_test_cases(
        self, agent_info: Dict[str, Any], count: int
    ) -> List[Dict[str, Any]]:
        """Create enhanced fallback test cases based on code analysis."""
        test_cases = []

        # Test standalone functions
        for func in agent_info["functions"]:
            if func["is_public"] and func["is_standalone"]:
                test_cases.extend(self._generate_function_tests(func, agent_info))

        # Test class methods
        for cls in agent_info["classes"]:
            if cls["is_public"]:
                test_cases.extend(self._generate_class_tests(cls, agent_info))

        # Ensure we have at least the requested count
        while len(test_cases) < count:
            test_cases.append(
                {
                    "name": f"test_general_functionality_{len(test_cases) + 1}",
                    "description": "General functionality test",
                    "function_to_test": "",
                    "input_data": {"input": "test data"},
                    "expected_behavior": "Should work correctly",
                    "evaluation_criteria": {
                        "functionality": "Should execute without errors",
                        "output": "Should produce expected output",
                    },
                    "tags": ["general", "fallback"],
                }
            )

        return test_cases[:count]

    def _generate_function_tests(
        self, func: Dict[str, Any], agent_info: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate test cases for a standalone function."""
        tests = []
        func_name = func["name"]
        signature = func["signature"]

        # Basic functionality test
        input_data = self._generate_input_data(signature)
        tests.append(
            {
                "name": f"test_{func_name}_basic",
                "description": f"Test basic functionality of {func_name}",
                "function_to_test": func_name,
                "input_data": input_data,
                "expected_behavior": f"Should execute {func_name} successfully",
                "evaluation_criteria": {
                    "execution": "Function should execute without errors",
                    "output_type": "Should return appropriate type",
                    "functionality": "Should perform expected operation",
                },
                "tags": ["basic", "function"],
            }
        )

        # Edge case test if function has arguments
        if signature["args"]:
            edge_input = self._generate_edge_case_input(signature)
            tests.append(
                {
                    "name": f"test_{func_name}_edge_case",
                    "description": f"Test edge cases for {func_name}",
                    "function_to_test": func_name,
                    "input_data": edge_input,
                    "expected_behavior": "Should handle edge cases gracefully",
                    "evaluation_criteria": {
                        "robustness": "Should handle edge cases without crashing",
                        "error_handling": "Should provide appropriate error handling",
                    },
                    "tags": ["edge_case", "function"],
                }
            )

        return tests

    def _generate_class_tests(
        self, cls: Dict[str, Any], agent_info: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate test cases for a class."""
        tests = []
        class_name = cls["name"]

        # Constructor test
        if cls["constructor_args"]:
            constructor_input = self._generate_constructor_input(cls)
            tests.append(
                {
                    "name": f"test_{class_name.lower()}_creation",
                    "description": f"Test creation of {class_name} object",
                    "function_to_test": class_name,
                    "input_data": constructor_input,
                    "expected_behavior": f"Should create {class_name} instance successfully",
                    "evaluation_criteria": {
                        "instantiation": "Object should be created successfully",
                        "attributes": "Object attributes should be set correctly",
                    },
                    "tags": ["basic", "class", "constructor"],
                }
            )

        # Method tests
        for method in cls["methods"]:
            if method["is_public"] and not method["is_constructor"]:
                method_input = self._generate_method_input(method, cls)
                tests.append(
                    {
                        "name": f"test_{class_name.lower()}_{method['name']}",
                        "description": f"Test {method['name']} method of {class_name}",
                        "function_to_test": f"{class_name}.{method['name']}",
                        "input_data": method_input,
                        "expected_behavior": f"Should execute {method['name']} method successfully",
                        "evaluation_criteria": {
                            "method_execution": "Method should execute without errors",
                            "return_value": "Should return appropriate value",
                        },
                        "tags": ["method", "class"],
                    }
                )

        return tests

    def _generate_input_data(self, signature: Dict[str, Any]) -> Dict[str, Any]:
        """Generate realistic input data based on function signature."""
        input_data = {}

        for i, arg in enumerate(signature["args"]):
            if arg["name"] == "self":
                continue

            # Generate data based on argument name and type hints
            arg_name = arg["name"]
            annotation = arg["annotation"]

            if "query" in arg_name.lower():
                input_data[arg_name] = "test query"
            elif "text" in arg_name.lower():
                input_data[arg_name] = "test text"
            elif "message" in arg_name.lower():
                input_data[arg_name] = "test message"
            elif "data" in arg_name.lower():
                input_data[arg_name] = {"key": "value"}
            elif "id" in arg_name.lower():
                input_data[arg_name] = "test_id"
            elif "name" in arg_name.lower():
                input_data[arg_name] = "test_name"
            elif "type" in arg_name.lower():
                input_data[arg_name] = "test_type"
            elif "count" in arg_name.lower() or "num" in arg_name.lower():
                input_data[arg_name] = 5
            elif annotation == "bool":
                input_data[arg_name] = True
            elif annotation == "int":
                input_data[arg_name] = 42
            elif annotation == "float":
                input_data[arg_name] = 3.14
            elif annotation == "list":
                input_data[arg_name] = ["item1", "item2"]
            elif annotation == "dict":
                input_data[arg_name] = {"key": "value"}
            else:
                # Default to string
                input_data[arg_name] = f"test_{arg_name}"

        return input_data

    def _generate_edge_case_input(self, signature: Dict[str, Any]) -> Dict[str, Any]:
        """Generate edge case input data."""
        input_data = {}

        for arg in signature["args"]:
            if arg["name"] == "self":
                continue

            arg_name = arg["name"]
            annotation = arg["annotation"]

            # Generate edge case values
            if "query" in arg_name.lower() or "text" in arg_name.lower():
                input_data[arg_name] = ""  # Empty string
            elif annotation == "int":
                input_data[arg_name] = 0
            elif annotation == "list":
                input_data[arg_name] = []
            elif annotation == "dict":
                input_data[arg_name] = {}
            else:
                input_data[arg_name] = f"test_{arg_name}"

        return input_data

    def _generate_constructor_input(self, cls: Dict[str, Any]) -> Dict[str, Any]:
        """Generate input data for class constructor."""
        input_data = {}

        for arg_name in cls["constructor_args"]:
            if "api_key" in arg_name.lower():
                input_data[arg_name] = "test_api_key"
            elif "url" in arg_name.lower():
                input_data[arg_name] = "https://test.example.com"
            elif "config" in arg_name.lower():
                input_data[arg_name] = {"setting": "value"}
            elif "model" in arg_name.lower():
                input_data[arg_name] = "test_model"
            else:
                input_data[arg_name] = f"test_{arg_name}"

        return input_data

    def _generate_method_input(
        self, method: Dict[str, Any], cls: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate input data for class method."""
        input_data = {}

        # Add class instance creation info
        if cls["constructor_args"]:
            input_data["_class_instance"] = {
                "class_name": cls["name"],
                "constructor_args": self._generate_constructor_input(cls),
            }

        # Add method arguments
        for arg_name in method["args"]:
            if arg_name in ["self"]:
                continue

            if "query" in arg_name.lower():
                input_data[arg_name] = "test query for method"
            elif "data" in arg_name.lower():
                input_data[arg_name] = {"method_data": "value"}
            else:
                input_data[arg_name] = f"test_{arg_name}"

        return input_data

    def _create_generation_prompt(self, agent_info: Dict[str, Any], count: int) -> str:
        """Create prompt for LLM test case generation."""

        prompt_parts = [
            "You are an expert test case generator for AI agents and Python code. Analyze the following code and generate comprehensive test cases.",
            "",
            "AGENT INFORMATION:",
            f"File: {agent_info['file_path']}",
            f"Module: {agent_info['module_name']}",
            f"Module Path: {agent_info['project_structure']['module_path']}",
            "",
        ]

        if agent_info["docstring"]:
            prompt_parts.extend(["AGENT DESCRIPTION:", agent_info["docstring"], ""])

        # Add source code excerpt for better context
        source_lines = agent_info["source_code"].split("\n")[:50]  # First 50 lines
        prompt_parts.extend(
            ["CODE SAMPLE (first 50 lines):", "```python", *source_lines, "```", ""]
        )

        if agent_info["functions"]:
            prompt_parts.extend(
                [
                    "PUBLIC FUNCTIONS TO TEST:",
                    *[
                        f"- {func['name']}({', '.join(func['args'])}): {func['docstring']}"
                        for func in agent_info["functions"]
                        if func["is_public"]
                    ],
                    "",
                ]
            )

        if agent_info["classes"]:
            prompt_parts.extend(
                [
                    "CLASSES TO TEST:",
                ]
            )
            for cls in agent_info["classes"]:
                if cls["is_public"]:
                    prompt_parts.append(f"- {cls['name']}: {cls['docstring']}")
                    public_methods = [m for m in cls["methods"] if m["is_public"]]
                    if public_methods:
                        prompt_parts.extend(
                            [
                                "  Methods:",
                                *[
                                    f"    - {method['name']}({', '.join(method['args'])}): {method['docstring']}"
                                    for method in public_methods
                                ],
                            ]
                        )
            prompt_parts.append("")

        prompt_parts.extend(
            [
                f"Generate {count} comprehensive test cases in the following EXACT JSON format:",
                "[",
                "  {",
                '    "name": "test_function_name_descriptive",',
                '    "description": "Clear description of what this test validates",',
                '    "function_to_test": "actual_function_name_from_code",',
                '    "input_data": {"key": "value"},',
                '    "expected_behavior": "What should happen",',
                '    "evaluation_criteria": {',
                '      "accuracy": "Response should be accurate and relevant",',
                '      "format": "Output should be in correct format",',
                '      "error_handling": "Should handle errors gracefully"',
                "    },",
                '    "tags": ["category", "priority"]',
                "  }",
                "]",
                "",
                "REQUIREMENTS:",
                "1. Use ACTUAL function names from the code above",
                "2. Create realistic input data based on function signatures",
                "3. Include specific evaluation criteria (3-5 criteria per test)",
                "4. Cover these scenarios:",
                "   - Normal operation with typical inputs",
                "   - Edge cases (empty, null, boundary values)",
                "   - Error conditions (invalid inputs, exceptions)",
                "   - Performance considerations (large inputs)",
                "   - Integration scenarios (if applicable)",
                "",
                "5. Make test names descriptive and follow Python naming conventions",
                "6. Ensure evaluation criteria are specific and measurable",
                "7. Use appropriate tags: ['basic', 'edge_case', 'error_handling', 'performance', 'integration']",
                "",
                "Generate the JSON array now:",
            ]
        )

        return "\n".join(prompt_parts)

    def _get_llm_response(self, prompt: str) -> str:
        """Get response from LLM."""
        try:
            provider = self.config.llm.provider

            if provider == "openai":
                return self._get_openai_response(prompt)
            elif provider == "anthropic":
                return self._get_anthropic_response(prompt)
            elif provider == "gemini":
                return self._get_gemini_response(prompt)
            else:
                raise GenerationError(f"Unsupported provider: {provider}")

        except Exception as e:
            raise GenerationError(f"LLM API call failed: {str(e)}")

    def _get_openai_response(self, prompt: str) -> str:
        """Get response from OpenAI."""
        response = self.llm_client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert test case generator. Generate test cases in valid JSON format exactly as requested."
                        + " Focus on creating realistic, comprehensive test cases."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=self.config.llm.temperature,
            max_tokens=self.config.llm.max_tokens or 3000,
        )

        return response.choices[0].message.content

    def _get_anthropic_response(self, prompt: str) -> str:
        """Get response from Anthropic."""
        response = self.llm_client.messages.create(
            model=self.model,
            max_tokens=self.config.llm.max_tokens or 3000,
            temperature=self.config.llm.temperature,
            messages=[{"role": "user", "content": prompt}],
        )

        return response.content[0].text

    def _get_gemini_response(self, prompt: str) -> str:
        """Get response from Google Gemini."""
        # Configure generation parameters
        generation_config = {
            "temperature": self.config.llm.temperature,
            "max_output_tokens": self.config.llm.max_tokens or 3000,
        }

        # Add system instruction about being a test case generator
        full_prompt = (
            "You are an expert test case generator. Generate test cases in valid JSON format exactly as requested."
            + " Focus on creating realistic, comprehensive test cases.\n\n"
            + prompt
        )

        response = self.llm_client.generate_content(
            full_prompt, generation_config=generation_config
        )

        return response.text

    def _parse_llm_test_cases(self, response: str) -> List[Dict[str, Any]]:
        """Parse LLM response to extract test cases."""
        try:
            import json
            import re

            # Try to extract JSON array from response
            json_match = re.search(r"\[.*\]", response, re.DOTALL)

            if json_match:
                json_str = json_match.group()
                test_cases = json.loads(json_str)

                # Validate and enhance test cases
                validated_cases = []
                for case in test_cases:
                    if isinstance(case, dict) and "name" in case:
                        # Ensure required fields exist
                        enhanced_case = {
                            "name": case.get("name", "test_unnamed"),
                            "description": case.get(
                                "description", "Generated test case"
                            ),
                            "function_to_test": case.get("function_to_test", ""),
                            "input_data": case.get("input_data", case.get("input", {})),
                            "expected_behavior": case.get(
                                "expected_behavior", case.get("expected", "")
                            ),
                            "evaluation_criteria": case.get(
                                "evaluation_criteria",
                                {"accuracy": "Should work correctly"},
                            ),
                            "tags": case.get("tags", ["generated"]),
                        }
                        validated_cases.append(enhanced_case)

                return validated_cases
            else:
                # Fallback: create basic test cases
                return self._create_fallback_test_cases()

        except Exception as e:
            print(f"Warning: Failed to parse LLM response: {e}")
            return self._create_fallback_test_cases()

    def _create_fallback_test_cases(self) -> List[Dict[str, Any]]:
        """Create basic fallback test cases."""
        return [
            {
                "name": "test_basic_functionality",
                "description": "Test basic agent functionality",
                "function_to_test": "",
                "input_data": {"query": "test input"},
                "expected_behavior": "Should return a valid response",
                "evaluation_criteria": {
                    "accuracy": "Response should be accurate",
                    "format": "Response should be properly formatted",
                    "completeness": "Response should address the input",
                },
                "tags": ["basic", "generated"],
            },
            {
                "name": "test_empty_input",
                "description": "Test agent with empty input",
                "function_to_test": "",
                "input_data": {"query": ""},
                "expected_behavior": "Should handle empty input gracefully",
                "evaluation_criteria": {
                    "robustness": "Should handle empty input gracefully",
                    "error_handling": "Should not crash on empty input",
                    "user_experience": "Should provide helpful feedback",
                },
                "tags": ["edge_case", "error_handling"],
            },
        ]

    def _format_as_python(
        self, agent_info: Dict[str, Any], test_cases: List[Dict[str, Any]]
    ) -> str:
        """Format test cases as Python code."""
        template_path = Path(".agenttest") / "templates" / "test_template.py.j2"

        if template_path.exists():
            with open(template_path, "r") as f:
                template_content = f.read()
        else:
            # Enhanced default template
            template_content = '''"""
Generated test for {{ agent_name }}.

This test was automatically generated by AgentTest.
"""

from agent_test import agent_test
{% if agent_module_path %}
from {{ agent_module_path }} import *
{% else %}
# TODO: Import your agent functions here
# from your_module import your_function
{% endif %}


{% for test_case in test_cases %}
@agent_test(
    criteria=[{% for criterion in test_case.evaluation_criteria.keys() %}"{{ criterion }}"{% if not loop.last %}, {% endif %}{% endfor %}],
    tags={{ test_case.tags | tojson }}
)
def {{ test_case.name }}():
    """{{ test_case.description }}"""
    {% if test_case.input_data -%}
    input_data = {{ test_case.input_data | tojson }}
    {%- else -%}
    input_data = {}
    {%- endif %}
    {% if test_case.expected_behavior -%}
    expected_behavior = {{ test_case.expected_behavior | tojson }}
    {%- endif %}

    {% if test_case.function_to_test -%}
    # Call the function being tested
    {% if "." in test_case.function_to_test -%}
    # Class method call
    {% set class_method = test_case.function_to_test.split(".") -%}
    {% if test_case.input_data.get("_class_instance") -%}
    instance = {{ class_method[0] }}(**{{ test_case.input_data._class_instance.constructor_args | tojson }})
    actual = instance.{{ class_method[1] }}({% for key, value in test_case.input_data.items() if key != "_class_instance" %}{{ key }}={{ value | tojson }}{% if not loop.last %}, {% endif %}{% endfor %})
    {%- else -%}
    # TODO: Create instance of {{ class_method[0] }} with appropriate arguments
    # instance = {{ class_method[0] }}(api_key="your_api_key")
    # actual = instance.{{ class_method[1] }}(**input_data)
    actual = None
    {%- endif %}
    {%- else -%}
    # Function call
    {% if test_case.input_data -%}
    actual = {{ test_case.function_to_test }}(**input_data)
    {%- else -%}
    actual = {{ test_case.function_to_test }}()
    {%- endif %}
    {%- endif %}
    {%- else -%}
    # TODO: Call your agent function here
    # actual = your_agent_function(input_data)
    actual = None  # Replace with actual function call
    {%- endif %}

    return {
        "input": input_data,
        {% if test_case.expected_behavior -%}
        "expected_behavior": expected_behavior,
        {%- endif %}
        "actual": actual,
        "evaluation_criteria": {{ test_case.evaluation_criteria | tojson }}
    }

{% endfor %}
'''

        template = Template(template_content)

        # Use the analyzed project structure for imports
        project_structure = agent_info.get("project_structure", {})
        agent_module_path = project_structure.get("module_path", None)

        return template.render(
            agent_name=agent_info["module_name"],
            agent_module_path=agent_module_path,
            test_cases=test_cases,
        )

    def _format_as_yaml(
        self, agent_info: Dict[str, Any], test_cases: List[Dict[str, Any]]
    ) -> str:
        """Format test cases as YAML."""
        import yaml

        yaml_data = {
            "agent": agent_info["module_name"],
            "description": f"Generated tests for {agent_info['module_name']}",
            "test_cases": test_cases,
        }

        return yaml.dump(yaml_data, default_flow_style=False, sort_keys=False)

    def _format_as_json(
        self, agent_info: Dict[str, Any], test_cases: List[Dict[str, Any]]
    ) -> str:
        """Format test cases as JSON."""
        import json

        json_data = {
            "agent": agent_info["module_name"],
            "description": f"Generated tests for {agent_info['module_name']}",
            "test_cases": test_cases,
        }

        return json.dumps(json_data, indent=2)
