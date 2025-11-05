"""
Basic example demonstrating MyTecZ OmniToken usage.

This example shows how to use the OmniToken tokenizer with different
tokenization methods and input formats.
"""

import sys
import os

# Add the parent directory to the path so we can import omnitoken
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from omnitoken import OmniToken
from omnitoken.utils import TokenVisualizer


def main():
    """Main example function demonstrating basic usage."""
    
    print("=" * 80)
    print("MyTecZ OmniToken - Basic Usage Example")
    print("=" * 80)
    
    # Sample texts for training and testing
    training_texts = [
        "Hello world! This is a sample text for tokenization.",
        "The quick brown fox jumps over the lazy dog. 🦊",
        "Python is a versatile programming language used for AI, web development, and automation.",
        "Machine learning and natural language processing are fascinating fields! 🤖",
        "Unicode support: café, naïve, résumé, 北京, Москва, العربية",
        "Special characters: @#$%^&*()_+-=[]{}|;':\"<>?/.,",
        "Numbers and dates: 2023-11-05, 3.14159, $1,234.56",
        "Email: user@example.com, Website: https://www.example.org"
    ]
    
    test_text = "Hello world 👋! This is a test with emojis 🚀 and Unicode café."
    
    # Test different tokenization methods
    methods = ["bpe", "wordpiece", "sentencepiece", "hybrid"]
    
    for method in methods:
        print(f"\n{'=' * 60}")
        print(f"Testing {method.upper()} Tokenizer")
        print(f"{'=' * 60}")
        
        try:
            # Create tokenizer
            tokenizer = OmniToken(method=method, vocab_size=1000, min_frequency=1)
            
            # Train the tokenizer
            print("Training tokenizer...")
            tokenizer.fit(training_texts)
            print(f"✅ Training completed! Vocabulary size: {tokenizer._tokenizer.get_vocab_size()}")
            
            # Encode text
            print(f"\nTesting text: {test_text}")
            tokens = tokenizer._tokenizer.tokenize(test_text)
            token_ids = tokenizer.encode(test_text)
            
            print(f"Tokens ({len(tokens)}): {tokens[:10]}{'...' if len(tokens) > 10 else ''}")
            print(f"Token IDs ({len(token_ids)}): {token_ids[:10]}{'...' if len(token_ids) > 10 else ''}")
            
            # Decode back to text
            decoded_text = tokenizer.decode(token_ids)
            print(f"Decoded: {decoded_text}")
            
            # Verify round-trip
            round_trip_success = tokenizer._tokenizer.verify_round_trip(test_text)
            print(f"Round-trip successful: {'✅' if round_trip_success else '❌'}")
            
            # Show tokenization visualization
            visualization = TokenVisualizer.visualize_tokens(test_text, tokens, token_ids, max_width=60)
            print("\nTokenization Visualization:")
            print(visualization)
            
        except Exception as e:
            print(f"❌ Error with {method} tokenizer: {e}")
    
    # Compare tokenization methods
    print(f"\n{'=' * 80}")
    print("TOKENIZATION COMPARISON")
    print(f"{'=' * 80}")
    
    tokenizations = {}
    
    for method in methods:
        try:
            tokenizer = OmniToken(method=method, vocab_size=500, min_frequency=1)
            tokenizer.fit(training_texts)
            tokens = tokenizer._tokenizer.tokenize(test_text)
            tokenizations[method] = tokens
        except Exception as e:
            print(f"Skipping {method} due to error: {e}")
    
    if tokenizations:
        comparison = TokenVisualizer.compare_tokenizations(test_text, tokenizations)
        print(comparison)
    
    # Test with different input formats
    print(f"\n{'=' * 80}")
    print("TESTING DIFFERENT INPUT FORMATS")
    print(f"{'=' * 80}")
    
    # Test with string input
    print("\n1. String input:")
    tokenizer = OmniToken(method="bpe", vocab_size=500)
    tokenizer.fit("This is a simple string input for training.")
    result = tokenizer.encode("Test encoding")
    print(f"   Result: {result}")
    
    # Test with list input
    print("\n2. List input:")
    tokenizer = OmniToken(method="bpe", vocab_size=500)
    tokenizer.fit(["First text", "Second text", "Third text"])
    result = tokenizer.encode("Test encoding")
    print(f"   Result: {result}")
    
    # Test with JSON input
    print("\n3. JSON input:")
    tokenizer = OmniToken(method="bpe", vocab_size=500)
    json_data = {
        "texts": ["Text from JSON", "Another JSON text"],
        "metadata": "Some metadata"
    }
    tokenizer.fit(json_data)
    result = tokenizer.encode("Test encoding")
    print(f"   Result: {result}")
    
    # Performance test
    print(f"\n{'=' * 80}")
    print("PERFORMANCE TEST")
    print(f"{'=' * 80}")
    
    import time
    
    # Create a larger training set
    large_training_set = training_texts * 100  # Repeat texts for more data
    
    for method in ["bpe", "hybrid"]:
        try:
            print(f"\nTesting {method} performance...")
            
            # Time training
            start_time = time.time()
            tokenizer = OmniToken(method=method, vocab_size=2000)
            tokenizer.fit(large_training_set)
            train_time = time.time() - start_time
            
            # Time encoding
            start_time = time.time()
            for _ in range(100):
                tokenizer.encode(test_text)
            encode_time = time.time() - start_time
            
            print(f"   Training time: {train_time:.2f}s")
            print(f"   Encoding time (100 iterations): {encode_time:.4f}s")
            print(f"   Avg encoding time: {encode_time/100:.6f}s")
            
        except Exception as e:
            print(f"   Error: {e}")
    
    print(f"\n{'=' * 80}")
    print("Example completed! 🎉")
    print(f"{'=' * 80}")


if __name__ == "__main__":
    main()