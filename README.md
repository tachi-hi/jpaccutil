# jpaccutil - Japanese Accent Processing Utility

A Python package for Japanese accent processing that implements Sagisaka rules (匂坂規則) for automatic accent mark insertion in Japanese text.

## Description

jpaccutil provides utilities for Japanese accent processing, including automatic accent mark insertion based on Sagisaka rules. The package uses the jamorasep library for accurate mora splitting and supports various Japanese text formats including hiragana, katakana, and kanji readings.

## Features

- **Sagisaka Rules Implementation**: Automatic accent mark insertion using Sagisaka rules
- **Mora-based Processing**: Accurate mora splitting using jamorasep library
- **Accent Mark Notation**: Standardized accent notation with '[' for rising tone, ']' for falling tone, and '|' for accent phrase boundaries
- **Text Normalization**: Support for hiragana/katakana conversion and text normalization
- **Command-line Interface**: CLI for batch processing of Japanese text
- **Comprehensive API**: Both high-level and low-level interfaces for flexible usage

## Installation

### Requirements

- Python 3.7+
- jamorasep library (for mora splitting)

### From PyPI (when published)

```bash
pip install jpaccutil
```

### From source

```bash
git clone https://github.com/yourusername/jpaccutil.git
cd jpaccutil
pip install -e .
```

### Development Installation

```bash
git clone https://github.com/yourusername/jpaccutil.git
cd jpaccutil
pip install -e ".[dev]"
```

## Usage

### Basic Accent Mark Embedding

```python
import jpaccutil

# Embed accent marks based on accent nucleus position
# Accent nucleus patterns:
# 0: |x[xxxxxxxx|  (no accent nucleus)
# 1: |x]xxxxxxxx|  (accent on first mora)
# 2: |x[x]xxxxxx|  (accent on second mora)
# n: |x[xxx...]x|  (accent on nth mora)

result = jpaccutil.embed_accent_marks("こんにちは", 0)
print(result)  # |こ[んにちは|

result = jpaccutil.embed_accent_marks("こんにちは", 1)
print(result)  # |こ]んにちは|

result = jpaccutil.embed_accent_marks("こんにちは", 2)
print(result)  # |こ[ん]にちは|

result = jpaccutil.embed_accent_marks("こんにちは", 3)
print(result)  # |こ[んに]ちは|
```

### Using the JapaneseAccentProcessor Class

```python
from jpaccutil import JapaneseAccentProcessor

# Initialize the processor
processor = JapaneseAccentProcessor()

# Apply Sagisaka rules (placeholder implementation)
result = processor.apply_niosaka_rules("こんにちは")
print(result)

# Add accent marks at specific positions
text = "こんにちは"
accent_positions = [(0, 'rise'), (3, 'fall')]
result = processor.add_accent_marks(text, accent_positions)
print(result)  # こ[んにち]は

# Remove accent marks
clean_text = processor.remove_accent_marks("こ[んにち]は")
print(clean_text)  # こんにちは
```

### Mora Processing

```python
import jpaccutil

# Split text into morae
morae = jpaccutil.split_into_mora("こんにちは")
print(morae)  # ['こ', 'ん', 'に', 'ち', 'は']

# Count morae
count = jpaccutil.count_mora("こんにちは")
print(count)  # 5

# Handle complex morae (with small characters)
morae = jpaccutil.split_into_mora("きょう")
print(morae)  # ['きょ', 'う']
```

### Text Conversion and Normalization

```python
import jpaccutil

# Convert between hiragana and katakana
hiragana = jpaccutil.convert_katakana_to_hiragana("コンニチハ")
print(hiragana)  # こんにちは

katakana = jpaccutil.convert_hiragana_to_katakana("こんにちは")
print(katakana)  # コンニチハ

# Normalize Japanese text
normalized = jpaccutil.normalize_japanese_text("こんにちは　　世界")
print(normalized)  # こんにちは 世界

# Validate Japanese text
is_japanese = jpaccutil.validate_japanese_text("こんにちは")
print(is_japanese)  # True
```

### Accent Information Extraction

