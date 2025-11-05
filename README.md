# MyTecZ OmniToken 🚀

**Universal Tokenizer with Modular Architecture**

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://python.org)
[![PyPI](https://img.shields.io/pypi/v/mytecz-omnitoken.svg)](https://pypi.org/project/mytecz-omnitoken/)
[![Build](https://github.com/mytecz/omnitoken/actions/workflows/publish.yml/badge.svg)](https://github.com/mytecz/omnitoken/actions)
[![Coverage](https://img.shields.io/badge/coverage-unknown-lightgrey.svg)](#) <!-- Replace with real badge once coverage upload enabled -->
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-beta-orange.svg)](https://github.com/mytecz/omnitoken)

## 🎯 Overview

MyTecZ OmniToken is a universal tokenizer designed to overcome limitations in existing tokenization solutions. It provides a **modular architecture** that supports multiple tokenization strategies and input formats, making it ideal for diverse NLP applications.

### ✨ Key Features

- **🔧 Modular Architecture**: Plug-and-play tokenization strategies
- **📁 Multiple Input Formats**: Files, JSON, raw strings, mixed data
- **🌍 Unicode & Emoji Support**: Full international character support
- **🔄 Deterministic & Reversible**: Reliable encode/decode operations
- **🧪 Experimental Hybrid Mode**: Adaptive tokenization strategies
- **📊 Built-in Visualizer**: Debug and analyze tokenization results
- **⚡ Performance Optimized**: Efficient training and inference
- **🎛️ Configurable**: Extensive customization options

### 🛠️ Supported Tokenization Methods

- **Character-based**: Fine-grained character-level tokenization
- **BPE (Byte Pair Encoding)**: Subword tokenization with merge operations
- **WordPiece**: BERT-style tokenization with ## prefixes
- **SentencePiece**: Language-independent subword tokenization
- **Hybrid**: Experimental adaptive tokenization combining multiple strategies

## 🚀 Quick Start

### Installation

```bash
pip install mytecz-omnitoken
```

### Basic Usage

```python
from omnitoken import OmniToken

# Create tokenizer with your preferred method
tokenizer = OmniToken(method="hybrid", vocab_size=10000)

# Train on various input formats
training_data = [
    "Hello world! This is sample text.",
    {"text": "JSON input is supported"},
    "path/to/your/textfile.txt"  # File paths work too
]

tokenizer.fit(training_data)

# Encode text to tokens
text = "Hello world 👋! Unicode and emojis work perfectly 🚀"
tokens = tokenizer.encode(text)
print(f"Tokens: {tokens}")

# Decode back to text
decoded = tokenizer.decode(tokens)
print(f"Decoded: {decoded}")
```

### Advanced Example

```python
from omnitoken import OmniToken
from omnitoken.utils import TokenVisualizer

# Configure tokenizer with custom settings
tokenizer = OmniToken(
    method="bpe",
    vocab_size=5000,
    min_frequency=2,
    special_tokens=["[CUSTOM]", "[SPECIAL]"]
)

# Train with mixed data sources
mixed_data = [
    "Regular text for training",
    "data/corpus.txt",  # File input
    {"documents": ["Doc 1", "Doc 2"]},  # JSON input
    ["List", "of", "strings"]  # List input
]

tokenizer.fit(mixed_data)

# Analyze tokenization
test_text = "Analyze this tokenization example!"
tokens = tokenizer._tokenizer.tokenize(test_text)
token_ids = tokenizer.encode(test_text)

# Visualize results
visualization = TokenVisualizer.visualize_tokens(test_text, tokens, token_ids)
print(visualization)
```

### Frequency & Vocabulary Introspection

After training you can inspect vocabulary size and token frequency distribution:

```python
tok = OmniToken(method="bpe", vocab_size=500)
tok.fit(["Some training text", "More tokens here", "Text text text"])
vocab = tok.get_vocab()              # token -> id
freqs = tok.get_token_frequencies()  # token -> observed count
print(len(vocab), "vocab items", len(freqs), "with frequencies tracked")
print(sorted(tok.get_token_frequencies().items(), key=lambda x: -x[1])[:10])
```

You can also pass the alias `mode=` instead of `method=` (e.g. `OmniToken(mode="wordpiece")`).

## 📚 Documentation

### Tokenization Methods

#### BPE (Byte Pair Encoding)
```python
tokenizer = OmniToken(method="bpe", vocab_size=10000)
```
- Learns merge operations for frequent character pairs
- Good for handling out-of-vocabulary words
- Deterministic and efficient

#### WordPiece
```python
tokenizer = OmniToken(method="wordpiece", vocab_size=10000)
```
- BERT-style tokenization with ## continuation prefixes
- Greedy longest-match-first algorithm
- Excellent for transformer models

#### SentencePiece
```python
tokenizer = OmniToken(method="sentencepiece", vocab_size=10000)
```
- Language-independent tokenization
- Treats text as raw character sequence
- Robust Unicode handling

#### Hybrid (Experimental)
```python
tokenizer = OmniToken(method="hybrid", vocab_size=10000)
```
- Combines multiple strategies adaptively
- Analyzes text characteristics to choose optimal approach
- Best for diverse content types

### Input Format Support

#### String Input
```python
tokenizer.fit("Simple string input for training")
```

#### File Input
```python
tokenizer.fit("path/to/textfile.txt")
tokenizer.fit(["file1.txt", "file2.txt", "file3.txt"])
```

#### JSON Input
```python
data = {
    "texts": ["Text 1", "Text 2"],
    "metadata": "Additional content"
}
tokenizer.fit(data)
```

#### Mixed Input
```python
mixed = [
    "Direct string",
    "data/file.txt",
    {"json": "object"},
    ["list", "of", "items"]
]
tokenizer.fit(mixed)
```

## 🧪 Examples

Explore the `/examples` directory for comprehensive usage examples:

- **`example_basic.py`**: Basic usage and method comparison
- **`example_json_file_input.py`**: Advanced input format handling

Run examples:
```bash
cd examples
python example_basic.py
python example_json_file_input.py
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Basic functionality tests
python -m pytest tests/test_basic.py -v

# Round-trip tokenization tests  
python -m pytest tests/test_reverse_tokenization.py -v

# Run all tests
python -m pytest tests/ -v
```

### Test Coverage

Our test suite covers:
- ✅ Round-trip encode/decode accuracy
- ✅ Unicode and emoji handling
- ✅ All input format types
- ✅ Edge cases and error conditions
- ✅ Performance benchmarks
- ✅ Deterministic behavior
- ✅ Cross-method consistency

## ⚙️ Configuration Options

### TokenizerConfig Parameters

```python
from omnitoken import OmniToken
from omnitoken.tokenizer_base import TokenizerConfig

config = TokenizerConfig(
    vocab_size=10000,           # Maximum vocabulary size
    min_frequency=2,            # Minimum token frequency
    special_tokens=["[MASK]"],  # Custom special tokens
    unk_token="[UNK]",         # Unknown token
    pad_token="[PAD]",         # Padding token
    case_sensitive=True,        # Case sensitivity
    max_token_length=100       # Maximum token length
)

tokenizer = OmniToken(method="bpe", config=config)
```

### Method-Specific Options

#### BPE Options
```python
tokenizer = OmniToken(
    method="bpe",
    vocab_size=10000,
    dropout=0.1,                # BPE dropout for regularization
    end_of_word_suffix="</w>"   # End-of-word marker
)
```

#### WordPiece Options
```python
tokenizer = OmniToken(
    method="wordpiece",
    vocab_size=10000,
    continuation_prefix="##",    # Subword continuation prefix
    do_lower_case=True,         # Lowercase normalization
    max_input_chars_per_word=100 # Max characters per word
)
```

#### Hybrid Options
```python
tokenizer = OmniToken(
    method="hybrid",
    vocab_size=10000,
    char_ratio=0.3,             # Character vocab ratio
    word_ratio=0.4,             # Word vocab ratio  
    subword_ratio=0.3,          # Subword vocab ratio
    adaptive_mode=True          # Enable adaptive strategy selection
)
```

## 🔍 Visualization and Analysis

### Token Visualization

```python
from omnitoken.utils import TokenVisualizer

# Visualize tokenization
text = "Example text with emojis 🎯"
tokens = tokenizer._tokenizer.tokenize(text)
token_ids = tokenizer.encode(text)

viz = TokenVisualizer.visualize_tokens(text, tokens, token_ids)
print(viz)
```

### Method Comparison

```python
# Compare different tokenization methods
tokenizations = {
    "BPE": bpe_tokenizer.tokenize(text),
    "WordPiece": wp_tokenizer.tokenize(text),
    "Hybrid": hybrid_tokenizer.tokenize(text)
}

comparison = TokenVisualizer.compare_tokenizations(text, tokenizations)
print(comparison)
```

### Vocabulary Statistics

```python
vocab = tokenizer._tokenizer.get_vocab()
stats = TokenVisualizer.show_vocabulary_stats(vocab)
print(stats)
```

## 🎯 Use Cases

### Natural Language Processing
- Text preprocessing for transformer models
- Multi-language document processing
- Social media content analysis

### Code Analysis
- Programming language tokenization
- Code documentation processing
- Technical text analysis

### Content Processing
- Web scraping and text extraction
- Document indexing and search
- Content recommendation systems

### Research and Development
- Tokenization algorithm research
- Comparative analysis studies
- Custom tokenization strategies

## 🏗️ Architecture

```
mytecz_omnitoken/
├── omnitoken/
│   ├── __init__.py              # Main package interface
│   ├── tokenizer_base.py        # Abstract base class
│   ├── tokenizer_bpe.py         # BPE implementation
│   ├── tokenizer_wordpiece.py   # WordPiece implementation
│   ├── tokenizer_sentencepiece.py # SentencePiece implementation
│   ├── tokenizer_hybrid.py      # Hybrid tokenizer
│   ├── trainer.py               # Training algorithms
│   └── utils.py                 # Utilities and visualization
├── examples/                    # Usage examples
├── tests/                       # Test suite
└── README.md                    # This file
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **🐛 Report Bugs**: Open issues for bugs or unexpected behavior
2. **💡 Feature Requests**: Suggest new features or improvements
3. **📝 Documentation**: Help improve documentation and examples
4. **🧪 Testing**: Add test cases for edge cases
5. **🔧 Code**: Submit pull requests with bug fixes or features

### Development Setup

```bash
# Clone the repository
git clone https://github.com/mytecz/omnitoken.git
cd omnitoken

# Install in development mode
pip install -e .[dev]

# Run tests
python -m pytest tests/ -v

# Format code
black omnitoken/ tests/ examples/

# Type checking
mypy omnitoken/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by research in subword tokenization algorithms
- Built with love for the NLP and ML community
- Special thanks to contributors and beta testers

## 📞 Contact

- **GitHub**: [https://github.com/mytecz/omnitoken](https://github.com/mytecz/omnitoken)
- **Email**: contact@mytecz.com
- **Issues**: [https://github.com/mytecz/omnitoken/issues](https://github.com/mytecz/omnitoken/issues)

---

**Made with ❤️ by MyTecZ**

*Empowering NLP with Universal Tokenization* 🚀