#!/usr/bin/env python3
"""
Command-line interface for the password generator.
"""

import argparse
import sys
from password_generator import PasswordGenerator, list_symbol_sets


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate secure passwords using cryptographically strong randomness",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
            Examples:
            %(prog)s                              # Generate a 16-character password
            %(prog)s -l 20                        # Generate a 20-character password
            %(prog)s -l 12 -n 5                   # Generate 5 passwords of 12 characters each
            %(prog)s -l 16 --no-symbols           # Generate password without special characters
            %(prog)s -l 20 --exclude-ambiguous    # Exclude ambiguous characters (0, O, l, 1, I, |)
            %(prog)s -l 16 --symbol-set common     # Use common symbol set (!@#$%%^&*_-+=)
            %(prog)s -l 16 --custom-symbols "!@#"  # Use custom symbol set
            %(prog)s --list-symbol-sets            # List available symbol sets
        """
    )
    
    parser.add_argument(
        '-l', '--length',
        type=int,
        default=16,
        help='Password length (default: 16, minimum: 4)'
    )
    
    parser.add_argument(
        '-n', '--count',
        type=int,
        default=1,
        help='Number of passwords to generate (default: 1)'
    )
    
    parser.add_argument(
        '--no-lowercase',
        action='store_true',
        help='Exclude lowercase letters'
    )
    
    parser.add_argument(
        '--no-uppercase',
        action='store_true',
        help='Exclude uppercase letters'
    )
    
    parser.add_argument(
        '--no-digits',
        action='store_true',
        help='Exclude digits'
    )
    
    parser.add_argument(
        '--no-symbols',
        action='store_true',
        help='Exclude special characters'
    )
    
    parser.add_argument(
        '--exclude-ambiguous',
        action='store_true',
        help='Exclude ambiguous characters (0, O, l, 1, I, |)'
    )
    
    parser.add_argument(
        '--symbol-set',
        choices=['full', 'common', 'minimal', 'url-safe', 'shell-safe', 'no-exclamation', 'full-no-exclamation', 'alphanumeric-only'],
        help='Use a predefined symbol set (default: full). Options: full, common, minimal, url-safe, shell-safe, no-exclamation, full-no-exclamation, alphanumeric-only'
    )
    
    parser.add_argument(
        '--custom-symbols',
        type=str,
        help='Custom string of allowed symbols (overrides --symbol-set)'
    )
    
    parser.add_argument(
        '--list-symbol-sets',
        action='store_true',
        help='List all available symbol sets and exit'
    )
    
    args = parser.parse_args()
    
    # Handle list-symbol-sets early
    if args.list_symbol_sets:
        symbol_sets = list_symbol_sets()
        print("Available symbol sets:")
        print()
        for name, chars in symbol_sets.items():
            if chars:
                print(f"  {name:20} {chars}")
            else:
                print(f"  {name:20} (no symbols)")
        sys.exit(0)
    
    # Validate arguments
    if args.length < 4:
        parser.error("Password length must be at least 4 characters")
    
    if args.count < 1:
        parser.error("Count must be at least 1")
    
    # Check that at least one character type is enabled
    if all([args.no_lowercase, args.no_uppercase, args.no_digits, args.no_symbols]):
        parser.error("At least one character type must be enabled")
    
    try:
        generator = PasswordGenerator(
            include_lowercase=not args.no_lowercase,
            include_uppercase=not args.no_uppercase,
            include_digits=not args.no_digits,
            include_symbols=not args.no_symbols,
            exclude_ambiguous=args.exclude_ambiguous,
            symbol_set=args.symbol_set,
            custom_symbols=args.custom_symbols
        )
        
        if args.count == 1:
            password = generator.generate(args.length)
            print(password)
        else:
            passwords = generator.generate_multiple(args.count, args.length)
            for i, password in enumerate(passwords, 1):
                print(f"{i}: {password}")
    
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

