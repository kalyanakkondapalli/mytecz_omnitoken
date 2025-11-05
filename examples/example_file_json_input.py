"""Example combining file and JSON inputs for OmniToken.

This script demonstrates training the hybrid tokenizer on a mixture of:
- Plain text file
- Multilingual file
- Emoji file
- Code snippets file
- JSON samples file
- Direct string
- Inline JSON object
"""
from pathlib import Path
import json
from omnitoken import OmniToken

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "training_corpus"

def load_sources():
    return [
        str(DATA_DIR / "english.txt"),
        str(DATA_DIR / "multilingual.txt"),
        str(DATA_DIR / "emojis.txt"),
        str(DATA_DIR / "code_snippets.txt"),
        str(DATA_DIR / "json_samples.json"),
        "Inline direct string with emojis 🚀 and multilingual مرحبا world こんにちは",  # direct string
        {"extra": {"nested": "Inline JSON object supplying additional training text."}},
    ]

def main():
    sources = load_sources()
    tokenizer = OmniToken(method="hybrid", vocab_size=1200)
    tokenizer.fit(sources)

    sample = "Hello multilingual world 👨‍💻 🚀"
    ids = tokenizer.encode(sample)
    decoded = tokenizer.decode(ids)

    print("Original:", sample)
    print("Token IDs:", ids[:40], "..." if len(ids) > 40 else "")
    print("Decoded:", decoded)
    print("Round-trip success:", sample == decoded)

    # Save vocabulary example
    vocab_path = Path("hybrid_vocab.json")
    tokenizer._tokenizer.save_vocabulary(str(vocab_path))
    print(f"Saved vocab to {vocab_path}")

if __name__ == "__main__":
    main()
