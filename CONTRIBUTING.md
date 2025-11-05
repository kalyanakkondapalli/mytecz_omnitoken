# Contributing to MyTecZ OmniToken 🤝

Thank you for your interest in contributing to MyTecZ OmniToken! We welcome contributions from the community and are grateful for any help in improving this project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Documentation](#documentation)
- [Issue Reporting](#issue-reporting)

## 🤝 Code of Conduct

This project adheres to a Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

### Our Standards

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## 🚀 Getting Started

### Types of Contributions

We welcome several types of contributions:

- **🐛 Bug Reports**: Help us identify and fix issues
- **✨ Feature Requests**: Suggest new functionality
- **📝 Documentation**: Improve or add documentation
- **🔧 Code Contributions**: Bug fixes, features, optimizations
- **🧪 Tests**: Add or improve test coverage
- **📊 Performance**: Optimization and benchmarking

### Quick Start for Contributors

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Set up the development environment**
4. **Create a feature branch**
5. **Make your changes**
6. **Run tests**
7. **Submit a pull request**

## 🛠️ Development Setup

### Prerequisites

- Python 3.10 or higher
- Git
- pip (package installer for Python)

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/mytecz-omnitoken.git
   cd mytecz-omnitoken
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install development dependencies**:
   ```bash
   pip install -e ".[dev]"
   
   # Or using the dev script
   python scripts/dev.py install-dev
   ```

4. **Set up pre-commit hooks** (optional but recommended):
   ```bash
   python scripts/dev.py setup-hooks
   ```

### Development Scripts

We provide several utility scripts to help with development:

```bash
# Code formatting
python scripts/dev.py format

# Linting
python scripts/dev.py lint

# Type checking
python scripts/dev.py type-check

# Running tests
python scripts/dev.py test

# Generate documentation
python scripts/dev.py docs

# Run all pre-commit checks
python scripts/dev.py pre-commit
```

## 🔄 Making Changes

### Creating a Feature Branch

Always create a new branch for your changes:

```bash
# Update main branch
git checkout main
git pull origin main

# Create a new feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b bugfix/issue-description
```

### Branch Naming Convention

- **Features**: `feature/description-of-feature`
- **Bug fixes**: `bugfix/description-of-fix`
- **Documentation**: `docs/description-of-change`
- **Tests**: `test/description-of-test`
- **Refactoring**: `refactor/description-of-refactor`

### Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
type(scope): short description

Longer description explaining what and why vs. how.

Fixes #123
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding or updating tests
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `style`: Code style changes (formatting, etc.)
- `chore`: Maintenance tasks

**Examples:**
```bash
feat(tokenizer): add support for custom special tokens
fix(bpe): resolve memory leak in merge operations
docs(readme): update installation instructions
test(unicode): add tests for emoji handling
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python scripts/dev.py test

# Run specific test file
pytest tests/test_basic.py

# Run tests with coverage
pytest --cov=omnitoken --cov-report=html

# Run tests in watch mode
python scripts/dev.py test-watch
```

### Writing Tests

We use **pytest** for testing. Tests should be:

- **Comprehensive**: Cover normal cases, edge cases, and error conditions
- **Fast**: Individual tests should run quickly
- **Independent**: Tests should not depend on each other
- **Clear**: Test names and code should be self-explanatory

#### Test Structure

```python
import pytest
from omnitoken import OmniToken

class TestFeatureName:
    """Test class for specific feature."""
    
    @pytest.fixture
    def sample_data(self):
        """Fixture providing test data."""
        return ["sample", "data", "for", "testing"]
    
    def test_basic_functionality(self, sample_data):
        """Test basic functionality works as expected."""
        tokenizer = OmniToken(method="bpe", vocab_size=100)
        tokenizer.fit(sample_data)
        
        result = tokenizer.encode("test text")
        
        assert isinstance(result, list)
        assert len(result) > 0
    
    def test_error_handling(self):
        """Test that errors are handled appropriately."""
        tokenizer = OmniToken(method="bpe")
        
        with pytest.raises(ValueError, match="must be trained"):
            tokenizer.encode("test")
    
    @pytest.mark.parametrize("method", ["bpe", "wordpiece", "sentencepiece"])
    def test_multiple_methods(self, method, sample_data):
        """Test functionality across different methods."""
        tokenizer = OmniToken(method=method, vocab_size=100)
        tokenizer.fit(sample_data)
        
        result = tokenizer.encode("test")
        assert len(result) > 0
```

### Test Categories

We use pytest markers to categorize tests:

- `@pytest.mark.unit`: Unit tests (fast, isolated)
- `@pytest.mark.integration`: Integration tests (slower, multiple components)
- `@pytest.mark.slow`: Slow tests (performance, large datasets)
- `@pytest.mark.gpu`: Tests requiring GPU (skipped if not available)

### Coverage Requirements

- **New code**: Must have at least 90% test coverage
- **Bug fixes**: Must include tests reproducing the bug
- **Features**: Must include comprehensive tests for all functionality

## 📥 Pull Request Process

### Before Submitting

1. **Run all checks**:
   ```bash
   python scripts/dev.py pre-commit
   ```

2. **Update documentation** if needed

3. **Add tests** for any new functionality

4. **Update CHANGELOG.md** if applicable

### Pull Request Template

When creating a pull request, please:

1. **Use a clear, descriptive title**
2. **Reference related issues** (`Fixes #123`, `Closes #456`)
3. **Describe your changes** in detail
4. **Include screenshots** if UI changes are involved
5. **List any breaking changes**

### Review Process

1. **Automated checks** must pass (CI/CD pipeline)
2. **Code review** by at least one maintainer
3. **Testing** on multiple environments
4. **Documentation review** if docs are changed
5. **Final approval** and merge

### After Your PR is Merged

- **Delete your feature branch**
- **Update your local main branch**
- **Consider contributing more!**

## 📏 Coding Standards

### Python Style

We follow [PEP 8](https://pep8.org/) with some modifications:

- **Line length**: 88 characters (Black formatter standard)
- **Quotes**: Use double quotes for strings
- **Imports**: Organized with isort
- **Type hints**: Required for all public functions

### Code Quality Tools

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking
- **pylint**: Additional linting

### Documentation Standards

- **Docstrings**: Use Google-style docstrings
- **Type hints**: All public functions must have type hints
- **Comments**: Explain why, not what
- **Examples**: Include usage examples in docstrings

#### Docstring Example

```python
def encode_text(text: str, method: str = "bpe") -> List[int]:
    """
    Encode text into token IDs using specified method.
    
    Args:
        text: Input text to tokenize
        method: Tokenization method ("bpe", "wordpiece", "sentencepiece")
        
    Returns:
        List of token IDs representing the input text
        
    Raises:
        ValueError: If tokenizer is not trained or method is invalid
        
    Example:
        >>> tokenizer = OmniToken(method="bpe")
        >>> tokenizer.fit(["training", "data"])
        >>> ids = tokenizer.encode("hello world")
        >>> print(ids)
        [15, 23, 42]
    """
```

## 📖 Documentation

### Types of Documentation

- **README**: Project overview and quick start
- **API Documentation**: Generated from docstrings
- **Tutorials**: Step-by-step guides
- **Examples**: Practical usage examples
- **Contributing Guide**: This document

### Building Documentation

```bash
# Generate API documentation
python scripts/dev.py docs

# View generated docs
open docs/_build/html/index.html
```

### Documentation Guidelines

- **Clear and concise**: Use simple language
- **Examples**: Include practical examples
- **Up-to-date**: Keep docs synchronized with code
- **Accessible**: Consider different skill levels

## 🐛 Issue Reporting

### Before Creating an Issue

1. **Search existing issues** to avoid duplicates
2. **Check the documentation** for solutions
3. **Try the latest version** to see if it's already fixed

### Bug Report Template

```markdown
## Bug Description
A clear and concise description of the bug.

## Steps to Reproduce
1. Create tokenizer with...
2. Train on data...
3. Call method...
4. See error

## Expected Behavior
What you expected to happen.

## Actual Behavior
What actually happened.

## Environment
- OS: [e.g. Windows 10, macOS 12, Ubuntu 20.04]
- Python: [e.g. 3.10.2]
- MyTecZ OmniToken: [e.g. 1.0.0]
- Other relevant packages: [e.g. numpy 1.21.0]

## Additional Context
Any additional information that might help.
```

### Feature Request Template

```markdown
## Feature Description
A clear and concise description of the feature.

## Motivation
Why is this feature needed? What problem does it solve?

## Proposed Solution
How would you like this feature to work?

## Alternatives Considered
Other solutions you've considered.

## Additional Context
Any additional information or context.
```

## 🏷️ Release Process

### Version Numbers

We use [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backwards compatible)
- **PATCH**: Bug fixes (backwards compatible)

### Release Checklist

- [ ] Update version numbers
- [ ] Update CHANGELOG.md
- [ ] Run full test suite
- [ ] Update documentation
- [ ] Create release notes
- [ ] Tag release
- [ ] Build and publish to PyPI

## 📞 Getting Help

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and community discussion
- **Email**: Direct contact with maintainers

### Questions and Support

- **Documentation**: Check our comprehensive docs first
- **Examples**: Look at practical examples in the repo
- **Issues**: Search existing issues for similar problems
- **Discussions**: Ask questions in GitHub Discussions

## 🙏 Recognition

Contributors will be recognized in:

- **README**: Contributors section
- **CHANGELOG**: Release notes
- **Documentation**: Author acknowledgments
- **Releases**: Release notes and announcements

## 📜 License

By contributing to MyTecZ OmniToken, you agree that your contributions will be licensed under the MIT License.

---

## 🎉 Thank You!

Thank you for contributing to MyTecZ OmniToken! Your help makes this project better for everyone. Every contribution, no matter how small, is valuable and appreciated.

**Happy coding! 🚀**