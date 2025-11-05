"""
JSON and File Input Example for MyTecZ OmniToken.

This example demonstrates how to use OmniToken with various input formats
including JSON objects, file inputs, and mixed data sources.
"""

import sys
import os
import json
import tempfile

# Add the parent directory to the path so we can import omnitoken
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from omnitoken import OmniToken
from omnitoken.utils import TokenVisualizer


def create_sample_files():
    """Create sample files for testing file input functionality."""
    
    # Create temporary directory for sample files
    temp_dir = tempfile.mkdtemp(prefix="omnitoken_example_")
    
    # Sample text file
    text_file = os.path.join(temp_dir, "sample.txt")
    with open(text_file, 'w', encoding='utf-8') as f:
        f.write("""
This is a sample text file for testing OmniToken file input capabilities.

The file contains multiple paragraphs with various types of content:
- Regular English text
- Unicode characters: café, naïve, résumé
- Emojis: 🚀 🌟 💡 🎯
- Technical terms: API, JSON, HTTP, regex
- Numbers and dates: 2023-11-05, 3.14159

This content will be used to train the tokenizer and demonstrate
how OmniToken can handle file-based input efficiently.
        """.strip())
    
    # Sample JSON file
    json_file = os.path.join(temp_dir, "sample.json")
    json_data = {
        "documents": [
            {
                "id": 1,
                "title": "Introduction to Tokenization",
                "content": "Tokenization is the process of breaking down text into smaller units called tokens.",
                "tags": ["NLP", "tokenization", "preprocessing"]
            },
            {
                "id": 2,
                "title": "Advanced Techniques",
                "content": "Modern tokenizers use subword algorithms like BPE, WordPiece, and SentencePiece.",
                "tags": ["BPE", "WordPiece", "SentencePiece"]
            }
        ],
        "metadata": {
            "version": "1.0",
            "created_by": "OmniToken Example",
            "description": "Sample JSON data for tokenizer training"
        }
    }
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    # Sample code file
    code_file = os.path.join(temp_dir, "sample.py")
    with open(code_file, 'w', encoding='utf-8') as f:
        f.write("""
def tokenize_text(text, method="bpe"):
    \"\"\"
    Tokenize input text using specified method.
    
    Args:
        text (str): Input text to tokenize
        method (str): Tokenization method
    
    Returns:
        list: List of tokens
    \"\"\"
    tokenizer = OmniToken(method=method)
    tokens = tokenizer.encode(text)
    return tokens

# Example usage
if __name__ == "__main__":
    sample_text = "Hello, world! 👋"
    result = tokenize_text(sample_text)
    print(f"Tokens: {result}")
        """.strip())
    
    return temp_dir, text_file, json_file, code_file


