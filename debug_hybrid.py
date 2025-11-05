#!/usr/bin/env python3
"""Debug script to trace hybrid tokenization."""

from omnitoken import OmniToken

def debug_hybrid_tokenization():
    print("=== DEBUGGING HYBRID TOKENIZATION ===")
    
    # Create and train tokenizer
    tokenizer = OmniToken(method='hybrid', vocab_size=1500, min_frequency=1)
    texts = ['Hello world', 'Bonjour monde', 'Hola mundo', '你好世界', 'こんにちは世界']
    tokenizer.fit(texts)
    
    # Test tokenization
    text = 'Hello world'
    print(f"\nTokenizing: {repr(text)}")
    
    # Get the underlying tokenizer for debugging
    hybrid_tokenizer = tokenizer._tokenizer
    
    # Analyze text characteristics
    text_stats = hybrid_tokenizer._analyze_text_characteristics(text)
    print(f"Text stats: {text_stats}")
    
    # Choose strategy
    strategy = hybrid_tokenizer._choose_optimal_strategy(text_stats)
    print(f"Chosen strategy: {strategy}")
    
    # Apply strategy
    tokens = hybrid_tokenizer._apply_strategy(text, strategy, text_stats)
    print(f"Tokens from strategy: {tokens}")
    
    # Full encode
    ids = tokenizer.encode(text)
    print(f"Final IDs: {ids}")
    
    # Convert IDs to tokens for verification
    token_names = [hybrid_tokenizer.id_to_token.get(id_, '[UNK]') for id_ in ids]
    print(f"Token names: {token_names}")
    
    # Decode
    decoded = tokenizer.decode(ids)
    print(f"Decoded: {repr(decoded)}")

if __name__ == "__main__":
    debug_hybrid_tokenization()