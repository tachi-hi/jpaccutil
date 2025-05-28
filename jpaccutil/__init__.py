"""
jpaccutil - A utility package for Japanese accent processing.

This package provides utilities for Japanese accent processing,
including implementation of Niosaka rules and automatic accent mark insertion.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# Import main functions/classes here for easy access
from .core import (
    JapaneseAccentProcessor,
    parse_accent_notation,
    format_accent_notation,
    validate_japanese_text
)
from .utils import (
    normalize_japanese_text,
    convert_katakana_to_hiragana,
    convert_hiragana_to_katakana,
    count_mora,
    split_into_mora,
    embed_accent_marks,
    is_long_vowel,
    get_vowel_sound,
    extract_accent_info
)

__all__ = [
    # Core functionality
    "JapaneseAccentProcessor",
    "parse_accent_notation",
    "format_accent_notation",
    "validate_japanese_text",
    # Utility functions
    "normalize_japanese_text",
    "convert_katakana_to_hiragana",
    "convert_hiragana_to_katakana",
    "count_mora",
    "split_into_mora",
    "embed_accent_marks",
    "is_long_vowel",
    "get_vowel_sound",
    "extract_accent_info",
]
