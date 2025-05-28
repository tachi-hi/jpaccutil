#!/usr/bin/env python3
"""
Test script for the embed_accent_marks function.
"""

import sys
import os

# Add the jpaccutil package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from jpaccutil.utils import embed_accent_marks

def test_embed_accent_marks():
    """Test the embed_accent_marks function with various inputs."""
    
    test_cases = [
        # (surface_reading, accent_nucleus, expected_pattern)
        ("こんにちは", 0, "No accent nucleus"),
        ("こんにちは", 1, "Accent on first mora"),
        ("こんにちは", 2, "Accent on second mora"),
        ("こんにちは", 3, "Accent on third mora"),
        ("こんにちは", 4, "Accent on fourth mora"),
        ("こんにちは", 5, "Accent on fifth mora"),
        ("さくら", 0, "No accent nucleus"),
        ("さくら", 1, "Accent on first mora"),
        ("さくら", 2, "Accent on second mora"),
        ("さくら", 3, "Accent on third mora"),
        ("あいうえおかき", 3, "7-mora word, accent on 3rd"),
        ("あいうえおかき", 4, "7-mora word, accent on 4th"),
        ("あいうえおかき", 5, "7-mora word, accent on 5th"),
    ]
    
    print("Testing embed_accent_marks function:")
    print("=" * 50)
    
    for surface_reading, accent_nucleus, description in test_cases:
        result = embed_accent_marks(surface_reading, accent_nucleus)
        print(f"Input: '{surface_reading}', Accent nucleus: {accent_nucleus}")
        print(f"Description: {description}")
        print(f"Result: {result}")
        print("-" * 30)

if __name__ == "__main__":
    test_embed_accent_marks()
