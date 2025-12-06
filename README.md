# Password Generator

A secure password generator for online accounts using Python's `secrets` module for cryptographically strong randomness.

## Features

- **Cryptographically secure**: Uses Python's `secrets` module (not `random`)
- **Guaranteed character variety**: Ensures at least one character from each enabled category
- **Configurable length**: Set any password length (minimum 4 characters)
- **Flexible character sets**: Enable/disable lowercase, uppercase, digits, and symbols
- **Predefined symbol sets**: Choose from common, minimal, url-safe, and other symbol sets
- **Custom symbol sets**: Specify exactly which symbols are allowed
- **Ambiguous character exclusion**: Option to exclude easily confused characters (0, O, l, 1, I, |)
- **Multiple passwords**: Generate multiple passwords at once
- **Command-line interface**: Easy to use from the terminal

## Installation

No external dependencies required! This uses only Python's standard library (Python 3.6+).

### Quick Start

1. Download or clone this repository
2. Open a terminal/command prompt
3. Navigate to the project directory
4. Run the generator:
   - **Windows**: `python cli.py` or `py cli.py`
   - **Mac/Linux**: `python3 cli.py`

**Note on Python commands:**
- On **Windows**: Use `python` or `py` (e.g., `python cli.py` or `py cli.py`)
- On **Mac/Linux**: Use `python3` (e.g., `python3 cli.py`)
- If `python` works on your system, you can use it instead of `python3`

## Usage

### Command Line

Basic usage (generates a 16-character password):
```bash
python cli.py
```
*Note: On Mac/Linux, you may need to use `python3 cli.py` instead of `python cli.py`*

Generate a password of specific length:
```bash
python cli.py -l 20
```

Generate multiple passwords:
```bash
python cli.py -l 12 -n 5
```

Generate password without special characters:
```bash
python cli.py -l 16 --no-symbols
```

Exclude ambiguous characters:
```bash
python cli.py -l 20 --exclude-ambiguous
```

Customize character sets:
```bash
python cli.py -l 16 --no-digits --no-symbols  # Only letters
```

Use a predefined symbol set (for systems with restricted character sets):
```bash
python cli.py -l 16 --symbol-set common    # Most commonly accepted symbols
python cli.py -l 16 --symbol-set minimal   # Basic symbol set
python cli.py -l 16 --symbol-set url-safe  # URL-safe symbols
```

Use a custom symbol set:
```bash
python cli.py -l 16 --custom-symbols "!@#$%"
```

List available symbol sets:
```bash
python cli.py --list-symbol-sets
```

### Python API

```python
from password_generator import generate_password, PasswordGenerator

# Quick generation
password = generate_password(length=16)
print(password)

# Advanced usage
generator = PasswordGenerator(
    include_lowercase=True,
    include_uppercase=True,
    include_digits=True,
    include_symbols=True,
    exclude_ambiguous=False
)

password = generator.generate(length=20)
passwords = generator.generate_multiple(count=5, length=16)

# Using predefined symbol sets
generator = PasswordGenerator(
    symbol_set='common'  # Use common symbol set
)
password = generator.generate(length=16)

# Using custom symbol set
generator = PasswordGenerator(
    custom_symbols='!@#$%^&*'  # Only these symbols allowed
)
password = generator.generate(length=16)
```

## Symbol Sets

Different systems have varying requirements for special characters. This generator provides several predefined symbol sets:

- **full** (default): All punctuation characters `!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~`
- **common**: Most commonly accepted `!@#$%^&*_-+=`
- **minimal**: Basic set `!@#$%&*`
- **url-safe**: Avoids characters needing URL encoding `!@#$%&*+-_=`
- **shell-safe**: Safe for shell usage `!@#$%^&*_-+=` (same as common)
- **no-exclamation**: Common symbols without exclamation mark `@#$%^&*_-+=`
- **full-no-exclamation**: All punctuation except exclamation mark `"#$%&'()*+,-./:;<=>?@[\]^_`{|}~`
- **alphanumeric-only**: No symbols (use with `--no-symbols` instead)

You can also specify a custom symbol set using `--custom-symbols` followed by the exact characters you want to allow.

## Testing

The project includes comprehensive unit and integration tests. To run the tests:

```bash
# Run all tests
python -m unittest discover -s tests -p "test_*.py" -v

# Run unit tests only
python -m unittest tests.test_password_generator -v

# Run integration tests only
python -m unittest tests.test_cli -v
```

*Note: On Mac/Linux, use `python3` instead of `python` if needed.*

The test suite includes:
- **Unit tests**: Test the `PasswordGenerator` class and helper functions
  - Password generation with various configurations
  - Character variety guarantees
  - Symbol set validation
  - Error handling
  - Edge cases

- **Integration tests**: Test the CLI interface
  - Command-line argument parsing
  - Output validation
  - Error message handling
  - Combined options

## Security Notes

- Uses `secrets` module which provides cryptographically strong random numbers
- Each character is independently random
- Passwords are shuffled after generation to avoid predictable patterns
- Minimum recommended length is 12 characters, but 16+ is better for high-security accounts

## Command-Line Options

```
-l, --length          Password length (default: 16, minimum: 4)
-n, --count           Number of passwords to generate (default: 1)
--no-lowercase        Exclude lowercase letters
--no-uppercase        Exclude uppercase letters
--no-digits           Exclude digits
--no-symbols          Exclude special characters
--exclude-ambiguous   Exclude ambiguous characters (0, O, l, 1, I, |)
--symbol-set          Use predefined symbol set (full, common, minimal, url-safe, shell-safe, no-exclamation, full-no-exclamation, alphanumeric-only)
--custom-symbols      Custom string of allowed symbols (overrides --symbol-set)
--list-symbol-sets    List all available symbol sets and exit
```

## Examples

*Note: On Mac/Linux, replace `python` with `python3` if needed. On Windows, you can also use `py`.*

```bash
# Default 16-character password
python cli.py

# Strong 24-character password
python cli.py -l 24

# Generate 10 passwords for testing
python cli.py -l 12 -n 10

# PIN-like password (digits only)
python cli.py -l 6 --no-lowercase --no-uppercase --no-symbols

# Easy-to-read password (no ambiguous chars)
python cli.py -l 16 --exclude-ambiguous

# Use common symbol set (for restrictive systems)
python cli.py -l 16 --symbol-set common

# Use symbol set without exclamation mark
python cli.py -l 16 --symbol-set no-exclamation

# Custom symbol set (only specific characters)
# Windows: Use double quotes or escape quotes
python cli.py -l 16 --custom-symbols "!@#$%"
# Mac/Linux: Single or double quotes work
python cli.py -l 16 --custom-symbols '!@#$%'

# List available symbol sets
python cli.py --list-symbol-sets
```
