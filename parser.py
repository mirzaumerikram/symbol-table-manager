"""
Parser and Semantic Analyzer - Mini Compiler
Group 6: Compiler Construction Project
Course: CSCS4573

This module implements the parser that analyzes syntax and populates
the symbol table with semantic information.
"""

from typing import List, Optional
from lexer import Token, TokenType, Lexer
from symbol_table import SymbolTable


class ParseError(Exception):
    """Exception raised for parsing errors."""
    pass


class Parser:
    """
    Parser for analyzing syntax and performing semantic analysis.
    
    Grammar (simplified):
    program -> statement_list
    statement_list -> statement*
    statement -> declaration | assignment | block | comment
    declaration -> type IDENTIFIER (= expression)? ;
    assignment -> IDENTIFIER = expression ;
    block -> { statement_list }
    expression -> term ((+|-) term)*
    term -> factor ((*|/) factor)*
    factor -> NUMBER | STRING | IDENTIFIER | (expression)
    """
    
    def __init__(self, tokens: List[Token]):
        """
        Initialize the parser with a list of tokens.
        
        Args:
            tokens: List of tokens from the lexer
        """
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[0] if tokens else None
        self.symbol_table = SymbolTable()
        self.errors: List[str] = []
    
    def advance(self) -> None:
        """Move to the next token."""
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = None
    
    def peek(self, offset: int = 1) -> Optional[Token]:
        """
        Look ahead at the next token without advancing.
        
        Args:
            offset: How many tokens ahead to look
            
        Returns:
            The token at position + offset, or None if out of bounds
        """
        peek_pos = self.position + offset
        if peek_pos < len(self.tokens):
            return self.tokens[peek_pos]
        return None
    
    def expect(self, token_type: TokenType, value: Optional[str] = None) -> bool:
        """
        Check if current token matches expected type and optionally value.
        
        Args:
            token_type: Expected token type
            value: Optional expected value
            
        Returns:
            True if matches, False otherwise
        """
        if self.current_token is None:
            return False
        
        if self.current_token.type != token_type:
            return False
        
        if value is not None and self.current_token.value != value:
            return False
        
        return True
    
    def error(self, message: str) -> None:
        """
        Record a parsing error.
        
        Args:
            message: Error message
        """
        line = self.current_token.line_number if self.current_token else "EOF"
        error_msg = f"Line {line}: {message}"
        self.errors.append(error_msg)
        print(f"ERROR: {error_msg}")
    
    def parse_type(self) -> Optional[str]:
        """
        Parse a type keyword (int, float, string, bool).
        
        Returns:
            Type name if valid, None otherwise
        """
        if self.expect(TokenType.KEYWORD) and self.current_token.value in ['int', 'float', 'string', 'bool']:
            type_name = self.current_token.value
            self.advance()
            return type_name
        return None
    
    def parse_expression(self) -> Optional[str]:
        """
        Parse an expression (simplified - just returns string representation).
        
        Returns:
            Expression value as string, or None if error
        """
        # For simplicity, we'll just capture the expression tokens until semicolon or delimiter
        expr_tokens = []
        
        while self.current_token and not (
            self.expect(TokenType.DELIMITER, ';') or 
            self.expect(TokenType.DELIMITER, ',') or
            self.expect(TokenType.DELIMITER, ')')
        ):
            expr_tokens.append(self.current_token.value)
            self.advance()
        
        return ' '.join(expr_tokens) if expr_tokens else None
    
    def parse_declaration(self) -> bool:
        """
        Parse a variable declaration.
        
        Grammar: type IDENTIFIER (= expression)? ;
        
        Returns:
            True if successfully parsed, False otherwise
        """
        # Get type
        var_type = self.parse_type()
        if not var_type:
            return False
        
        # Get identifier
        if not self.expect(TokenType.IDENTIFIER):
            self.error(f"Expected identifier after type '{var_type}'")
            return False
        
        var_name = self.current_token.value
        line_number = self.current_token.line_number
        self.advance()
        
        # Check for initialization
        value = None
        initialized = False
        
        if self.expect(TokenType.OPERATOR, '='):
            self.advance()  # Skip '='
            value = self.parse_expression()
            initialized = True
        
        # Expect semicolon
        if not self.expect(TokenType.DELIMITER, ';'):
            self.error(f"Expected ';' after declaration of '{var_name}'")
            return False
        
        self.advance()  # Skip ';'
        
        # Insert into symbol table
        if not self.symbol_table.insert(var_name, var_type, line_number, value=value, initialized=initialized):
            self.error(f"Duplicate declaration of variable '{var_name}'")
            return False
        
        return True
    
    def parse_assignment(self) -> bool:
        """
        Parse an assignment statement.
        
        Grammar: IDENTIFIER = expression ;
        
        Returns:
            True if successfully parsed, False otherwise
        """
        var_name = self.current_token.value
        line_number = self.current_token.line_number
        self.advance()  # Skip identifier
        
        # Check if variable is declared
        symbol = self.symbol_table.lookup(var_name)
        if symbol is None:
            self.error(f"Undeclared variable '{var_name}'")
            return False
        
        # Expect '='
        if not self.expect(TokenType.OPERATOR, '='):
            self.error(f"Expected '=' in assignment")
            return False
        
        self.advance()  # Skip '='
        
        # Parse expression
        value = self.parse_expression()
        
        # Expect semicolon
        if not self.expect(TokenType.DELIMITER, ';'):
            self.error(f"Expected ';' after assignment")
            return False
        
        self.advance()  # Skip ';'
        
        # Update symbol table
        self.symbol_table.update(var_name, value=value, initialized=True)
        
        return True
    
    def parse_block(self) -> bool:
        """
        Parse a block statement (scope).
        
        Grammar: { statement_list }
        
        Returns:
            True if successfully parsed, False otherwise
        """
        if not self.expect(TokenType.DELIMITER, '{'):
            return False
        
        self.advance()  # Skip '{'
        
        # Enter new scope
        self.symbol_table.enter_scope()
        
        # Parse statements in block
        while self.current_token and not self.expect(TokenType.DELIMITER, '}'):
            self.parse_statement()
        
        # Expect '}'
        if not self.expect(TokenType.DELIMITER, '}'):
            self.error("Expected '}' to close block")
            return False
        
        self.advance()  # Skip '}'
        
        # Exit scope
        self.symbol_table.exit_scope()
        
        return True
    
    def parse_statement(self) -> bool:
        """
        Parse a single statement.
        
        Returns:
            True if successfully parsed, False otherwise
        """
        if self.current_token is None or self.expect(TokenType.EOF):
            return False
        
        # Declaration (starts with type keyword)
        if self.expect(TokenType.KEYWORD) and self.current_token.value in ['int', 'float', 'string', 'bool']:
            return self.parse_declaration()
        
        # Block
        if self.expect(TokenType.DELIMITER, '{'):
            return self.parse_block()
        
        # Assignment (starts with identifier)
        if self.expect(TokenType.IDENTIFIER):
            return self.parse_assignment()
        
        # Skip unknown tokens
        self.advance()
        return False
    
    def parse(self) -> SymbolTable:
        """
        Parse the entire program.
        
        Returns:
            The populated symbol table
        """
        print("\n" + "="*60)
        print("PARSING")
        print("="*60)
        
        while self.current_token and not self.expect(TokenType.EOF):
            self.parse_statement()
        
        if self.errors:
            print(f"\nParsing completed with {len(self.errors)} error(s)")
        else:
            print("\nParsing completed successfully!")
        
        return self.symbol_table
    
    def get_errors(self) -> List[str]:
        """
        Get all parsing errors.
        
        Returns:
            List of error messages
        """
        return self.errors


if __name__ == "__main__":
    # Demo usage
    print("Parser and Semantic Analyzer - Demo")
    print("="*50)
    
    sample_code = """
    int x = 10;
    float y = 3.14;
    string name = "Alice";
    
    {
        int local_var = 20;
        x = 15;  // Update global variable
    }
    
    int z;  // Uninitialized
    z = x + 5;
    """
    
    print(f"Source code:\n{sample_code}\n")
    
    # Tokenize
    lexer = Lexer(sample_code)
    tokens = lexer.tokenize()
    
    # Parse
    parser = Parser(tokens)
    symbol_table = parser.parse()
    
    # Display symbol table
    symbol_table.display()
    
    # Display statistics
    stats = symbol_table.get_statistics()
    print(f"\nStatistics:")
    print(f"  Total symbols: {stats['total_symbols']}")
    print(f"  Total scopes: {stats['total_scopes']}")
    print(f"  Initialized: {stats['initialized']}")
    print(f"  Used: {stats['used']}")
    print(f"  Unused: {stats['unused']}")
