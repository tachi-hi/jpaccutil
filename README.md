# jpaccutil

A utility package for Japanese accent processing.

## Description

jpaccutil is a Python package designed to provide utilities for Japanese accent processing. This package implements the Sagisaka rules (匂坂規則) to automatically add accent marks to Japanese text.

## Features

- Implementation of Sagisaka rules for Japanese accent processing
- Automatic accent mark insertion
- Support for various Japanese text formats (hiragana, katakana, kanji readings)
- Command-line interface for batch processing
- Flexible accent notation formats

## Installation

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

## Usage

### Basic Accent Mark Embedding

```python
import jpaccutil

# Embed accent marks based on accent nucleus position
result = jpaccutil.embed_accent_marks("こんにちは", 0)  # No accent nucleus
print(result)  # |こ[んにちは|

result = jpaccutil.embed_accent_marks("こんにちは", 1)  # Accent on first mora
print(result)  # |こ]んにちは|

result = jpaccutil.embed_accent_marks("こんにちは", 2)  # Accent on second mora
print(result)  # |こ[ん]にちは|

result = jpaccutil.embed_accent_marks("こんにちは", 3)  # Accent on third mora
print(result)  # |こん[に]ちは|
```

### Using jamorasep for Mora Splitting

```python
# Split text into morae using jamorasep library
morae = jpaccutil.split_into_mora("こんにちは")
print(morae)  # ['こ', 'ん', 'に', 'ち', 'は']

# Count morae
count = jpaccutil.count_mora("こんにちは")
print(count)  # 5
```

## Development

### Setting up development environment

```bash
# Clone the repository
git clone https://github.com/yourusername/jpaccutil.git
cd jpaccutil

# Install in development mode with dev dependencies
pip install -e ".[dev]"
```

### Running tests

```bash
pytest
```

### Code formatting

```bash
black jpaccutil/
```

### Linting

```bash
flake8 jpaccutil/
```

### Type checking

```bash
mypy jpaccutil/
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### [0.1.0] - 2024-XX-XX
- Initial release
- Basic project structure
