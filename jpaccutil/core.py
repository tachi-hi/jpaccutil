"""
Core functionality for jpaccutil package.

This module contains the main classes and functions for Japanese accent processing,
including implementation of Niosaka rules and accent mark insertion.
"""

from typing import List, Dict, Optional, Tuple, Union
import re
try:
    import jamorasep
except ImportError:
    jamorasep = None


class JapaneseAccentProcessor:
    """
    A processor class for Japanese accent operations.
    
    This class provides methods for applying Niosaka rules and inserting
    accent marks into Japanese text.
    """
    
    def __init__(self):
        """Initialize the accent processor."""
        # Accent mark symbols
        self.accent_marks = {
            'rise': '[',    # Rising tone mark
            'fall': ']',    # Falling tone mark
            'boundary': '|' # Accent phrase boundary
        }
        
        # Initialize basic accent patterns (to be expanded with Niosaka rules)
        self.accent_patterns = {}
        
        # Check if jamorasep is available
        if jamorasep is None:
            raise ImportError("jamorasep library is required. Install it with: pip install jamorasep")
    
    def apply_niosaka_rules(
        self, 
        text: str, 
        word_info: Optional[Dict] = None
    ) -> str:
        """
        Apply Niosaka rules to add accent marks to Japanese text.
        
        Args:
            text: The Japanese text to process
            word_info: Optional dictionary containing word information
                      (part of speech, accent type, etc.)
            
        Returns:
            Text with accent marks applied
            
        Example:
            >>> processor = JapaneseAccentProcessor()
            >>> processor.apply_niosaka_rules("こんにちは")
            "こ[んにちは"
        """
        if not text:
            return text
        
        # Use jamorasep to split into morae first
        morae = self.split_into_morae(text)
        
        if not morae:
            return text
        
        # Placeholder implementation - to be replaced with actual Niosaka rules
        # This is a basic example that adds rise accent to the first mora
        accent_positions = [(0, 'rise')]
        
        return self.add_accent_to_morae(morae, accent_positions)
    
    def add_accent_marks(
        self, 
        text: str, 
        accent_positions: List[Tuple[int, str]]
    ) -> str:
        """
        Add accent marks at specified positions in the text.
        
        Args:
            text: The text to add accent marks to
            accent_positions: List of tuples (position, accent_type)
            
        Returns:
            Text with accent marks added
            
        Example:
            >>> processor = JapaneseAccentProcessor()
            >>> processor.add_accent_marks("こんにちは", [(0, 'rise'), (3, 'fall')])
            "こ[んにち]は"
        """
        if not accent_positions:
            return text
        
        # Sort positions in reverse order to avoid index shifting
        sorted_positions = sorted(accent_positions, key=lambda x: x[0], reverse=True)
        
        result = list(text)
        for position, accent_type in sorted_positions:
            if 0 <= position < len(result) and accent_type in self.accent_marks:
                # Insert accent mark after the character
                result.insert(position + 1, self.accent_marks[accent_type])
        
        return ''.join(result)
    
    def detect_accent_pattern(self, text: str) -> List[Tuple[int, str]]:
        """
        Detect accent pattern in Japanese text.
        
        Args:
            text: Japanese text to analyze
            
        Returns:
            List of detected accent positions and types
            
        Note:
            This is a placeholder implementation.
            Actual implementation will depend on specific Niosaka rules.
        """
        # Use jamorasep to split into morae first
        morae = self.split_into_morae(text)
        positions = []
        
        # Simple rule: rise accent on first mora if more than 2 morae
        if len(morae) > 2:
            positions.append((0, 'rise'))
        
        return positions
    
    def remove_accent_marks(self, text: str) -> str:
        """
        Remove all accent marks from text.
        
        Args:
            text: Text with accent marks
            
        Returns:
            Text without accent marks
            
        Example:
            >>> processor = JapaneseAccentProcessor()
            >>> processor.remove_accent_marks("こ[んにち]は")
            "こんにちは"
        """
        # Remove all accent marks
        accent_pattern = r'[\[\]\|]'
        return re.sub(accent_pattern, '', text)
    
    def split_into_morae(self, text: str) -> List[str]:
        """
        Split Japanese text into morae using jamorasep.
        
        Args:
            text: Japanese text to split
            
        Returns:
            List of morae
            
        Example:
            >>> processor = JapaneseAccentProcessor()
            >>> processor.split_into_morae("こんにちは")
            ['こ', 'ん', 'に', 'ち', 'は']
        """
        if not text:
            return []
        
        # Use jamorasep to split into morae
        morae = jamorasep.split_morae(text)
        return morae
    
    def add_accent_to_morae(
        self, 
        morae: List[str], 
        accent_positions: List[Tuple[int, str]]
    ) -> str:
        """
        Add accent marks to specific morae positions.
        
        Args:
            morae: List of morae
            accent_positions: List of (mora_index, accent_type) tuples
            
        Returns:
            Text with accent marks applied to morae
            
        Example:
            >>> processor = JapaneseAccentProcessor()
            >>> morae = ['こ', 'ん', 'に', 'ち', 'は']
            >>> processor.add_accent_to_morae(morae, [(0, 'rise'), (3, 'fall')])
            "こ[んにち]は"
        """
        if not morae or not accent_positions:
            return ''.join(morae)
        
        result = morae.copy()
        
        # Sort positions in reverse order to avoid index shifting
        sorted_positions = sorted(accent_positions, key=lambda x: x[0], reverse=True)
        
        for position, accent_type in sorted_positions:
            if 0 <= position < len(result) and accent_type in self.accent_marks:
                # Insert accent mark after the mora
                result.insert(position + 1, self.accent_marks[accent_type])
        
        return ''.join(result)


