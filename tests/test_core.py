#!/usr/bin/env python3
"""
Tests for jpaccutil.core module.
"""

import unittest
from jpaccutil.utils import embed_accent_marks


class TestEmbedAccentMarks(unittest.TestCase):
    """Test cases for embed_accent_marks function."""
    
    def test_no_accent_nucleus(self):
        """Test with no accent nucleus (0)."""
        test_cases = [
            ("こんにちは", 0),
            ("さくら", 0),
        ]
        
        for surface_reading, accent_nucleus in test_cases:
            with self.subTest(surface_reading=surface_reading, accent_nucleus=accent_nucleus):
                result = embed_accent_marks(surface_reading, accent_nucleus)
                # When accent_nucleus is 0, should return pattern with brackets
                self.assertIn("[", result)
                self.assertIn("|", result)
    
    def test_accent_on_first_mora(self):
        """Test with accent on first mora."""
        test_cases = [
            ("こんにちは", 1),
            ("さくら", 1),
        ]
        
        for surface_reading, accent_nucleus in test_cases:
            with self.subTest(surface_reading=surface_reading, accent_nucleus=accent_nucleus):
                result = embed_accent_marks(surface_reading, accent_nucleus)
                # Should have ] after first character for accent on first mora
                self.assertIn("]", result)
                self.assertIn("|", result)
    
    def test_accent_on_second_mora(self):
        """Test with accent on second mora."""
        test_cases = [
            ("こんにちは", 2),
            ("さくら", 2),
        ]
        
        for surface_reading, accent_nucleus in test_cases:
            with self.subTest(surface_reading=surface_reading, accent_nucleus=accent_nucleus):
                result = embed_accent_marks(surface_reading, accent_nucleus)
                # Should have brackets for accent on second mora
                self.assertIn("[", result)
                self.assertIn("]", result)
                self.assertIn("|", result)
    
    def test_accent_on_third_mora(self):
        """Test with accent on third mora."""
        test_cases = [
            ("こんにちは", 3),
            ("さくら", 3),
            ("あいうえおかき", 3),
        ]
        
        for surface_reading, accent_nucleus in test_cases:
            with self.subTest(surface_reading=surface_reading, accent_nucleus=accent_nucleus):
                result = embed_accent_marks(surface_reading, accent_nucleus)
                # Should have brackets for accent on third mora
                self.assertIn("[", result)
                self.assertIn("]", result)
                self.assertIn("|", result)
    
    def test_accent_on_fourth_mora(self):
        """Test with accent on fourth mora."""
        test_cases = [
            ("こんにちは", 4),
            ("あいうえおかき", 4),
        ]
        
        for surface_reading, accent_nucleus in test_cases:
            with self.subTest(surface_reading=surface_reading, accent_nucleus=accent_nucleus):
                result = embed_accent_marks(surface_reading, accent_nucleus)
                # Should have brackets for accent on fourth mora
                self.assertIn("[", result)
                self.assertIn("]", result)
                self.assertIn("|", result)
    
    def test_accent_on_fifth_mora(self):
        """Test with accent on fifth mora."""
        test_cases = [
            ("こんにちは", 5),
            ("あいうえおかき", 5),
        ]
        
        for surface_reading, accent_nucleus in test_cases:
            with self.subTest(surface_reading=surface_reading, accent_nucleus=accent_nucleus):
                result = embed_accent_marks(surface_reading, accent_nucleus)
                # Should have brackets for accent on fifth mora
                self.assertIn("[", result)
                self.assertIn("]", result)
                self.assertIn("|", result)
    
    def test_long_word_accents(self):
        """Test with longer words and various accent positions."""
        surface_reading = "あいうえおかき"
        
        for accent_nucleus in range(1, 6):
            with self.subTest(accent_nucleus=accent_nucleus):
                result = embed_accent_marks(surface_reading, accent_nucleus)
                if accent_nucleus == 0:
                    self.assertIn("[", result)
                    self.assertIn("|", result)
                elif accent_nucleus == 1:
                    self.assertIn("]", result)
                    self.assertIn("|", result)
                else:
                    self.assertIn("[", result)
                    self.assertIn("]", result)
                    self.assertIn("|", result)
    
    def test_accent_nucleus_out_of_range(self):
        """Test with accent nucleus beyond word length."""
        surface_reading = "さくら"  # 3 mora
        accent_nucleus = 5  # Beyond word length
        
        result = embed_accent_marks(surface_reading, accent_nucleus)
        # Should handle gracefully - implementation dependent
        self.assertIsInstance(result, str)
    
    def test_empty_string(self):
        """Test with empty string."""
        result = embed_accent_marks("", 0)
        self.assertEqual(result, "||")
    
    def test_single_character(self):
        """Test with single character."""
        result = embed_accent_marks("あ", 1)
        self.assertIsInstance(result, str)


if __name__ == '__main__':
    unittest.main()
