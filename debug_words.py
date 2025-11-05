#!/usr/bin/env python3
"""Debug script to see what words are being extracted."""

from pathlib import Path
from omnitoken.trainer import FrequencyAnalyzer

TRAIN_DIR = Path("data/training_corpus")

def debug_word_extraction():
    print("=== DEBUGGING WORD EXTRACTION ===")
    
    # Training sources
    training_sources = [
        str(TRAIN_DIR / "english.txt"),
        str(TRAIN_DIR / "multilingual.txt"),
        str(TRAIN_DIR / "emojis.txt"),
        str(TRAIN_DIR / "code_snippets.txt"),
        str(TRAIN_DIR / "json_samples.json"),
    ]
    
    # Process each file
    all_texts = []
    for source in training_sources:
        try:
            with open(source, 'r', encoding='utf-8') as f:
                content = f.read()
                all_texts.append(content)
                print(f"Loaded {source}: {len(content)} chars")
        except Exception as e:
            print(f"Error loading {source}: {e}")
    
    # Analyze word frequencies
    word_freq = FrequencyAnalyzer.analyze_word_frequency(all_texts)
    
    print(f"\nTop 20 words by frequency:")
    for word, freq in word_freq.most_common(20):
        print(f"  {repr(word)}: {freq}")
    
    # Check for specific words
    target_words = ["Hello", "hello", "world", "World"]
    print(f"\nChecking for target words:")
    for word in target_words:
        freq = word_freq.get(word, 0)
        print(f"  {repr(word)}: {freq}")

if __name__ == "__main__":
    debug_word_extraction()