def parse_accent_notation(notation: str) -> List[Tuple[int, str]]:
    """
    Parse accent notation string into position and type information.
    
    Args:
        notation: Accent notation string (e.g., "1R,3F" for rise at 1, fall at 3)
        
    Returns:
        List of (position, accent_type) tuples
        
    Example:
        >>> parse_accent_notation("1R,3F")
        [(1, 'rise'), (3, 'fall')]
    """
    positions = []
    
    if not notation:
        return positions
    
    # Parse notation like "1R,3F,5B"
    parts = notation.split(',')
    accent_map = {'R': 'rise', 'F': 'fall', 'B': 'boundary'}
    
    for part in parts:
        part = part.strip()
        if len(part) >= 2:
            try:
                position = int(part[:-1])
                accent_char = part[-1].upper()
                if accent_char in accent_map:
                    positions.append((position, accent_map[accent_char]))
            except ValueError:
                continue
    
    return positions


def format_accent_notation(positions: List[Tuple[int, str]]) -> str:
    """
    Format accent positions into notation string.
    
    Args:
        positions: List of (position, accent_type) tuples
        
    Returns:
        Formatted notation string
        
    Example:
        >>> format_accent_notation([(1, 'rise'), (3, 'fall')])
        "1R,3F"
    """
    if not positions:
        return ""
    
    accent_map = {'rise': 'R', 'fall': 'F', 'boundary': 'B'}
    
    notation_parts = []
    for position, accent_type in sorted(positions):
        if accent_type in accent_map:
            notation_parts.append(f"{position}{accent_map[accent_type]}")
    
    return ','.join(notation_parts)


def validate_japanese_text(text: str) -> bool:
    """
    Validate if text contains Japanese characters.
    
    Args:
        text: Text to validate
        
    Returns:
        True if text contains Japanese characters, False otherwise
        
    Example:
        >>> validate_japanese_text("こんにちは")
        True
        >>> validate_japanese_text("hello")
        False
    """
    # Check for hiragana, katakana, or kanji characters
    japanese_pattern = r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]'
    return bool(re.search(japanese_pattern, text))
