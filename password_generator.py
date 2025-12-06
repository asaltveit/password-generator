"""
Secure password generator using cryptographically strong randomness.

This module provides password generation functionality using Python's secrets
module, which is designed for cryptographic security.
"""

import secrets
import string
from typing import Optional


# Predefined symbol sets for common password requirements
SYMBOL_SETS = {
    'full': string.punctuation,  # All punctuation: !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    'common': '!@#$%^&*_-+=',  # Most commonly accepted symbols
    'minimal': '!@#$%&*',  # Basic set, widely supported
    'url-safe': '!@#$%&*+-_=',  # Avoids characters that need URL encoding
    'shell-safe': '!@#$%^&*_-+=',  # Safe for shell usage (same as common)
    'no-exclamation': '@#$%^&*_-+=',  # Common symbols without exclamation mark
    'full-no-exclamation': string.punctuation.replace('!', ''),  # All punctuation except !
    'alphanumeric-only': '',  # No symbols
}


class PasswordGenerator:
    """Generate secure passwords with guaranteed character variety."""
    
    def __init__(
        self,
        include_lowercase: bool = True,
        include_uppercase: bool = True,
        include_digits: bool = True,
        include_symbols: bool = True,
        exclude_ambiguous: bool = False,
        symbol_set: Optional[str] = None,
        custom_symbols: Optional[str] = None
    ):
        """
        Initialize the password generator with character set options.
        
        Args:
            include_lowercase: Include lowercase letters (a-z)
            include_uppercase: Include uppercase letters (A-Z)
            include_digits: Include digits (0-9)
            include_symbols: Include special characters (!@#$% etc.)
            exclude_ambiguous: Exclude ambiguous characters (0, O, l, 1, I, |)
            symbol_set: Predefined symbol set name ('full', 'common', 'minimal', 
                      'url-safe', 'shell-safe', 'alphanumeric-only')
            custom_symbols: Custom string of allowed symbols (overrides symbol_set)
        """
        self.include_lowercase = include_lowercase
        self.include_uppercase = include_uppercase
        self.include_digits = include_digits
        self.include_symbols = include_symbols
        self.exclude_ambiguous = exclude_ambiguous
        self.symbol_set = symbol_set
        self.custom_symbols = custom_symbols
        
        self._build_character_pool()
    
    def _build_character_pool(self) -> None:
        """Build the character pool based on configuration."""
        pool = []
        
        if self.include_lowercase:
            lowercase = string.ascii_lowercase
            if self.exclude_ambiguous:
                lowercase = lowercase.replace('l', '').replace('o', '')
            pool.append(lowercase)
        
        if self.include_uppercase:
            uppercase = string.ascii_uppercase
            if self.exclude_ambiguous:
                uppercase = uppercase.replace('I', '').replace('O', '')
            pool.append(uppercase)
        
        if self.include_digits:
            digits = string.digits
            if self.exclude_ambiguous:
                digits = digits.replace('0', '').replace('1', '')
            pool.append(digits)
        
        if self.include_symbols:
            # Determine which symbols to use
            if self.custom_symbols is not None:
                symbols = self.custom_symbols
            elif self.symbol_set is not None:
                if self.symbol_set not in SYMBOL_SETS:
                    raise ValueError(
                        f"Unknown symbol set '{self.symbol_set}'. "
                        f"Available sets: {', '.join(SYMBOL_SETS.keys())}"
                    )
                symbols = SYMBOL_SETS[self.symbol_set]
            else:
                symbols = string.punctuation
            
            if self.exclude_ambiguous:
                symbols = symbols.replace('|', '')
            
            if symbols:  # Only add if there are symbols
                pool.append(symbols)
        
        if not pool:
            raise ValueError("At least one character type must be enabled")
        
        self.character_pool = ''.join(pool)
        self._required_categories = [cat for cat in pool if cat]
    
    def generate(self, length: int = 16) -> str:
        """
        Generate a secure password with guaranteed character variety.
        
        Args:
            length: Desired password length (minimum 4, recommended 12+)
        
        Returns:
            A secure password string
        
        Raises:
            ValueError: If length is too short or character pool is insufficient
        """
        if length < 4:
            raise ValueError("Password length must be at least 4 characters")
        
        if length < len(self._required_categories):
            raise ValueError(
                f"Password length must be at least {len(self._required_categories)} "
                f"to guarantee one character from each category"
            )
        
        # Generate password ensuring at least one character from each category
        password_chars = []
        
        # First, ensure at least one character from each required category
        for category in self._required_categories:
            password_chars.append(secrets.choice(category))
        
        # Fill the rest with random characters from the full pool
        remaining_length = length - len(password_chars)
        for _ in range(remaining_length):
            password_chars.append(secrets.choice(self.character_pool))
        
        # Shuffle to avoid predictable patterns
        secrets.SystemRandom().shuffle(password_chars)
        
        return ''.join(password_chars)
    
    def generate_multiple(self, count: int, length: int = 16) -> list[str]:
        """
        Generate multiple unique passwords.
        
        Args:
            count: Number of passwords to generate
            length: Desired password length for each
        
        Returns:
            List of secure password strings
        """
        return [self.generate(length) for _ in range(count)]


def generate_password(
    length: int = 16,
    include_lowercase: bool = True,
    include_uppercase: bool = True,
    include_digits: bool = True,
    include_symbols: bool = True,
    exclude_ambiguous: bool = False,
    symbol_set: Optional[str] = None,
    custom_symbols: Optional[str] = None
) -> str:
    """
    Convenience function to generate a single password.
    
    Args:
        length: Desired password length
        include_lowercase: Include lowercase letters
        include_uppercase: Include uppercase letters
        include_digits: Include digits
        include_symbols: Include special characters
        exclude_ambiguous: Exclude ambiguous characters
        symbol_set: Predefined symbol set name
        custom_symbols: Custom string of allowed symbols
    
    Returns:
        A secure password string
    """
    generator = PasswordGenerator(
        include_lowercase=include_lowercase,
        include_uppercase=include_uppercase,
        include_digits=include_digits,
        include_symbols=include_symbols,
        exclude_ambiguous=exclude_ambiguous,
        symbol_set=symbol_set,
        custom_symbols=custom_symbols
    )
    return generator.generate(length)


def list_symbol_sets() -> dict[str, str]:
    """
    Get a dictionary of available predefined symbol sets.
    
    Returns:
        Dictionary mapping set names to their character strings
    """
    return SYMBOL_SETS.copy()