```python
import jpaccutil

# Extract accent information from marked text
clean_text, positions = jpaccutil.extract_accent_info("こ[んにち]は")
print(clean_text)  # こんにちは
print(positions)   # [(0, 'rise'), (3, 'fall')]

# Parse and format accent notation
positions = jpaccutil.parse_accent_notation("1R,3F")
print(positions)  # [(1, 'rise'), (3, 'fall')]

notation = jpaccutil.format_accent_notation([(1, 'rise'), (3, 'fall')])
print(notation)   # 1R,3F
```

## Accent Mark Conventions

The package uses standardized accent notation:

- `[` - Rising tone (rise)
- `]` - Falling tone (fall)  
- `|` - Accent phrase boundary

## Command Line Interface

```bash
# Process a single text (when CLI is implemented)
jpaccutil "こんにちは"

# Process files in batch
jpaccutil --input input.txt --output output.txt

# Specify accent nucleus position
jpaccutil "こんにちは" --accent-nucleus 2
```

## API Reference

### Core Classes

- `JapaneseAccentProcessor`: Main processor class for accent operations
- `apply_niosaka_rules()`: Apply Sagisaka rules to text
- `add_accent_marks()`: Add accent marks at specified positions
- `remove_accent_marks()`: Remove all accent marks from text

### Utility Functions

- `split_into_mora()`: Split Japanese text into morae
- `count_mora()`: Count number of morae in text
- `embed_accent_marks()`: Embed accent marks based on nucleus position
- `normalize_japanese_text()`: Normalize Japanese text
- `convert_katakana_to_hiragana()`: Convert katakana to hiragana
- `convert_hiragana_to_katakana()`: Convert hiragana to katakana
- `validate_japanese_text()`: Validate if text contains Japanese characters
- `extract_accent_info()`: Extract accent information from marked text
- `parse_accent_notation()`: Parse accent notation string
- `format_accent_notation()`: Format accent positions to notation string

## Development

### Setting up Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/jpaccutil.git
cd jpaccutil

# Install in development mode with dev dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=jpaccutil

# Run specific test file
pytest tests/test_core.py
```

### Code Quality

```bash
# Format code
black jpaccutil/

# Lint code
flake8 jpaccutil/

# Type checking
mypy jpaccutil/
```

### Project Structure

```
jpaccutil/
├── jpaccutil/
│   ├── __init__.py      # Package initialization and exports
│   ├── core.py          # Core JapaneseAccentProcessor class
│   ├── utils.py         # Utility functions
│   └── cli.py           # Command-line interface
├── tests/
│   ├── __init__.py
│   └── test_core.py     # Unit tests
├── requirements.txt     # Core dependencies
├── requirements-dev.txt # Development dependencies
├── setup.py            # Package setup
└── README.md           # This file
```

## Dependencies

### Core Dependencies

- `jamorasep`: For accurate Japanese mora splitting

### Development Dependencies

- `pytest`: Testing framework
- `black`: Code formatting
- `flake8`: Code linting
- `mypy`: Type checking
- `pytest-cov`: Test coverage

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes following the coding standards
4. Add tests for new functionality
5. Ensure all tests pass and code coverage is maintained
6. Commit your changes (`git commit -m 'Add some amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Coding Standards

- Follow PEP 8 Python style guidelines
- Use type hints for all function parameters and return values
- Include comprehensive docstrings with examples
- Maintain test coverage above 80%
- Use meaningful variable and function names

## Domain Knowledge

### Sagisaka Rules (匂坂規則)

The Sagisaka rules are linguistic rules for Japanese accent processing. The current implementation includes:

- Accent nucleus positioning based on mora count
- Accent phrase boundary detection
- Rising and falling tone assignment

### Accent Nucleus Patterns

```
0:     |x[xxxxxxxx|  (no accent nucleus)
1:     |x]xxxxxxxx|  (accent on first mora)
2:     |x[x]xxxxxx|  (accent on second mora)
3:     |x[xx]xxxxx|  (accent on third mora)
4:     |x[xxx]xxxx|  (accent on fourth mora)
n-1:   |x[xxxxxxx]|  (accent on second-to-last mora)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### [0.1.0] - 2024-XX-XX
- Initial release
- Basic project structure
- Core accent processing functionality
- Mora splitting using jamorasep
- Text normalization utilities
- Accent mark embedding and extraction
- Comprehensive test suite
