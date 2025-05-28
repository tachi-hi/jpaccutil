"""
Tests for jpaccutil.utils module.
"""

import unittest
from decimal import Decimal

from jpaccutil.utils import (
    validate_japanese_postal_code,
    format_japanese_postal_code,
    convert_zenkaku_to_hankaku,
    convert_hankaku_to_zenkaku,
    round_to_japanese_currency,
    parse_japanese_number_string,
    get_japanese_era_year
)


class TestPostalCodeFunctions(unittest.TestCase):
    """Test cases for postal code functions."""
    
    def test_validate_japanese_postal_code_valid_with_hyphen(self):
        """Test validation of valid postal code with hyphen."""
        self.assertTrue(validate_japanese_postal_code("123-4567"))
    
    def test_validate_japanese_postal_code_valid_without_hyphen(self):
        """Test validation of valid postal code without hyphen."""
        self.assertTrue(validate_japanese_postal_code("1234567"))
    
    def test_validate_japanese_postal_code_invalid_short(self):
        """Test validation of invalid short postal code."""
        self.assertFalse(validate_japanese_postal_code("12-345"))
    
    def test_validate_japanese_postal_code_invalid_long(self):
        """Test validation of invalid long postal code."""
        self.assertFalse(validate_japanese_postal_code("1234-56789"))
    
    def test_validate_japanese_postal_code_with_spaces(self):
        """Test validation of postal code with spaces."""
        self.assertTrue(validate_japanese_postal_code("123 4567"))
    
    def test_format_japanese_postal_code_without_hyphen(self):
        """Test formatting postal code without hyphen."""
        result = format_japanese_postal_code("1234567")
        self.assertEqual(result, "123-4567")
    
    def test_format_japanese_postal_code_with_hyphen(self):
        """Test formatting postal code with hyphen."""
        result = format_japanese_postal_code("123-4567")
        self.assertEqual(result, "123-4567")
    
    def test_format_japanese_postal_code_invalid(self):
        """Test formatting invalid postal code."""
        result = format_japanese_postal_code("12345")
        self.assertIsNone(result)


class TestNumberConversionFunctions(unittest.TestCase):
    """Test cases for number conversion functions."""
    
    def test_convert_zenkaku_to_hankaku(self):
        """Test conversion from full-width to half-width numbers."""
        result = convert_zenkaku_to_hankaku("１２３４５")
        self.assertEqual(result, "12345")
    
    def test_convert_zenkaku_to_hankaku_mixed(self):
        """Test conversion with mixed characters."""
        result = convert_zenkaku_to_hankaku("価格：１，０００円")
        self.assertEqual(result, "価格：1，000円")
    
    def test_convert_hankaku_to_zenkaku(self):
        """Test conversion from half-width to full-width numbers."""
        result = convert_hankaku_to_zenkaku("12345")
        self.assertEqual(result, "１２３４５")
    
    def test_convert_hankaku_to_zenkaku_mixed(self):
        """Test conversion with mixed characters."""
        result = convert_hankaku_to_zenkaku("価格：1,000円")
        self.assertEqual(result, "価格：１，０００円")


class TestRoundingFunction(unittest.TestCase):
    """Test cases for rounding function."""
    
    def test_round_to_japanese_currency_default(self):
        """Test default rounding."""
        result = round_to_japanese_currency(Decimal("123.456"))
        self.assertEqual(result, Decimal('123'))
    
    def test_round_to_japanese_currency_floor(self):
        """Test floor rounding."""
        result = round_to_japanese_currency(Decimal("123.789"), "floor")
        self.assertEqual(result, Decimal('123'))
    
    def test_round_to_japanese_currency_ceil(self):
        """Test ceiling rounding."""
        result = round_to_japanese_currency(Decimal("123.123"), "ceil")
        self.assertEqual(result, Decimal('124'))
    
    def test_round_to_japanese_currency_round_half_up(self):
        """Test round half up."""
        result = round_to_japanese_currency(Decimal("123.5"))
        self.assertEqual(result, Decimal('124'))


class TestParseJapaneseNumberString(unittest.TestCase):
    """Test cases for parsing Japanese number strings."""
    
    def test_parse_japanese_number_string_zenkaku(self):
        """Test parsing full-width numbers."""
        result = parse_japanese_number_string("１２３４")
        self.assertEqual(result, Decimal('1234'))
    
    def test_parse_japanese_number_string_with_comma(self):
        """Test parsing numbers with comma separator."""
        result = parse_japanese_number_string("１，２３４")
        self.assertEqual(result, Decimal('1234'))
    
    def test_parse_japanese_number_string_hankaku(self):
        """Test parsing half-width numbers."""
        result = parse_japanese_number_string("1,234")
        self.assertEqual(result, Decimal('1234'))
    
    def test_parse_japanese_number_string_invalid(self):
        """Test parsing invalid number string."""
        result = parse_japanese_number_string("abc")
        self.assertIsNone(result)
    
    def test_parse_japanese_number_string_with_spaces(self):
        """Test parsing numbers with spaces."""
        result = parse_japanese_number_string("1 234")
        self.assertEqual(result, Decimal('1234'))


class TestJapaneseEraYear(unittest.TestCase):
    """Test cases for Japanese era year conversion."""
    
    def test_get_japanese_era_year_reiwa(self):
        """Test Reiwa era conversion."""
        result = get_japanese_era_year(2023)
        expected = {
            'era': '令和',
            'era_year': 5,
            'western_year': 2023
        }
        self.assertEqual(result, expected)
    
    def test_get_japanese_era_year_heisei(self):
        """Test Heisei era conversion."""
        result = get_japanese_era_year(2000)
        expected = {
            'era': '平成',
            'era_year': 12,
            'western_year': 2000
        }
        self.assertEqual(result, expected)
    
    def test_get_japanese_era_year_showa(self):
        """Test Showa era conversion."""
        result = get_japanese_era_year(1950)
        expected = {
            'era': '昭和',
            'era_year': 25,
            'western_year': 1950
        }
        self.assertEqual(result, expected)
    
    def test_get_japanese_era_year_unknown(self):
        """Test unknown era conversion."""
        result = get_japanese_era_year(1900)
        expected = {
            'era': '不明',
            'era_year': None,
            'western_year': 1900
        }
        self.assertEqual(result, expected)
    
    def test_get_japanese_era_year_reiwa_first_year(self):
        """Test Reiwa era first year."""
        result = get_japanese_era_year(2019)
        expected = {
            'era': '令和',
            'era_year': 1,
            'western_year': 2019
        }
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