def main():
    """Main function demonstrating JSON and file input capabilities."""
    
    print("=" * 80)
    print("MyTecZ OmniToken - JSON and File Input Example")
    print("=" * 80)
    
    # Create sample files
    print("Creating sample files...")
    temp_dir, text_file, json_file, code_file = create_sample_files()
    print(f"Sample files created in: {temp_dir}")
    
    # Test 1: Single file input
    print(f"\n{'=' * 60}")
    print("TEST 1: Single File Input")
    print(f"{'=' * 60}")
    
    try:
        tokenizer = OmniToken(method="bpe", vocab_size=1000)
        print(f"Training with single text file: {os.path.basename(text_file)}")
        tokenizer.fit(text_file)
        
        test_text = "This is a test with file-trained tokenizer."
        tokens = tokenizer._tokenizer.tokenize(test_text)
        token_ids = tokenizer.encode(test_text)
        
        print(f"Test text: {test_text}")
        print(f"Tokens: {tokens}")
        print(f"Token IDs: {token_ids}")
        print(f"Vocabulary size: {tokenizer._tokenizer.get_vocab_size()}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Multiple file input
    print(f"\n{'=' * 60}")
    print("TEST 2: Multiple File Input")
    print(f"{'=' * 60}")
    
    try:
        tokenizer = OmniToken(method="wordpiece", vocab_size=1000)
        file_list = [text_file, json_file, code_file]
        print(f"Training with multiple files: {[os.path.basename(f) for f in file_list]}")
        tokenizer.fit(file_list)
        
        test_text = "def process_json_data():"
        tokens = tokenizer._tokenizer.tokenize(test_text)
        
        print(f"Test text: {test_text}")
        print(f"Tokens: {tokens}")
        print(f"Vocabulary size: {tokenizer._tokenizer.get_vocab_size()}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: JSON object input
    print(f"\n{'=' * 60}")
    print("TEST 3: JSON Object Input")
    print(f"{'=' * 60}")
    
    try:
        complex_json = {
            "articles": [
                {
                    "title": "Machine Learning Basics",
                    "content": "Machine learning is a subset of artificial intelligence that focuses on algorithms.",
                    "author": "AI Researcher",
                    "date": "2023-11-05"
                },
                {
                    "title": "Deep Learning Advances",
                    "content": "Deep learning has revolutionized many fields including computer vision and NLP.",
                    "author": "ML Engineer",
                    "date": "2023-11-06"
                }
            ],
            "tags": ["AI", "ML", "DL", "algorithms", "neural networks"],
            "summary": "A collection of articles about modern AI techniques and applications."
        }
        
        tokenizer = OmniToken(method="hybrid", vocab_size=1500)
        print("Training with complex JSON object...")
        tokenizer.fit(complex_json)
        
        test_text = "Neural networks and deep learning algorithms."
        tokens = tokenizer._tokenizer.tokenize(test_text)
        
        print(f"Test text: {test_text}")
        print(f"Tokens: {tokens}")
        print(f"Vocabulary size: {tokenizer._tokenizer.get_vocab_size()}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Mixed input formats
    print(f"\n{'=' * 60}")
    print("TEST 4: Mixed Input Formats")
    print(f"{'=' * 60}")
    
    try:
        mixed_data = [
            "Direct string input for training.",
            text_file,  # File path
            {
                "mixed_json": "JSON object within list",
                "data": ["item1", "item2", "item3"]
            },
            "Another direct string with emojis 🎨 and Unicode résumé."
        ]
        
        tokenizer = OmniToken(method="sentencepiece", vocab_size=1200)
        print("Training with mixed input formats...")
        tokenizer.fit(mixed_data)
        
        test_texts = [
            "Regular English text.",
            "Code-like_text with_underscores.",
            "Mixed content: résumé with 🎯 emojis!",
            "JSON-style: {\"key\": \"value\"}"
        ]
        
        for test_text in test_texts:
            tokens = tokenizer._tokenizer.tokenize(test_text)
            token_ids = tokenizer.encode(test_text)
            decoded = tokenizer.decode(token_ids)
            
            print(f"\nTest: {test_text}")
            print(f"Tokens: {tokens}")
            print(f"Decoded: {decoded}")
            print(f"Round-trip: {'✅' if test_text == decoded else '❌'}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 5: Real JSON file processing
    print(f"\n{'=' * 60}")
    print("TEST 5: JSON File Processing")
    print(f"{'=' * 60}")
    
    try:
        tokenizer = OmniToken(method="bpe", vocab_size=800)
        print(f"Training with JSON file: {os.path.basename(json_file)}")
        tokenizer.fit(json_file)
        
        # Show what was extracted from the JSON file
        with open(json_file, 'r', encoding='utf-8') as f:
            original_json = json.load(f)
        
        print("Original JSON structure:")
        print(json.dumps(original_json, indent=2)[:300] + "...")
        
        test_text = "Introduction to advanced tokenization techniques"
        tokens = tokenizer._tokenizer.tokenize(test_text)
        
        print(f"\nTest text: {test_text}")
        print(f"Tokens: {tokens}")
        
        # Test encoding/decoding
        encoded = tokenizer.encode(test_text)
        decoded = tokenizer.decode(encoded)
        print(f"Encoded: {encoded}")
        print(f"Decoded: {decoded}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 6: Tokenization comparison across input types
    print(f"\n{'=' * 60}")
    print("TEST 6: Tokenization Comparison")
    print(f"{'=' * 60}")
    
    try:
        test_sentence = "AI and machine learning algorithms 🤖"
        
        # Train tokenizers with different input types
        inputs = {
            "string_input": "AI machine learning algorithms artificial intelligence",
            "file_input": text_file,
            "json_input": complex_json
        }
        
        tokenizations = {}
        
        for input_name, input_data in inputs.items():
            try:
                tokenizer = OmniToken(method="bpe", vocab_size=500)
                tokenizer.fit(input_data)
                tokens = tokenizer._tokenizer.tokenize(test_sentence)
                tokenizations[input_name] = tokens
            except Exception as e:
                print(f"Error with {input_name}: {e}")
        
        # Compare results
        if tokenizations:
            comparison = TokenVisualizer.compare_tokenizations(test_sentence, tokenizations)
            print(comparison)
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Cleanup
    print(f"\n{'=' * 60}")
    print("CLEANUP")
    print(f"{'=' * 60}")
    
    try:
        import shutil
        shutil.rmtree(temp_dir)
        print(f"✅ Cleaned up temporary directory: {temp_dir}")
    except Exception as e:
        print(f"⚠️  Could not clean up temporary directory: {e}")
    
    print(f"\n{'=' * 80}")
    print("JSON and File Input Example completed! 🎉")
    print(f"{'=' * 80}")


if __name__ == "__main__":
    main()