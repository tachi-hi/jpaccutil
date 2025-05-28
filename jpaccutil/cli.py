"""
Command-line interface for jpaccutil package.

This module provides CLI commands for Japanese accent processing operations.
"""

import argparse
import sys
from typing import Optional

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
    extract_accent_info,
    validate_accent_pattern
)


def cmd_process_accent(args) -> None:
    """Process text with accent marks using Niosaka rules."""
    processor = JapaneseAccentProcessor()
    
    try:
        text = args.text
        
        if not validate_japanese_text(text):
            print(f"Warning: Text may not contain Japanese characters: {text}", file=sys.stderr)
        
        # Apply Niosaka rules
        result = processor.apply_niosaka_rules(text)
        
        print(f"Input: {text}")
        print(f"Output: {result}")
        
        # Show mora count
        mora_count = count_mora(text)
        print(f"Mora count: {mora_count}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_add_accents(args) -> None:
    """Add accent marks at specified positions."""
    processor = JapaneseAccentProcessor()
    
    try:
        text = args.text
        notation = args.notation
        
        if not validate_accent_pattern(notation):
            print(f"Invalid accent notation: {notation}", file=sys.stderr)
            sys.exit(1)
        
        # Parse accent notation
        positions = parse_accent_notation(notation)
        
        # Add accent marks
        result = processor.add_accent_marks(text, positions)
        
        print(f"Input: {text}")
        print(f"Notation: {notation}")
        print(f"Output: {result}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_remove_accents(args) -> None:
    """Remove accent marks from text."""
    processor = JapaneseAccentProcessor()
    
    try:
        text = args.text
        result = processor.remove_accent_marks(text)
        
        print(f"Input: {text}")
        print(f"Output: {result}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_convert_script(args) -> None:
    """Convert between hiragana and katakana."""
    try:
        text = args.text
        
        if args.to_hiragana:
            result = convert_katakana_to_hiragana(text)
            print(f"Katakana to Hiragana: {text} -> {result}")
        elif args.to_katakana:
            result = convert_hiragana_to_katakana(text)
            print(f"Hiragana to Katakana: {text} -> {result}")
        else:
            print("Please specify --to-hiragana or --to-katakana", file=sys.stderr)
            sys.exit(1)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_analyze_text(args) -> None:
    """Analyze Japanese text structure."""
    try:
        text = args.text
        
        # Normalize text
        normalized = normalize_japanese_text(text)
        
        # Count mora
        mora_count = count_mora(text)
        
        # Split into mora
        mora_list = split_into_mora(text)
        
        # Extract accent info if present
        clean_text, accent_positions = extract_accent_info(text)
        
        print(f"Original text: {text}")
        print(f"Normalized: {normalized}")
        print(f"Clean text: {clean_text}")
        print(f"Mora count: {mora_count}")
        print(f"Mora list: {mora_list}")
        
        if accent_positions:
            notation = format_accent_notation(accent_positions)
            print(f"Accent positions: {accent_positions}")
            print(f"Accent notation: {notation}")
        else:
            print("No accent marks found")
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_validate(args) -> None:
    """Validate Japanese text and accent patterns."""
    try:
        if args.text:
            is_valid = validate_japanese_text(args.text)
            print(f"Text '{args.text}' is {'valid' if is_valid else 'invalid'} Japanese text")
        
        if args.pattern:
            is_valid = validate_accent_pattern(args.pattern)
            print(f"Pattern '{args.pattern}' is {'valid' if is_valid else 'invalid'} accent notation")
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def create_parser() -> argparse.ArgumentParser:
    """Create command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Japanese accent processing utilities",
        prog="jpaccutil"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Process accent command
    process_parser = subparsers.add_parser("process", help="Apply Niosaka rules to text")
    process_parser.add_argument("text", help="Japanese text to process")
    process_parser.set_defaults(func=cmd_process_accent)
    
    # Add accents command
    add_parser = subparsers.add_parser("add", help="Add accent marks at specified positions")
    add_parser.add_argument("text", help="Japanese text")
    add_parser.add_argument("notation", help="Accent notation (e.g., '1H,3L')")
    add_parser.set_defaults(func=cmd_add_accents)
    
    # Remove accents command
    remove_parser = subparsers.add_parser("remove", help="Remove accent marks from text")
    remove_parser.add_argument("text", help="Text with accent marks")
    remove_parser.set_defaults(func=cmd_remove_accents)
    
    # Convert script command
    convert_parser = subparsers.add_parser("convert", help="Convert between hiragana and katakana")
    convert_parser.add_argument("text", help="Text to convert")
    convert_group = convert_parser.add_mutually_exclusive_group(required=True)
    convert_group.add_argument(
        "--to-hiragana", 
        action="store_true", 
        help="Convert katakana to hiragana"
    )
    convert_group.add_argument(
        "--to-katakana", 
        action="store_true", 
        help="Convert hiragana to katakana"
    )
    convert_parser.set_defaults(func=cmd_convert_script)
    
    # Analyze text command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze Japanese text structure")
    analyze_parser.add_argument("text", help="Japanese text to analyze")
    analyze_parser.set_defaults(func=cmd_analyze_text)
    
    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate text and patterns")
    validate_parser.add_argument("--text", help="Japanese text to validate")
    validate_parser.add_argument("--pattern", help="Accent pattern to validate")
    validate_parser.set_defaults(func=cmd_validate)
    
    return parser


def main() -> None:
    """Main entry point for CLI."""
    parser = create_parser()
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    
    # Call the appropriate command function
    args.func(args)


if __name__ == "__main__":
    main()
