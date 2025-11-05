#!/usr/bin/env python3
"""Debug script to diagnose WordPiece encoding issues."""

import json
from pathlib import Path
from omnitoken import OmniToken

DATA_DIR = Path("data/test_samples")
TRAIN_DIR = Path("data/training_corpus")

def debug_wordpiece_encoding():
    print("=== DEBUGGING WORDPIECE ===")
    
    # Load test cases
    fp = DATA_DIR / "roundtrip_expected.json"
    with open(fp, "r", encoding="utf-8") as f:
        cases = json.load(f)
    
    # Create tokenizer
    tokenizer = OmniToken(method="wordpiece", vocab_size=800)
    
    # Training sources
    training_sources = [
        str(TRAIN_DIR / "english.txt"),
        str(TRAIN_DIR / "multilingual.txt"),
        str(TRAIN_DIR / "emojis.txt"),
        str(TRAIN_DIR / "code_snippets.txt"),
        str(TRAIN_DIR / "json_samples.json"),
    ]
    
    print(f"Training on: {training_sources}")
    tokenizer.fit(training_sources)
    
    print(f"Vocab size after training: {tokenizer._tokenizer.get_vocab_size()}")
    print(f"Sample vocab entries:")
    vocab = tokenizer._tokenizer.get_vocab()
    for i, (token, token_id) in enumerate(list(vocab.items())[:20]):
        print(f"  {token_id}: {repr(token)}")
    
    # Test just the first case in detail
    text = cases[0]["text"]  # "Hello world!"
    print(f"\nDetailed encoding of: {repr(text)}")
    
    # Step by step
    basic_tokens = tokenizer._tokenizer._basic_tokenize(text)
    print(f"Basic tokens: {basic_tokens}")
    
    wordpiece_tokens = []
    for token in basic_tokens:
        wp_tokens = tokenizer._tokenizer._wordpiece_tokenize(token)
        wordpiece_tokens.extend(wp_tokens)
        print(f"  '{token}' -> {wp_tokens}")
    
    print(f"Final wordpiece tokens: {wordpiece_tokens}")
    
    # Check token to ID mapping
    token_ids = []
    for token in wordpiece_tokens:
        token_id = tokenizer._tokenizer.token_to_id.get(token, tokenizer._tokenizer.token_to_id.get(tokenizer._tokenizer.config.unk_token, 0))
        token_ids.append(token_id)
        print(f"  '{token}' -> ID {token_id}")
    
    print(f"Final IDs: {token_ids}")
    
    # Test decode
    decoded = tokenizer.decode(token_ids)
    print(f"Decoded: {repr(decoded)}")

if __name__ == "__main__":
    debug_wordpiece_encoding()