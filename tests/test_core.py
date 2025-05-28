"""
Tests for jpaccutil.core module.
"""

import unittest
from decimal import Decimal

from jpaccutil.core import (
    JapaneseAccountingCalculator,
    format_japanese_currency,
    parse_japanese_date
)


class TestJapaneseAccountingCalculator(unittest.TestCase):
    """Test cases for JapaneseAccountingCalculator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.calc = JapaneseAccountingCalculator()
    
    def test_calculate_consumption_tax_default_rate(self):
        """Test consumption tax calculation with default rate."""
        result = self.calc.calculate_consumption_tax(1000)
        self.assertEqual(result, Decimal('100'))
    
    def test_calculate_consumption_tax_custom_rate(self):
        """Test consumption tax calculation with custom rate."""
        result = self.calc.calculate_consumption_tax(1000, 0.08)
        self.assertEqual(result, Decimal('80'))
    
    def test_calculate_consumption_tax_with_decimal_input(self):
        """Test consumption tax calculation with Decimal input."""
        result = self.calc.calculate_consumption_tax(Decimal('1000'), 0.10)
        self.assertEqual(result, Decimal('100'))
    
    def test_calculate_consumption_tax_with_float_input(self):
        """Test consumption tax calculation with float input."""
        result = self.calc.calculate_consumption_tax(1000.0, 0.10)
        self.assertEqual(result, Decimal('100'))
    
    def test_calculate_total_with_tax_default_rate(self):
        """Test total calculation with default tax rate."""
        result = self.calc.calculate_total_with_tax(1000)
        self.assertEqual(result, Decimal('1100'))
    
    def test_calculate_total_with_tax_custom_rate(self):
        """Test total calculation with custom tax rate."""
        result = self.calc.calculate_total_with_tax(1000, 0.08)
        self.assertEqual(result, Decimal('1080'))
    
    def test_calculate_total_with_tax_decimal_input(self):
        """Test total calculation with Decimal input."""
        result = self.calc.calculate_total_with_tax(Decimal('1000'))
        self.assertEqual(result, Decimal('1100'))


class TestFormatJapaneseCurrency(unittest.TestCase):
    """Test cases for format_japanese_currency function."""
    
    def test_format_integer(self):
        """Test formatting integer amount."""
        result = format_japanese_currency(1000)
        self.assertEqual(result, "¥1,000")
    
    def test_format_decimal(self):
        """Test formatting Decimal amount."""
        result = format_japanese_currency(Decimal('1234567'))
        self.assertEqual(result, "¥1,234,567")
    
    def test_format_float(self):
        """Test formatting float amount."""
        result = format_japanese_currency(1000.0)
        self.assertEqual(result, "¥1,000")
    
    def test_format_zero(self):
        """Test formatting zero amount."""
        result = format_japanese_currency(0)
        self.assertEqual(result, "¥0")
    
    def test_format_negative(self):
        """Test formatting negative amount."""
        result = format_japanese_currency(-1000)
        self.assertEqual(result, "¥-1,000")


class TestParseJapaneseDate(unittest.TestCase):
    """Test cases for parse_japanese_date function."""
    
    def test_parse_date_placeholder(self):
        """Test date parsing (placeholder implementation)."""
        # This is a placeholder test since the function is not fully implemented
        result = parse_japanese_date("2024-01-01")
        self.assertEqual(result, "2024-01-01")


if __name__ == '__main__':
    unittest.main()
