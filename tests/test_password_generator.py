"""
Unit tests for the password generator module.
"""

import unittest
import string
from password_generator import (
    PasswordGenerator,
    generate_password,
    list_symbol_sets,
    SYMBOL_SETS
)


class TestPasswordGenerator(unittest.TestCase):
    """Unit tests for PasswordGenerator class."""
    
    def test_default_generation(self):
        """Test default password generation."""
        generator = PasswordGenerator()
        password = generator.generate(16)
        
        self.assertEqual(len(password), 16)
        self.assertTrue(any(c.islower() for c in password))
        self.assertTrue(any(c.isupper() for c in password))
        self.assertTrue(any(c.isdigit() for c in password))
        self.assertTrue(any(c in string.punctuation for c in password))
    
    def test_password_length(self):
        """Test password length is correct."""
        generator = PasswordGenerator()
        
        for length in [4, 8, 12, 16, 20, 32]:
            password = generator.generate(length)
            self.assertEqual(len(password), length)
    
    def test_minimum_length_validation(self):
        """Test that minimum length is enforced."""
        generator = PasswordGenerator()
        
        with self.assertRaises(ValueError) as context:
            generator.generate(3)
        self.assertIn("at least 4", str(context.exception))
    
    def test_character_variety_lowercase(self):
        """Test that lowercase letters are included when enabled."""
        generator = PasswordGenerator(
            include_lowercase=True,
            include_uppercase=False,
            include_digits=False,
            include_symbols=False
        )
        
        password = generator.generate(10)
        self.assertTrue(any(c.islower() for c in password))
        self.assertTrue(all(c.islower() for c in password))
    
    def test_character_variety_uppercase(self):
        """Test that uppercase letters are included when enabled."""
        generator = PasswordGenerator(
            include_lowercase=False,
            include_uppercase=True,
            include_digits=False,
            include_symbols=False
        )
        
        password = generator.generate(10)
        self.assertTrue(any(c.isupper() for c in password))
        self.assertTrue(all(c.isupper() for c in password))
    
    def test_character_variety_digits(self):
        """Test that digits are included when enabled."""
        generator = PasswordGenerator(
            include_lowercase=False,
            include_uppercase=False,
            include_digits=True,
            include_symbols=False
        )
        
        password = generator.generate(10)
        self.assertTrue(any(c.isdigit() for c in password))
        self.assertTrue(all(c.isdigit() for c in password))
    
    def test_character_variety_symbols(self):
        """Test that symbols are included when enabled."""
        generator = PasswordGenerator(
            include_lowercase=False,
            include_uppercase=False,
            include_digits=False,
            include_symbols=True
        )
        
        password = generator.generate(10)
        self.assertTrue(any(c in string.punctuation for c in password))
        self.assertTrue(all(c in string.punctuation for c in password))
    
    def test_all_character_types(self):
        """Test that all character types are included when all enabled."""
        generator = PasswordGenerator()
        password = generator.generate(20)
        
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(c in string.punctuation for c in password)
        
        self.assertTrue(has_lower)
        self.assertTrue(has_upper)
        self.assertTrue(has_digit)
        self.assertTrue(has_symbol)
    
    def test_exclude_ambiguous(self):
        """Test that ambiguous characters are excluded when enabled."""
        generator = PasswordGenerator(exclude_ambiguous=True)
        
        # Generate multiple passwords to increase chance of hitting ambiguous chars
        for _ in range(50):
            password = generator.generate(20)
            self.assertNotIn('0', password)
            self.assertNotIn('O', password)
            self.assertNotIn('l', password)
            self.assertNotIn('1', password)
            self.assertNotIn('I', password)
            self.assertNotIn('|', password)
    
    def test_exclude_ambiguous_lowercase(self):
        """Test ambiguous lowercase exclusion."""
        generator = PasswordGenerator(
            include_lowercase=True,
            include_uppercase=False,
            include_digits=False,
            include_symbols=False,
            exclude_ambiguous=True
        )
        
        for _ in range(50):
            password = generator.generate(10)
            self.assertNotIn('l', password)
            self.assertNotIn('o', password)
    
    def test_exclude_ambiguous_uppercase(self):
        """Test ambiguous uppercase exclusion."""
        generator = PasswordGenerator(
            include_lowercase=False,
            include_uppercase=True,
            include_digits=False,
            include_symbols=False,
            exclude_ambiguous=True
        )
        
        for _ in range(50):
            password = generator.generate(10)
            self.assertNotIn('I', password)
            self.assertNotIn('O', password)
    
    def test_exclude_ambiguous_digits(self):
        """Test ambiguous digit exclusion."""
        generator = PasswordGenerator(
            include_lowercase=False,
            include_uppercase=False,
            include_digits=True,
            include_symbols=False,
            exclude_ambiguous=True
        )
        
        for _ in range(50):
            password = generator.generate(10)
            self.assertNotIn('0', password)
            self.assertNotIn('1', password)
    
    def test_no_character_types_error(self):
        """Test error when no character types are enabled."""
        with self.assertRaises(ValueError) as context:
            PasswordGenerator(
                include_lowercase=False,
                include_uppercase=False,
                include_digits=False,
                include_symbols=False
            )
        self.assertIn("At least one character type", str(context.exception))
    
    def test_length_insufficient_for_categories(self):
        """Test error when length is less than number of categories."""
        generator = PasswordGenerator()
        
        # With 4 categories, length must be at least 4
        with self.assertRaises(ValueError) as context:
            generator.generate(3)
        self.assertIn("at least", str(context.exception))
    
    def test_generate_multiple(self):
        """Test generating multiple passwords."""
        generator = PasswordGenerator()
        passwords = generator.generate_multiple(5, 12)
        
        self.assertEqual(len(passwords), 5)
        for password in passwords:
            self.assertEqual(len(password), 12)
            # Check variety
            self.assertTrue(any(c.islower() for c in password))
            self.assertTrue(any(c.isupper() for c in password))
            self.assertTrue(any(c.isdigit() for c in password))
            self.assertTrue(any(c in string.punctuation for c in password))
    
    def test_generate_multiple_uniqueness(self):
        """Test that multiple passwords are likely unique."""
        generator = PasswordGenerator()
        passwords = generator.generate_multiple(100, 16)
        
        # With 100 passwords, we should have high uniqueness
        unique_passwords = set(passwords)
        self.assertGreater(len(unique_passwords), 95)  # Allow for rare collisions
    
    def test_symbol_set_full(self):
        """Test full symbol set."""
        generator = PasswordGenerator(symbol_set='full')
        password = generator.generate(20)
        
        # Should contain at least one symbol from full set
        has_symbol = any(c in string.punctuation for c in password)
        self.assertTrue(has_symbol)
    
    def test_symbol_set_common(self):
        """Test common symbol set."""
        generator = PasswordGenerator(symbol_set='common')
        password = generator.generate(20)
        
        # Should only contain symbols from common set
        symbols_in_password = [c for c in password if c in string.punctuation]
        if symbols_in_password:
            for symbol in symbols_in_password:
                self.assertIn(symbol, SYMBOL_SETS['common'])
    
    def test_symbol_set_minimal(self):
        """Test minimal symbol set."""
        generator = PasswordGenerator(symbol_set='minimal')
        password = generator.generate(20)
        
        symbols_in_password = [c for c in password if c in string.punctuation]
        if symbols_in_password:
            for symbol in symbols_in_password:
                self.assertIn(symbol, SYMBOL_SETS['minimal'])
    
    def test_symbol_set_no_exclamation(self):
        """Test no-exclamation symbol set."""
        generator = PasswordGenerator(symbol_set='no-exclamation')
        
        # Generate multiple passwords
        for _ in range(50):
            password = generator.generate(20)
            self.assertNotIn('!', password)
            # Should still have other symbols
            has_symbol = any(c in SYMBOL_SETS['no-exclamation'] for c in password)
            if any(c in string.punctuation for c in password):
                self.assertTrue(has_symbol)
    
    def test_symbol_set_full_no_exclamation(self):
        """Test full-no-exclamation symbol set."""
        generator = PasswordGenerator(symbol_set='full-no-exclamation')
        
        for _ in range(50):
            password = generator.generate(20)
            self.assertNotIn('!', password)
    
    def test_custom_symbols(self):
        """Test custom symbol set."""
        custom_symbols = '!@#$%'
        generator = PasswordGenerator(custom_symbols=custom_symbols)
        
        # Generate multiple passwords
        for _ in range(50):
            password = generator.generate(20)
            symbols_in_password = [c for c in password if c in string.punctuation]
            if symbols_in_password:
                for symbol in symbols_in_password:
                    self.assertIn(symbol, custom_symbols)
    
    def test_custom_symbols_override_symbol_set(self):
        """Test that custom_symbols overrides symbol_set."""
        generator = PasswordGenerator(
            symbol_set='common',
            custom_symbols='!@#'
        )
        
        # Custom symbols should be used, not common set
        for _ in range(50):
            password = generator.generate(20)
            symbols_in_password = [c for c in password if c in string.punctuation]
            if symbols_in_password:
                for symbol in symbols_in_password:
                    self.assertIn(symbol, '!@#')
    
    def test_invalid_symbol_set(self):
        """Test error for invalid symbol set."""
        with self.assertRaises(ValueError) as context:
            PasswordGenerator(symbol_set='invalid-set')
        self.assertIn("Unknown symbol set", str(context.exception))
    
    def test_symbol_set_alphanumeric_only(self):
        """Test alphanumeric-only symbol set (no symbols)."""
        generator = PasswordGenerator(symbol_set='alphanumeric-only')
        password = generator.generate(20)
        
        # Should not contain any punctuation
        self.assertFalse(any(c in string.punctuation for c in password))
        # Should still have letters and/or digits
        self.assertTrue(any(c.isalnum() for c in password))
    
    def test_all_symbol_sets(self):
        """Test all predefined symbol sets."""
        for symbol_set_name in SYMBOL_SETS.keys():
            if symbol_set_name == 'alphanumeric-only':
                continue  # Tested separately
            
            generator = PasswordGenerator(symbol_set=symbol_set_name)
            password = generator.generate(16)
            
            # Should generate valid password
            self.assertEqual(len(password), 16)
            
            # If symbol set has characters, password should have symbols
            if SYMBOL_SETS[symbol_set_name]:
                symbols_in_password = [c for c in password if c in string.punctuation]
                if symbols_in_password:
                    for symbol in symbols_in_password:
                        self.assertIn(symbol, SYMBOL_SETS[symbol_set_name])


