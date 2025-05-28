"""
Utility functions for jpaccutil package.

This module contains helper functions and utilities for Japanese accent processing.
"""

import re
from typing import List, Dict, Any, Optional, Tuple
import unicodedata


def normalize_japanese_text(text: str) -> str:
    """
    Normalize Japanese text for consistent processing.
    
    Args:
        text: Japanese text to normalize
        
    Returns:
        Normalized text
        
    Example:
        >>> normalize_japanese_text("こんにちは")
        "こんにちは"
    """
    # Normalize Unicode (NFC form)
    normalized = unicodedata.normalize('NFC', text)
    
    # Remove extra whitespace
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    
    return normalized


def convert_katakana_to_hiragana(text: str) -> str:
    """
    Convert katakana characters to hiragana.
    
    Args:
        text: Text containing katakana characters
        
    Returns:
        Text with katakana converted to hiragana
        
    Example:
        >>> convert_katakana_to_hiragana("コンニチハ")
        "こんにちは"
    """
    result = []
    for char in text:
        # Convert katakana to hiragana (Unicode range conversion)
        if '\u30A1' <= char <= '\u30F6':  # Katakana range
            hiragana_char = chr(ord(char) - 0x60)  # Convert to hiragana
            result.append(hiragana_char)
        else:
            result.append(char)
    
    return ''.join(result)


def convert_hiragana_to_katakana(text: str) -> str:
    """
    Convert hiragana characters to katakana.
    
    Args:
        text: Text containing hiragana characters
        
    Returns:
        Text with hiragana converted to katakana
        
    Example:
        >>> convert_hiragana_to_katakana("こんにちは")
        "コンニチハ"
    """
    result = []
    for char in text:
        # Convert hiragana to katakana (Unicode range conversion)
        if '\u3041' <= char <= '\u3096':  # Hiragana range
            katakana_char = chr(ord(char) + 0x60)  # Convert to katakana
            result.append(katakana_char)
        else:
            result.append(char)
    
    return ''.join(result)


def count_mora(text: str) -> int:
    """
    Count the number of mora in Japanese text.
    
    Args:
        text: Japanese text
        
    Returns:
        Number of mora
        
    Example:
        >>> count_mora("こんにちは")
        5
        >>> count_mora("きょう")  # きょ + う = 2 mora
        2
    """
    # Remove accent marks first
    clean_text = re.sub(r'[́̀̂̌]', '', text)
    
    mora_count = 0
    i = 0
    
    while i < len(clean_text):
        char = clean_text[i]
        
        # Check if current character is a Japanese character
        if re.match(r'[\u3040-\u309F\u30A0-\u30FF]', char):
            # Check for small characters (っ, ゃ, ゅ, ょ, etc.)
            if char in 'っッゃゅょャュョぁぃぅぇぉァィゥェォ':
                # Small characters don't count as separate mora
                # but combine with the previous character
                pass
            else:
                mora_count += 1
                
                # Check if next character is a small character
                if i + 1 < len(clean_text):
                    next_char = clean_text[i + 1]
                    if next_char in 'ゃゅょャュョ':
                        # Skip the small character as it's part of this mora
                        i += 1
        
        i += 1
    
    return mora_count


def split_into_mora(text: str) -> List[str]:
    """
    Split Japanese text into individual mora.
    
    Args:
        text: Japanese text
        
    Returns:
        List of mora
        
    Example:
        >>> split_into_mora("こんにちは")
        ["こ", "ん", "に", "ち", "は"]
        >>> split_into_mora("きょう")
        ["きょ", "う"]
    """
    # Remove accent marks first
    clean_text = re.sub(r'[́̀̂̌]', '', text)
    
    mora_list = []
    i = 0
    
    while i < len(clean_text):
        char = clean_text[i]
        
        if re.match(r'[\u3040-\u309F\u30A0-\u30FF]', char):
            current_mora = char
            
            # Check if next character is a small character
            if i + 1 < len(clean_text):
                next_char = clean_text[i + 1]
                if next_char in 'ゃゅょャュョ':
                    current_mora += next_char
                    i += 1
            
            mora_list.append(current_mora)
        else:
            # Non-Japanese character, add as is
            mora_list.append(char)
        
        i += 1
    
    return mora_list


def is_long_vowel(mora1: str, mora2: str) -> bool:
    """
    Check if two consecutive mora form a long vowel.
    
    Args:
        mora1: First mora
        mora2: Second mora
        
    Returns:
        True if they form a long vowel, False otherwise
        
    Example:
        >>> is_long_vowel("こ", "う")
        True
        >>> is_long_vowel("こ", "ん")
        False
    """
    # Define vowel mappings for long vowels
    long_vowel_patterns = {
        'あ': ['あ', 'ー'],
        'い': ['い', 'ー'],
        'う': ['う', 'ー'],
        'え': ['え', 'い', 'ー'],
        'お': ['お', 'う', 'ー'],
        'か': ['あ', 'ー'], 'き': ['い', 'ー'], 'く': ['う', 'ー'], 
        'け': ['え', 'い', 'ー'], 'こ': ['お', 'う', 'ー'],
        # Add more patterns as needed
    }
    
    if len(mora1) == 0 or len(mora2) == 0:
        return False
    
    # Get the vowel sound of the first mora
    first_vowel = get_vowel_sound(mora1)
    
    if first_vowel in long_vowel_patterns:
        return mora2 in long_vowel_patterns[first_vowel]
    
    return False


