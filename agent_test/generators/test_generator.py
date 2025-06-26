"""
Test generator for AgentTest.

Automatically generates test cases using LLMs by analyzing agent code and docstrings.
"""

import ast
import inspect
import importlib.util
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
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
        if not hasattr(self.config, 'llm'):
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
            raise GenerationError("OpenAI package not installed. Install with: pip install openai")
    
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
            raise GenerationError("Anthropic package not installed. Install with: pip install anthropic")
    
    def _setup_gemini_client(self):
        """Setup Google Gemini client."""
        try:
            import google.generativeai as genai
            
            api_key = self.config.llm.api_key
            if not api_key:
                import os
                api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
            
            if not api_key:
                raise GenerationError("Google API key not found. Set GOOGLE_API_KEY or GEMINI_API_KEY environment variable")
            
            genai.configure(api_key=api_key)
            self.llm_client = genai.GenerativeModel(self.config.llm.model or 'gemini-pro')
            self.model = self.config.llm.model or 'gemini-pro'
            
        except ImportError:
            raise GenerationError("Google Generative AI package not installed. Install with: pip install google-generativeai")
    
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
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for agent-related patterns
            agent_indicators = [
                "agent", "Agent", "chain", "Chain", 
                "llm", "LLM", "openai", "anthropic",
                "langchain", "llama_index"
            ]
            
            content_lower = content.lower()
            return any(indicator.lower() in content_lower for indicator in agent_indicators)
            
        except Exception:
            return False
    
    def generate_tests(
        self,
        agent_path: str,
        count: int = 5,
        format: str = "python"
    ) -> str:
        """Generate test cases for an agent."""
        # Analyze the agent
        agent_info = self._analyze_agent(agent_path)
        
        # Generate test cases using LLM
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
            with open(file_path, 'r', encoding='utf-8') as f:
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
                "docstring": ast.get_docstring(tree) or ""
            }
            
            # Extract functions and classes
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_info = {
                        "name": node.name,
                        "docstring": ast.get_docstring(node) or "",
                        "args": [arg.arg for arg in node.args.args],
                        "returns": getattr(node.returns, 'id', None) if node.returns else None,
                        "is_public": not node.name.startswith('_')
                    }
                    info["functions"].append(func_info)
                
                elif isinstance(node, ast.ClassDef):
                    class_info = {
                        "name": node.name,
                        "docstring": ast.get_docstring(node) or "",
                        "methods": [],
                        "is_public": not node.name.startswith('_')
                    }
                    
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            method_info = {
                                "name": item.name,
                                "docstring": ast.get_docstring(item) or "",
                                "args": [arg.arg for arg in item.args.args],
                                "is_public": not item.name.startswith('_')
                            }
                            class_info["methods"].append(method_info)
                    
                    info["classes"].append(class_info)
                
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            info["imports"].append(alias.name)
                    else:
                        module = node.module or ""
                        for alias in node.names:
                            info["imports"].append(f"{module}.{alias.name}")
            
            return info
            
        except Exception as e:
            raise GenerationError(f"Failed to analyze agent: {str(e)}")
    
    def _generate_test_cases_with_llm(
        self, 
        agent_info: Dict[str, Any], 
        count: int
    ) -> List[Dict[str, Any]]:
        """Generate test cases using LLM."""
        
        # Create generation prompt
        prompt = self._create_generation_prompt(agent_info, count)
        
        # Get response from LLM
        response = self._get_llm_response(prompt)
        
        # Parse the response to extract test cases
        return self._parse_llm_test_cases(response)
    
    def _create_generation_prompt(self, agent_info: Dict[str, Any], count: int) -> str:
        """Create prompt for LLM test case generation."""
        
        prompt_parts = [
            "You are an expert test case generator for AI agents. Based on the following agent code,",
            "generate comprehensive test cases that cover various scenarios including edge cases.",
            "",
            "AGENT INFORMATION:",
            f"File: {agent_info['file_path']}",
            f"Module: {agent_info['module_name']}",
            ""
        ]
        
        if agent_info["docstring"]:
            prompt_parts.extend([
                "AGENT DESCRIPTION:",
                agent_info["docstring"],
                ""
            ])
        
        if agent_info["functions"]:
            prompt_parts.extend([
                "PUBLIC FUNCTIONS:",
                *[f"- {func['name']}({', '.join(func['args'])}): {func['docstring']}" 
                  for func in agent_info["functions"] if func["is_public"]],
                ""
            ])
        
        if agent_info["classes"]:
            prompt_parts.extend([
                "CLASSES:",
                *[f"- {cls['name']}: {cls['docstring']}" 
                  for cls in agent_info["classes"] if cls["is_public"]],
                ""
            ])
        
        prompt_parts.extend([
            "FRAMEWORK IMPORTS:",
            *[f"- {imp}" for imp in agent_info["imports"] 
              if any(framework in imp.lower() for framework in ["langchain", "llama", "openai", "anthropic"])],
            "",
            f"Please generate {count} test cases in the following JSON format:",
            "[",
            "  {",
            '    "name": "test_case_name",',
            '    "description": "What this test case covers",',
            '    "input": "test input data",',
            '    "expected": "expected output (if applicable)",',
            '    "evaluation_criteria": {"criterion": "description"},',
            '    "tags": ["tag1", "tag2"]',
            "  }",
            "]",
            "",
            "Focus on:",
            "1. Normal operation cases",
            "2. Edge cases (empty input, very long input, etc.)",
            "3. Error handling scenarios",
            "4. Different input types/formats",
            "5. Performance considerations",
            "",
            "Test cases:"
        ])
        
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
                {"role": "system", "content": "You are an expert test case generator. Generate test cases in valid JSON format."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.config.llm.temperature,
            max_tokens=self.config.llm.max_tokens or 2000
        )
        
        return response.choices[0].message.content
    
    def _get_anthropic_response(self, prompt: str) -> str:
        """Get response from Anthropic."""
        response = self.llm_client.messages.create(
            model=self.model,
            max_tokens=self.config.llm.max_tokens or 2000,
            temperature=self.config.llm.temperature,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.content[0].text
    
    def _get_gemini_response(self, prompt: str) -> str:
        """Get response from Google Gemini."""
        # Configure generation parameters
        generation_config = {
            'temperature': self.config.llm.temperature,
            'max_output_tokens': self.config.llm.max_tokens or 2000,
        }
        
        # Add system instruction about being a test case generator
        full_prompt = "You are an expert test case generator. Generate test cases in valid JSON format. " + prompt
        
        response = self.llm_client.generate_content(
            full_prompt,
            generation_config=generation_config
        )
        
        return response.text
    
    def _parse_llm_test_cases(self, response: str) -> List[Dict[str, Any]]:
        """Parse LLM response to extract test cases."""
        try:
            import json
            import re
            
            # Try to extract JSON array from response
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            
            if json_match:
                json_str = json_match.group()
                test_cases = json.loads(json_str)
                
                # Validate test cases
                validated_cases = []
                for case in test_cases:
                    if isinstance(case, dict) and "name" in case:
                        validated_cases.append(case)
                
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
                "input": "test input",
                "expected": None,
                "evaluation_criteria": {"accuracy": "Response should be accurate"},
                "tags": ["basic"]
            },
            {
                "name": "test_empty_input",
                "description": "Test agent with empty input",
                "input": "",
                "expected": None,
                "evaluation_criteria": {"robustness": "Should handle empty input gracefully"},
                "tags": ["edge_case"]
            }
        ]
    
    def _format_as_python(self, agent_info: Dict[str, Any], test_cases: List[Dict[str, Any]]) -> str:
        """Format test cases as Python code."""
        template_path = Path(".agenttest") / "templates" / "test_template.py.j2"
        
        if template_path.exists():
            with open(template_path, 'r') as f:
                template_content = f.read()
        else:
            # Default template
            template_content = '''"""
Generated test for {{ agent_name }}.

This test was automatically generated by AgentTest.
"""

from agenttest import agent_test
from {{ agent_module }} import *


{% for test_case in test_cases %}
@agent_test(criteria={{ test_case.evaluation_criteria.keys() | list }}, tags={{ test_case.tags }})
def {{ test_case.name }}():
    """{{ test_case.description }}"""
    input_data = {{ test_case.input | tojson }}
    {% if test_case.expected %}
    expected = {{ test_case.expected | tojson }}
    {% endif %}
    
    # TODO: Call your agent function here
    # actual = your_agent_function(input_data)
    
    return {
        "input": input_data,
        {% if test_case.expected %}
        "expected": expected,
        {% endif %}
        # "actual": actual,
        {% if test_case.evaluation_criteria %}
        "evaluation_criteria": {{ test_case.evaluation_criteria | tojson }}
        {% endif %}
    }

{% endfor %}
'''
        
        template = Template(template_content)
        
        return template.render(
            agent_name=agent_info["module_name"],
            agent_module=agent_info["module_name"],
            test_cases=test_cases
        )
    
    def _format_as_yaml(self, agent_info: Dict[str, Any], test_cases: List[Dict[str, Any]]) -> str:
        """Format test cases as YAML."""
        import yaml
        
        yaml_data = {
            "agent": agent_info["module_name"],
            "description": f"Generated tests for {agent_info['module_name']}",
            "test_cases": test_cases
        }
        
        return yaml.dump(yaml_data, default_flow_style=False, sort_keys=False)
    
    def _format_as_json(self, agent_info: Dict[str, Any], test_cases: List[Dict[str, Any]]) -> str:
        """Format test cases as JSON."""
        import json
        
        json_data = {
            "agent": agent_info["module_name"],
            "description": f"Generated tests for {agent_info['module_name']}",
            "test_cases": test_cases
        }
        
        return json.dumps(json_data, indent=2) 