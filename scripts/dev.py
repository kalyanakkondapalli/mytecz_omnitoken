#!/usr/bin/env python3
"""
Development utility script for MyTecZ OmniToken.

This script provides development utilities for the MyTecZ OmniToken project
including code formatting, linting, testing, and documentation generation.

Usage:
    python scripts/dev.py [command]
    
Commands:
    format      - Format code with black and isort
    lint        - Run linting with flake8 and pylint
    type-check  - Run type checking with mypy
    test        - Run test suite
    test-watch  - Run tests in watch mode
    docs        - Generate documentation
    install-dev - Install development dependencies
    pre-commit  - Run pre-commit checks
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
from typing import List, Optional


class DevManager:
    """Manages development tasks for the project."""
    
    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize development manager.
        
        Args:
            project_root: Path to project root directory
        """
        self.project_root = project_root or Path(__file__).parent.parent
        self.src_dirs = ["omnitoken", "tests", "examples", "scripts"]
    
    def run_command(self, command: List[str], check: bool = True) -> subprocess.CompletedProcess:
        """
        Run a shell command.
        
        Args:
            command: Command to run as list of strings
            check: Whether to check return code
            
        Returns:
            CompletedProcess result
        """
        print(f"Running: {' '.join(command)}")
        
        try:
            result = subprocess.run(
                command,
                cwd=self.project_root,
                check=check,
                text=True
            )
            return result
            
        except subprocess.CalledProcessError as e:
            print(f"Command failed with exit code {e.returncode}")
            if hasattr(e, 'stdout') and e.stdout:
                print("STDOUT:", e.stdout)
            if hasattr(e, 'stderr') and e.stderr:
                print("STDERR:", e.stderr)
            raise
    
    def install_dev_dependencies(self) -> None:
        """Install development dependencies."""
        print("📦 Installing development dependencies...")
        
        dev_dependencies = [
            # Testing
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
            
            # Code formatting
            "black>=23.0.0",
            "isort>=5.12.0",
            
            # Linting
            "flake8>=6.0.0",
            "pylint>=2.17.0",
            "mypy>=1.5.0",
            
            # Documentation
            "sphinx>=6.0.0",
            "sphinx-rtd-theme>=1.2.0",
            
            # Build tools
            "build>=0.10.0",
            "twine>=4.0.0",
            
            # Pre-commit hooks
            "pre-commit>=3.0.0",
        ]
        
        self.run_command([sys.executable, "-m", "pip", "install", "--upgrade"] + dev_dependencies)
        print("✅ Development dependencies installed")
    
    def format_code(self) -> None:
        """Format code with black and isort."""
        print("🎨 Formatting code...")
        
        # Run black
        print("Running black...")
        for src_dir in self.src_dirs:
            src_path = self.project_root / src_dir
            if src_path.exists():
                self.run_command([
                    sys.executable, "-m", "black",
                    "--line-length", "88",
                    "--target-version", "py310",
                    str(src_path)
                ])
        
        # Run isort
        print("Running isort...")
        for src_dir in self.src_dirs:
            src_path = self.project_root / src_dir
            if src_path.exists():
                self.run_command([
                    sys.executable, "-m", "isort",
                    "--profile", "black",
                    "--line-length", "88",
                    str(src_path)
                ])
        
        print("✅ Code formatting completed")
    
    def lint_code(self) -> None:
        """Run linting with flake8 and pylint."""
        print("🔍 Linting code...")
        
        # Run flake8
        print("Running flake8...")
        flake8_config = [
            "--max-line-length=88",
            "--extend-ignore=E203,W503",  # Ignore black conflicts
            "--exclude=__pycache__,*.egg-info,build,dist"
        ]
        
        for src_dir in self.src_dirs:
            src_path = self.project_root / src_dir
            if src_path.exists():
                try:
                    self.run_command([
                        sys.executable, "-m", "flake8"
                    ] + flake8_config + [str(src_path)])
                except subprocess.CalledProcessError:
                    print(f"⚠️  Flake8 found issues in {src_dir}")
        
        # Run pylint on main package
        print("Running pylint...")
        omnitoken_path = self.project_root / "omnitoken"
        if omnitoken_path.exists():
            try:
                self.run_command([
                    sys.executable, "-m", "pylint",
                    "--rcfile=.pylintrc" if (self.project_root / ".pylintrc").exists() else "",
                    str(omnitoken_path)
                ])
            except subprocess.CalledProcessError:
                print("⚠️  Pylint found issues")
        
        print("✅ Linting completed")
    
    def type_check(self) -> None:
        """Run type checking with mypy."""
        print("🔬 Running type checking...")
        
        # Run mypy
        mypy_config = [
            "--ignore-missing-imports",
            "--strict-optional",
            "--warn-redundant-casts",
            "--warn-unused-ignores",
            "--show-error-codes"
        ]
        
        omnitoken_path = self.project_root / "omnitoken"
        if omnitoken_path.exists():
            try:
                self.run_command([
                    sys.executable, "-m", "mypy"
                ] + mypy_config + [str(omnitoken_path)])
            except subprocess.CalledProcessError:
                print("⚠️  MyPy found type issues")
        
        print("✅ Type checking completed")
    
    def run_tests(self) -> None:
        """Run the test suite."""
        print("🧪 Running tests...")
        
        test_command = [
            sys.executable, "-m", "pytest",
            "tests/",
            "-v",
            "--tb=short",
            "--cov=omnitoken",
            "--cov-report=term-missing",
            "--cov-report=html"
        ]
        
        try:
            self.run_command(test_command)
            print("✅ Tests completed successfully")
        except subprocess.CalledProcessError:
            print("❌ Some tests failed")
            raise
    
    def test_watch(self) -> None:
        """Run tests in watch mode."""
        print("👀 Running tests in watch mode...")
        print("Press Ctrl+C to stop watching...")
        
        try:
            self.run_command([
                sys.executable, "-m", "pytest",
                "tests/",
                "-v",
                "--tb=short",
                "-f"  # Fail fast
            ])
        except KeyboardInterrupt:
            print("\n⚠️  Test watching stopped")
    
    def generate_docs(self) -> None:
        """Generate documentation."""
        print("📚 Generating documentation...")
        
        docs_dir = self.project_root / "docs"
        docs_dir.mkdir(exist_ok=True)
        
        # Create basic Sphinx configuration if it doesn't exist
        conf_py = docs_dir / "conf.py"
        if not conf_py.exists():
            self._create_sphinx_config(docs_dir)
        
        # Generate API documentation
        try:
            self.run_command([
                sys.executable, "-m", "sphinx.ext.autodoc",
                "-o", str(docs_dir),
                str(self.project_root / "omnitoken")
            ])
        except subprocess.CalledProcessError:
            print("⚠️  Autodoc generation failed, continuing...")
        
        # Build HTML documentation
        try:
            self.run_command([
                sys.executable, "-m", "sphinx.cmd.build",
                "-b", "html",
                str(docs_dir),
                str(docs_dir / "_build" / "html")
            ])
            
            html_index = docs_dir / "_build" / "html" / "index.html"
            if html_index.exists():
                print(f"📖 Documentation available at: {html_index}")
            
        except subprocess.CalledProcessError:
            print("⚠️  Documentation build failed")
        
        print("✅ Documentation generation completed")
    
    def _create_sphinx_config(self, docs_dir: Path) -> None:
        """Create basic Sphinx configuration."""
        conf_content = '''"""
Configuration file for Sphinx documentation builder.
"""
import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.abspath('..'))

# Project information
project = 'MyTecZ OmniToken'
copyright = '2024, MyTecZ'
author = 'MyTecZ'
release = '1.0.0'

# Extensions
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
]

# Templates
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# HTML output
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Autodoc settings
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}
'''
        
        with open(docs_dir / "conf.py", 'w') as f:
            f.write(conf_content)
    
    def pre_commit_checks(self) -> None:
        """Run pre-commit checks."""
        print("🔒 Running pre-commit checks...")
        
        try:
            # Format code
            self.format_code()
            
            # Lint code
            self.lint_code()
            
            # Type check
            self.type_check()
            
            # Run tests
            self.run_tests()
            
            print("✅ All pre-commit checks passed!")
            
        except subprocess.CalledProcessError:
            print("❌ Pre-commit checks failed!")
            raise
    
    def setup_pre_commit_hooks(self) -> None:
        """Setup pre-commit hooks."""
        print("🪝 Setting up pre-commit hooks...")
        
        # Create .pre-commit-config.yaml if it doesn't exist
        pre_commit_config = self.project_root / ".pre-commit-config.yaml"
        if not pre_commit_config.exists():
            config_content = '''repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      
  - repo: https://github.com/psf/black
    rev: 23.7.0
    hooks:
      - id: black
        language_version: python3
        
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
'''
            
            with open(pre_commit_config, 'w') as f:
                f.write(config_content)
        
        # Install pre-commit hooks
        self.run_command([sys.executable, "-m", "pre_commit", "install"])
        
        print("✅ Pre-commit hooks setup completed")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Development utilities for MyTecZ OmniToken",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/dev.py install-dev    # Install development dependencies
  python scripts/dev.py format         # Format code with black and isort
  python scripts/dev.py lint           # Run linting checks
  python scripts/dev.py test           # Run test suite
  python scripts/dev.py pre-commit     # Run all pre-commit checks
        """
    )
    
    parser.add_argument(
        "command",
        choices=[
            "install-dev", "format", "lint", "type-check", "test", 
            "test-watch", "docs", "pre-commit", "setup-hooks"
        ],
        help="Command to execute"
    )
    
    args = parser.parse_args()
    
    # Create dev manager
    dev_manager = DevManager()
    
    # Execute command
    command_map = {
        "install-dev": dev_manager.install_dev_dependencies,
        "format": dev_manager.format_code,
        "lint": dev_manager.lint_code,
        "type-check": dev_manager.type_check,
        "test": dev_manager.run_tests,
        "test-watch": dev_manager.test_watch,
        "docs": dev_manager.generate_docs,
        "pre-commit": dev_manager.pre_commit_checks,
        "setup-hooks": dev_manager.setup_pre_commit_hooks
    }
    
    try:
        command_map[args.command]()
    except KeyboardInterrupt:
        print("\n⚠️  Operation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()