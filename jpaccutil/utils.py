"""
Utility functions for jpaccutil package.

This module contains helper functions and utilities for Japanese accent processing.
"""

import re
from typing import List, Dict, Any, Optional, Tuple
import unicodedata
try:
    import jamorasep
except ImportError:
    jamorasep = None


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
    Count the number of mora in Japanese text using jamorasep.
    
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
    if jamorasep is not None:
        # Use jamorasep for accurate mora counting
        morae = jamorasep.split_morae(text)
        return len(morae)
    else:
        # Fallback to manual counting
        # Remove accent marks first
        clean_text = re.sub(r'[\[\]\|]', '', text)
        
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
    Split Japanese text into individual mora using jamorasep.
    
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
    if jamorasep is not None:
        # Use jamorasep for accurate mora splitting
        return jamorasep.split_morae(text)
    else:
        # Fallback to manual splitting
        # Remove accent marks first
        clean_text = re.sub(r'[\[\]\|]', '', text)
        
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


def embed_accent_marks(surface_reading: str, accent_nucleus: int) -> str:
    """
    Embed accent marks into surface reading based on accent nucleus position.
    
    Args:
        surface_reading: Surface reading in hiragana/katakana
        accent_nucleus: Accent nucleus position (0-based, 0 means no accent nucleus)
        
    Returns:
        Text with embedded accent marks
        
    Examples:
        >>> embed_accent_marks("こんにちは", 0)
        "|*[****|"
        >>> embed_accent_marks("こんにちは", 1)
        "|*]****|"
        >>> embed_accent_marks("こんにちは", 2)
        "|*[*]***|"
        >>> embed_accent_marks("こんにちは", 3)
        "|*[**]**|"
    """
    if jamorasep is not None:
        # Use jamorasep for accurate mora splitting
        morae = jamorasep.split_morae(surface_reading)
    else:
        # Fallback to manual splitting
        morae = split_into_mora(surface_reading)
    
    if not morae:
        return "|" + surface_reading + "|"
    
    mora_count = len(morae)
    
    # Create accent pattern based on nucleus position
    if accent_nucleus == 0:
        # No accent nucleus: |*[****|
        result = "|" + morae[0] + "[" + "".join(morae[1:]) + "|"
    elif accent_nucleus == 1:
        # Accent on first mora: |*]****|
        result = "|" + morae[0] + "]" + "".join(morae[1:]) + "|"
    elif accent_nucleus == 2:
        # Accent on second mora: |*[*]***|
        result = "|" + morae[0] + "[" + morae[1] + "]" + "".join(morae[2:]) + "|"
    elif accent_nucleus <= mora_count:
        # Accent nucleus at specified position: |*[***]*****|
        # Pattern: first mora + [ + morae up to nucleus + ] + remaining morae
        first_mora = morae[0]
        nucleus_morae = morae[1:accent_nucleus]  # morae from 2nd to nucleus
        after_nucleus = morae[accent_nucleus:]   # morae after nucleus
        
        result = "|" + first_mora + "[" + "".join(nucleus_morae) + "]" + "".join(after_nucleus) + "|"
    else:
        # Accent nucleus beyond mora count, treat as no accent
        result = "|" + "".join(morae) + "|"
    
    return result


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
        >>> extract_accent_info("こ[んにち]は")
        ("こんにちは", [(0, 'rise'), (3, 'fall')])
    """
    clean_text = ""
    accent_positions = []
    position = 0
    
    accent_map = {
        '[': 'rise',     # Rising tone mark
        ']': 'fall',     # Falling tone mark
        '|': 'boundary'  # Accent phrase boundary
    }
    
    i = 0
    while i < len(text_with_accents):
        char = text_with_accents[i]
        
        if char in accent_map:
            # This is an accent mark, record its position
            accent_positions.append((position, accent_map[char]))
        else:
            # Regular character
            clean_text += char
            position += 1
        
        i += 1
    
    return clean_text, accent_positions