class TestHelperFunctions(unittest.TestCase):
    """Unit tests for helper functions."""
    
    def test_generate_password_function(self):
        """Test generate_password convenience function."""
        password = generate_password(length=16)
        
        self.assertEqual(len(password), 16)
        self.assertTrue(any(c.islower() for c in password))
        self.assertTrue(any(c.isupper() for c in password))
        self.assertTrue(any(c.isdigit() for c in password))
        self.assertTrue(any(c in string.punctuation for c in password))
    
    def test_generate_password_with_options(self):
        """Test generate_password with various options."""
        password = generate_password(
            length=20,
            include_lowercase=True,
            include_uppercase=False,
            include_digits=True,
            include_symbols=False,
            exclude_ambiguous=True
        )
        
        self.assertEqual(len(password), 20)
        self.assertTrue(any(c.islower() for c in password))
        self.assertTrue(any(c.isdigit() for c in password))
        self.assertFalse(any(c.isupper() for c in password))
        self.assertFalse(any(c in string.punctuation for c in password))
        self.assertNotIn('0', password)
        self.assertNotIn('1', password)
        self.assertNotIn('l', password)
        self.assertNotIn('o', password)
    
    def test_list_symbol_sets(self):
        """Test list_symbol_sets function."""
        symbol_sets = list_symbol_sets()
        
        self.assertIsInstance(symbol_sets, dict)
        self.assertEqual(symbol_sets, SYMBOL_SETS)
        # Should be a copy, not the same object
        self.assertIsNot(symbol_sets, SYMBOL_SETS)
        
        # Check that all expected sets are present
        expected_sets = [
            'full', 'common', 'minimal', 'url-safe', 'shell-safe',
            'no-exclamation', 'full-no-exclamation', 'alphanumeric-only'
        ]
        for expected_set in expected_sets:
            self.assertIn(expected_set, symbol_sets)


if __name__ == '__main__':
    unittest.main()