def get_vowel_sound(mora: str) -> str:
    """
    Get the vowel sound of a mora.
    
    Args:
        mora: Japanese mora
        
    Returns:
        Vowel sound (あ, い, う, え, お)
        
    Example:
        >>> get_vowel_sound("か")
        "あ"
        >>> get_vowel_sound("きょ")
        "お"
    """
    # Vowel mapping for hiragana
    vowel_map = {
        'あ': 'あ', 'い': 'い', 'う': 'う', 'え': 'え', 'お': 'お',
        'か': 'あ', 'き': 'い', 'く': 'う', 'け': 'え', 'こ': 'お',
        'が': 'あ', 'ぎ': 'い', 'ぐ': 'う', 'げ': 'え', 'ご': 'お',
        'さ': 'あ', 'し': 'い', 'す': 'う', 'せ': 'え', 'そ': 'お',
        'ざ': 'あ', 'じ': 'い', 'ず': 'う', 'ぜ': 'え', 'ぞ': 'お',
        'た': 'あ', 'ち': 'い', 'つ': 'う', 'て': 'え', 'と': 'お',
        'だ': 'あ', 'ぢ': 'い', 'づ': 'う', 'で': 'え', 'ど': 'お',
        'な': 'あ', 'に': 'い', 'ぬ': 'う', 'ね': 'え', 'の': 'お',
        'は': 'あ', 'ひ': 'い', 'ふ': 'う', 'へ': 'え', 'ほ': 'お',
        'ば': 'あ', 'び': 'い', 'ぶ': 'う', 'べ': 'え', 'ぼ': 'お',
        'ぱ': 'あ', 'ぴ': 'い', 'ぷ': 'う', 'ぺ': 'え', 'ぽ': 'お',
        'ま': 'あ', 'み': 'い', 'む': 'う', 'め': 'え', 'も': 'お',
        'や': 'あ', 'ゆ': 'う', 'よ': 'お',
        'ら': 'あ', 'り': 'い', 'る': 'う', 'れ': 'え', 'ろ': 'お',
        'わ': 'あ', 'ゐ': 'い', 'ゑ': 'え', 'を': 'お', 'ん': 'ん',
        # Special combinations
        'きゃ': 'あ', 'きゅ': 'う', 'きょ': 'お',
        'しゃ': 'あ', 'しゅ': 'う', 'しょ': 'お',
        'ちゃ': 'あ', 'ちゅ': 'う', 'ちょ': 'お',
        'にゃ': 'あ', 'にゅ': 'う', 'にょ': 'お',
        'ひゃ': 'あ', 'ひゅ': 'う', 'ひょ': 'お',
        'みゃ': 'あ', 'みゅ': 'う', 'みょ': 'お',
        'りゃ': 'あ', 'りゅ': 'う', 'りょ': 'お',
        'ぎゃ': 'あ', 'ぎゅ': 'う', 'ぎょ': 'お',
        'じゃ': 'あ', 'じゅ': 'う', 'じょ': 'お',
        'びゃ': 'あ', 'びゅ': 'う', 'びょ': 'お',
        'ぴゃ': 'あ', 'ぴゅ': 'う', 'ぴょ': 'お',
    }
    
    # Convert katakana to hiragana for lookup
    hiragana_mora = convert_katakana_to_hiragana(mora)
    
    return vowel_map.get(hiragana_mora, 'あ')  # Default to 'あ' if not found


def extract_accent_info(text_with_accents: str) -> Tuple[str, List[Tuple[int, str]]]:
    """
    Extract accent information from text with accent marks.
    
    Args:
        text_with_accents: Text containing accent marks
        
    Returns:
        Tuple of (clean_text, accent_positions)
        
    Example:
        >>> extract_accent_info("こ́んにち̀は")
        ("こんにちは", [(0, 'high'), (3, 'low')])
    """
    clean_text = ""
    accent_positions = []
    position = 0
    
    accent_map = {
        '́': 'high',   # Combining acute accent
        '̀': 'low',    # Combining grave accent
        '̂': 'fall',   # Combining circumflex
        '̌': 'rise'    # Combining caron
    }
    
    i = 0
    while i < len(text_with_accents):
        char = text_with_accents[i]
        
        if char in accent_map:
            # This is an accent mark, record its position
            if position > 0:  # Accent applies to previous character
                accent_positions.append((position - 1, accent_map[char]))
        else:
            # Regular character
            clean_text += char
            position += 1
        
        i += 1
    
    return clean_text, accent_positions


def validate_accent_pattern(pattern: str) -> bool:
    """
    Validate accent pattern notation.
    
    Args:
        pattern: Accent pattern string (e.g., "1H,3L")
        
    Returns:
        True if pattern is valid, False otherwise
        
    Example:
        >>> validate_accent_pattern("1H,3L")
        True
        >>> validate_accent_pattern("invalid")
        False
    """
    if not pattern:
        return True  # Empty pattern is valid
    
    # Pattern should be like "1H,3L,5F"
    pattern_regex = r'^(\d+[HLFR])(,\d+[HLFR])*$'
    return bool(re.match(pattern_regex, pattern.upper()))
