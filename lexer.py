"""
Lexical Analyzer (Tokenizer) - Mini Compiler
Group 6: Compiler Construction Project
Course: CSCS4573

This module implements the lexical analyzer that breaks source code
into tokens for further processing.
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional


class TokenType(Enum):
    """Enumeration of all token types."""
    # Keywords
    KEYWORD = auto()
    
    # Identifiers and literals
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()
    
    # Operators
    OPERATOR = auto()
    
    # Delimiters
    DELIMITER = auto()
    
    # Special
    EOF = auto()
    NEWLINE = auto()
    COMMENT = auto()


@dataclass
class Token:
    """
    Represents a single token from the source code.
    
    Attributes:
        type: Type of the token
        value: The actual text value
        line_number: Line number where token appears
    """
    type: TokenType
    value: str
    line_number: int
    
    def __str__(self) -> str:
        """String representation of token."""
        return f"Token({self.type.name}, '{self.value}', line={self.line_number})"


class Lexer:
    """
    Lexical Analyzer for tokenizing source code.
    
    Recognizes:
    - Keywords: int, float, string, bool, if, else, while, for, return, etc.
    - Identifiers: variable names
    - Literals: numbers, strings
    - Operators: +, -, *, /, =, ==, !=, <, >, <=, >=, etc.
    - Delimiters: {, }, (, ), ;, ,
    """
    
    # Language keywords
    KEYWORDS = {
        'int', 'float', 'string', 'bool',
        'if', 'else', 'elif', 'while', 'for',
        'return', 'break', 'continue',
        'true', 'false', 'null',
        'const', 'function', 'begin', 'end'
    }
    
    # Operators
    OPERATORS = {
        '+', '-', '*', '/', '%',
        '=', '==', '!=', '<', '>', '<=', '>=',
        '&&', '||', '!',
        '+=', '-=', '*=', '/='
    }
    
    # Delimiters
    DELIMITERS = {
        '{', '}', '(', ')', '[', ']',
        ';', ',', ':', '.'
    }
    
    def __init__(self, source_code: str):
        """
        Initialize the lexer with source code.
        
        Args:
            source_code: The source code to tokenize
        """
        self.source = source_code
        self.position = 0
        self.line_number = 1
        self.current_char = self.source[0] if source_code else None
        self.tokens: List[Token] = []
    
    def advance(self) -> None:
        """Move to the next character in the source code."""
        self.position += 1
        if self.position >= len(self.source):
            self.current_char = None
        else:
            self.current_char = self.source[self.position]
            if self.current_char == '\n':
                self.line_number += 1
    
    def peek(self, offset: int = 1) -> Optional[str]:
        """
        Look ahead at the next character without advancing.
        
        Args:
            offset: How many characters ahead to look
            
        Returns:
            The character at position + offset, or None if out of bounds
        """
        peek_pos = self.position + offset
        if peek_pos < len(self.source):
            return self.source[peek_pos]
        return None
    
    def skip_whitespace(self) -> None:
        """Skip whitespace characters (except newlines in some contexts)."""
        while self.current_char is not None and self.current_char in ' \t\r\n':
            self.advance()
    
    def skip_comment(self) -> None:
        """Skip single-line comments (// style)."""
        if self.current_char == '/' and self.peek() == '/':
            # Skip until end of line
            while self.current_char is not None and self.current_char != '\n':
                self.advance()
            if self.current_char == '\n':
                self.advance()
    
    def read_number(self) -> Token:
        """
        Read a numeric literal (integer or float).
        
        Returns:
            Token representing the number
        """
        num_str = ''
        start_line = self.line_number
        has_decimal = False
        
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                if has_decimal:
                    break  # Second decimal point, stop
                has_decimal = True
            num_str += self.current_char
            self.advance()
        
        return Token(TokenType.NUMBER, num_str, start_line)
    
    def read_string(self) -> Token:
        """
        Read a string literal (enclosed in quotes).
        
        Returns:
            Token representing the string
        """
        start_line = self.line_number
        quote_char = self.current_char  # ' or "
        string_value = ''
        
        self.advance()  # Skip opening quote
        
        while self.current_char is not None and self.current_char != quote_char:
            if self.current_char == '\\':
                # Handle escape sequences
                self.advance()
                if self.current_char in ['n', 't', 'r', '\\', quote_char]:
                    escape_map = {'n': '\n', 't': '\t', 'r': '\r', '\\': '\\'}
                    string_value += escape_map.get(self.current_char, self.current_char)
                    self.advance()
            else:
                string_value += self.current_char
                self.advance()
        
        if self.current_char == quote_char:
            self.advance()  # Skip closing quote
        
        return Token(TokenType.STRING, string_value, start_line)
    
    def read_identifier(self) -> Token:
        """
        Read an identifier or keyword.
        
        Returns:
            Token representing identifier or keyword
        """
        identifier = ''
        start_line = self.line_number
        
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            identifier += self.current_char
            self.advance()
        
        # Check if it's a keyword
        if identifier in self.KEYWORDS:
            return Token(TokenType.KEYWORD, identifier, start_line)
        else:
            return Token(TokenType.IDENTIFIER, identifier, start_line)
    
    def read_operator(self) -> Token:
        """
        Read an operator (can be multi-character).
        
        Returns:
            Token representing the operator
        """
        start_line = self.line_number
        op = self.current_char
        self.advance()
        
        # Check for two-character operators
        if self.current_char is not None:
            two_char_op = op + self.current_char
            if two_char_op in self.OPERATORS:
                self.advance()
                return Token(TokenType.OPERATOR, two_char_op, start_line)
        
        return Token(TokenType.OPERATOR, op, start_line)
    
    def get_next_token(self) -> Optional[Token]:
        """
        Get the next token from the source code.
        
        Returns:
            Next Token, or None if end of file
        """
        while self.current_char is not None:
            # Skip whitespace
            if self.current_char in ' \t\r\n':
                self.skip_whitespace()
                continue
            
            # Skip comments
            if self.current_char == '/' and self.peek() == '/':
                self.skip_comment()
                continue
            
            # Numbers
            if self.current_char.isdigit():
                return self.read_number()
            
            # Strings
            if self.current_char in ['"', "'"]:
                return self.read_string()
            
            # Identifiers and keywords
            if self.current_char.isalpha() or self.current_char == '_':
                return self.read_identifier()
            
            # Delimiters
            if self.current_char in self.DELIMITERS:
                delimiter = self.current_char
                line = self.line_number
                self.advance()
                return Token(TokenType.DELIMITER, delimiter, line)
            
            # Operators
            if self.current_char in '+-*/%=!<>&|':
                return self.read_operator()
            
            # Unknown character - skip it
            self.advance()
        
        # End of file
        return Token(TokenType.EOF, '', self.line_number)
    
    def tokenize(self) -> List[Token]:
        """
        Tokenize the entire source code.
        
        Returns:
            List of all tokens
        """
        self.tokens = []
        
        while True:
            token = self.get_next_token()
            if token is None:
                break
            
            self.tokens.append(token)
            
            if token.type == TokenType.EOF:
                break
        
        return self.tokens
    
    def display_tokens(self) -> None:
        """Display all tokens in a formatted manner."""
        print("\n" + "="*60)
        print("TOKENS")
        print("="*60)
        print(f"{'Type':<15} {'Value':<20} {'Line':<6}")
        print("-"*60)
        
        for token in self.tokens:
            value_display = token.value if len(token.value) <= 20 else token.value[:17] + "..."
            print(f"{token.type.name:<15} {value_display:<20} {token.line_number:<6}")
        
        print("="*60)


if __name__ == "__main__":
    # Demo usage
    print("Lexical Analyzer - Demo")
    print("="*50)
    
    sample_code = """
    // Sample program
    int x = 10;
    float y = 3.14;
    string name = "Alice";
    
    if (x > 5) {
        x = x + 1;
    }
    """
    
    lexer = Lexer(sample_code)
    tokens = lexer.tokenize()
    
    print(f"\nSource code:\n{sample_code}")
    
    lexer.display_tokens()
    
    print(f"\nTotal tokens: {len(tokens)}")
