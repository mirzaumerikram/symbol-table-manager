"""
Mini Compiler - Main Driver
Group 6: Compiler Construction Project
Course: CSCS4573

Main program that orchestrates the compilation process and
demonstrates the Symbol Table Manager functionality.
"""

import sys
from pathlib import Path
from lexer import Lexer
from parser import Parser


def compile_file(filepath: str) -> None:
    """
    Compile a source file and display the symbol table.
    
    Args:
        filepath: Path to the source file
    """
    print("\n" + "="*80)
    print("MINI COMPILER - Symbol Table Manager Demo")
    print("Group 6: Compiler Construction Project (CSCS4573)")
    print("="*80)
    
    # Read source file
    try:
        with open(filepath, 'r') as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"ERROR: File '{filepath}' not found")
        return
    except Exception as e:
        print(f"ERROR: Could not read file '{filepath}': {e}")
        return
    
    print(f"\nSource File: {filepath}")
    print("-"*80)
    print(source_code)
    print("-"*80)
    
    # Phase 1: Lexical Analysis
    print("\n[Phase 1: Lexical Analysis]")
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    print(f"✓ Tokenization complete: {len(tokens)} tokens generated")
    
    # Optional: Display tokens
    # lexer.display_tokens()
    
    # Phase 2: Syntax and Semantic Analysis
    print("\n[Phase 2: Syntax and Semantic Analysis]")
    parser = Parser(tokens)
    symbol_table = parser.parse()
    
    # Check for errors
    errors = parser.get_errors()
    if errors:
        print(f"\n✗ Compilation failed with {len(errors)} error(s):")
        for error in errors:
            print(f"  • {error}")
    else:
        print("✓ Syntax and semantic analysis complete")
    
    # Phase 3: Display Symbol Table
    print("\n[Phase 3: Symbol Table]")
    symbol_table.display()
    
    # Display statistics
    stats = symbol_table.get_statistics()
    print("\n" + "="*80)
    print("COMPILATION STATISTICS")
    print("="*80)
    print(f"Total Tokens:        {len(tokens)}")
    print(f"Total Symbols:       {stats['total_symbols']}")
    print(f"Total Scopes:        {stats['total_scopes']}")
    print(f"Initialized Vars:    {stats['initialized']}")
    print(f"Used Vars:           {stats['used']}")
    print(f"Unused Vars:         {stats['unused']}")
    print(f"Compilation Errors:  {len(errors)}")
    print("="*80)
    
    # Warnings for unused variables
    if stats['unused'] > 0:
        print("\nWARNINGS:")
        all_symbols = symbol_table.get_all_symbols()
        for symbol in all_symbols:
            if not symbol.used:
                print(f"  • Line {symbol.line_number}: Variable '{symbol.name}' declared but never used")
    
    print()


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python compiler.py <source_file>")
        print("\nExample:")
        print("  python compiler.py examples/test_program1.txt")
        sys.exit(1)
    
    source_file = sys.argv[1]
    compile_file(source_file)


if __name__ == "__main__":
    main()
