#!/usr/bin/env python3
"""Debug script to diagnose roundtrip issues."""

import json
from pathlib import Path
from omnitoken import OmniToken

DATA_DIR = Path("data/test_samples")
TRAIN_DIR = Path("data/training_corpus")

def debug_roundtrip(method):
    print(f"\n=== Testing {method.upper()} ===")
    
    # Load test cases
    fp = DATA_DIR / "roundtrip_expected.json"
    with open(fp, "r", encoding="utf-8") as f:
        cases = json.load(f)
    
    # Create tokenizer
    tokenizer = OmniToken(method=method, vocab_size=800)
    
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
    
    # Test roundtrips
    successes = 0
    for i, case in enumerate(cases):
        text = case["text"]
        try:
            ids = tokenizer.encode(text)
            decoded = tokenizer.decode(ids)
            success = text == decoded
            if success:
                successes += 1
            print(f"Case {i+1}: {'✓' if success else '✗'}")
            print(f"  Original: {repr(text)}")
            print(f"  Encoded:  {ids}")
            print(f"  Decoded:  {repr(decoded)}")
            if not success:
                print(f"  Length diff: {len(text)} -> {len(decoded)}")
        except Exception as e:
            print(f"Case {i+1}: ERROR - {e}")
    
    print(f"\nTotal successes: {successes}/{len(cases)}")
    return successes

if __name__ == "__main__":
    for method in ["wordpiece", "hybrid"]:
        debug_roundtrip(method)