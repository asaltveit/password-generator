"""
Integration tests for the CLI interface.
"""

import unittest
import subprocess
import sys
import os


class TestCLI(unittest.TestCase):
    """Integration tests for the command-line interface."""
    
    def _run_cli(self, args):
        """Helper method to run CLI and return result."""
        # cli.py is in the parent directory
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        cli_path = os.path.join(parent_dir, 'cli.py')
        cmd = [sys.executable, cli_path] + args
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=5
        )
        return result
    
    def test_basic_generation(self):
        """Test basic password generation."""
        result = self._run_cli([])
        
        self.assertEqual(result.returncode, 0)
        self.assertEqual(len(result.stdout.strip()), 16)
        self.assertEqual(len(result.stderr), 0)
    
    def test_custom_length(self):
        """Test password generation with custom length."""
        result = self._run_cli(['-l', '20'])
        
        self.assertEqual(result.returncode, 0)
        self.assertEqual(len(result.stdout.strip()), 20)
    
    def test_multiple_passwords(self):
        """Test generating multiple passwords."""
        result = self._run_cli(['-l', '12', '-n', '5'])
        
        self.assertEqual(result.returncode, 0)
        lines = result.stdout.strip().split('\n')
        self.assertEqual(len(lines), 5)
        
        for line in lines:
            # Format: "1: password"
            parts = line.split(': ', 1)
            self.assertEqual(len(parts), 2)
            password = parts[1]
            self.assertEqual(len(password), 12)
    
    def test_no_lowercase(self):
        """Test excluding lowercase letters."""
        result = self._run_cli(['-l', '16', '--no-lowercase'])
        
        self.assertEqual(result.returncode, 0)
        password = result.stdout.strip()
        self.assertFalse(any(c.islower() for c in password))
    
    def test_no_uppercase(self):
        """Test excluding uppercase letters."""
        result = self._run_cli(['-l', '16', '--no-uppercase'])
        
        self.assertEqual(result.returncode, 0)
        password = result.stdout.strip()
        self.assertFalse(any(c.isupper() for c in password))
    
    def test_no_digits(self):
        """Test excluding digits."""
        result = self._run_cli(['-l', '16', '--no-digits'])
        
        self.assertEqual(result.returncode, 0)
        password = result.stdout.strip()
        self.assertFalse(any(c.isdigit() for c in password))
    
    def test_no_symbols(self):
        """Test excluding symbols."""
        result = self._run_cli(['-l', '16', '--no-symbols'])
        
        self.assertEqual(result.returncode, 0)
        password = result.stdout.strip()
        import string
        self.assertFalse(any(c in string.punctuation for c in password))
    
    def test_exclude_ambiguous(self):
        """Test excluding ambiguous characters."""
        result = self._run_cli(['-l', '20', '--exclude-ambiguous'])
        
        self.assertEqual(result.returncode, 0)
        password = result.stdout.strip()
        
        # Generate multiple times to increase chance of hitting ambiguous chars
        for _ in range(10):
            result = self._run_cli(['-l', '20', '--exclude-ambiguous'])
            password = result.stdout.strip()
            self.assertNotIn('0', password)
            self.assertNotIn('O', password)
            self.assertNotIn('l', password)
            self.assertNotIn('1', password)
            self.assertNotIn('I', password)
            self.assertNotIn('|', password)
    
    def test_symbol_set_common(self):
        """Test using common symbol set."""
        result = self._run_cli(['-l', '16', '--symbol-set', 'common'])
        
        self.assertEqual(result.returncode, 0)
        password = result.stdout.strip()
        self.assertEqual(len(password), 16)
    
    def test_symbol_set_minimal(self):
        """Test using minimal symbol set."""
        result = self._run_cli(['-l', '16', '--symbol-set', 'minimal'])
        
        self.assertEqual(result.returncode, 0)
        password = result.stdout.strip()
        self.assertEqual(len(password), 16)
    
    def test_symbol_set_no_exclamation(self):
        """Test using no-exclamation symbol set."""
        result = self._run_cli(['-l', '16', '--symbol-set', 'no-exclamation'])
        
        self.assertEqual(result.returncode, 0)
        password = result.stdout.strip()
        self.assertNotIn('!', password)
    
    def test_custom_symbols(self):
        """Test using custom symbol set."""
        result = self._run_cli(['-l', '16', '--custom-symbols', '!@#'])
        
        self.assertEqual(result.returncode, 0)
        password = result.stdout.strip()
        self.assertEqual(len(password), 16)
        
        # Check that any symbols in password are from custom set
        import string
        symbols_in_password = [c for c in password if c in string.punctuation]
        for symbol in symbols_in_password:
            self.assertIn(symbol, '!@#')
    
    def test_list_symbol_sets(self):
        """Test listing available symbol sets."""
        result = self._run_cli(['--list-symbol-sets'])
        
        self.assertEqual(result.returncode, 0)
        self.assertIn('Available symbol sets', result.stdout)
        self.assertIn('full', result.stdout)
        self.assertIn('common', result.stdout)
        self.assertIn('minimal', result.stdout)
        self.assertIn('no-exclamation', result.stdout)
    
    def test_invalid_length(self):
        """Test error handling for invalid length."""
        result = self._run_cli(['-l', '3'])
        
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('at least 4', result.stderr.lower())
    
    def test_invalid_count(self):
        """Test error handling for invalid count."""
        result = self._run_cli(['-n', '0'])
        
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('at least 1', result.stderr.lower())
    
    def test_no_character_types(self):
        """Test error when all character types are disabled."""
        result = self._run_cli([
            '--no-lowercase',
            '--no-uppercase',
            '--no-digits',
            '--no-symbols'
        ])
        
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('at least one character type', result.stderr.lower())
    
    def test_invalid_symbol_set(self):
        """Test error handling for invalid symbol set."""
        result = self._run_cli(['--symbol-set', 'invalid'])
        
        self.assertNotEqual(result.returncode, 0)
        # Should show available options or error message
        self.assertTrue(len(result.stderr) > 0)
    
    def test_help_message(self):
        """Test help message is displayed."""
        result = self._run_cli(['--help'])
        
        self.assertEqual(result.returncode, 0)
        self.assertIn('Generate secure passwords', result.stdout)
        self.assertIn('--length', result.stdout)
        self.assertIn('--count', result.stdout)
    
    def test_combined_options(self):
        """Test combining multiple options."""
        result = self._run_cli([
            '-l', '20',
            '-n', '3',
            '--symbol-set', 'common',
            '--exclude-ambiguous'
        ])
        
        self.assertEqual(result.returncode, 0)
        lines = result.stdout.strip().split('\n')
        self.assertEqual(len(lines), 3)
        
        for line in lines:
            parts = line.split(': ', 1)
            password = parts[1]
            self.assertEqual(len(password), 20)
            # Check ambiguous chars are excluded
            self.assertNotIn('0', password)
            self.assertNotIn('O', password)
            self.assertNotIn('l', password)
            self.assertNotIn('1', password)
            self.assertNotIn('I', password)
            self.assertNotIn('|', password)


if __name__ == '__main__':
    unittest.main()

