"""
Symbol Table Manager - Core Module
Group 6: Compiler Construction Project
Course: CSCS4573

This module implements the Symbol Table data structure for tracking
program identifiers during compilation.
"""

from typing import Optional, Dict, List, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class SymbolEntry:
    """
    Represents a single entry in the symbol table.
    
    Attributes:
        name: Identifier name
        symbol_type: Data type (int, float, string, bool, etc.)
        scope: Scope where the symbol is defined
        line_number: Line number where symbol is declared
        value: Optional initial value
        initialized: Whether the variable has been assigned a value
        used: Whether the variable has been referenced
        constant: Whether the symbol is a constant
        attributes: Additional metadata
    """
    name: str
    symbol_type: str
    scope: str
    line_number: int
    value: Optional[Any] = None
    initialized: bool = False
    used: bool = False
    constant: bool = False
    attributes: Dict[str, Any] = field(default_factory=dict)
    
    def __str__(self) -> str:
        """String representation of symbol entry."""
        return (f"Symbol(name='{self.name}', type='{self.symbol_type}', "
                f"scope='{self.scope}', line={self.line_number})")


class SymbolTable:
    """
    Symbol Table Manager for tracking program identifiers.
    
    Features:
    - Insert, lookup, update, delete operations
    - Hierarchical scope management
    - Duplicate declaration detection
    - Scope-aware symbol resolution
    """
    
    def __init__(self):
        """Initialize an empty symbol table."""
        self.table: Dict[str, Dict[str, SymbolEntry]] = {}
        self.current_scope: str = "global"
        self.scope_stack: List[str] = ["global"]
        self.scope_counter: int = 0
        
    def _get_full_scope_path(self) -> str:
        """Get the current full scope path (e.g., 'global.function1.block1')."""
        return ".".join(self.scope_stack)
    
    def insert(self, name: str, symbol_type: str, line_number: int, 
               value: Optional[Any] = None, **kwargs) -> bool:
        """
        Insert a new symbol into the table.
        
        Args:
            name: Identifier name
            symbol_type: Data type of the symbol
            line_number: Line number where declared
            value: Optional initial value
            **kwargs: Additional attributes (initialized, constant, etc.)
            
        Returns:
            True if insertion successful, False if symbol already exists in current scope
        """
        scope = self._get_full_scope_path()
        
        # Check for duplicate declaration in current scope
        if scope in self.table and name in self.table[scope]:
            return False
        
        # Create scope entry if it doesn't exist
        if scope not in self.table:
            self.table[scope] = {}
        
        # Create symbol entry
        initialized = kwargs.get('initialized', value is not None)
        constant = kwargs.get('constant', False)
        
        symbol = SymbolEntry(
            name=name,
            symbol_type=symbol_type,
            scope=scope,
            line_number=line_number,
            value=value,
            initialized=initialized,
            constant=constant,
            attributes=kwargs.get('attributes', {})
        )
        
        self.table[scope][name] = symbol
        return True
    
    def lookup(self, name: str, scope: Optional[str] = None) -> Optional[SymbolEntry]:
        """
        Look up a symbol in the table.
        
        Performs scope-aware lookup: searches current scope first,
        then parent scopes up to global.
        
        Args:
            name: Identifier name to search for
            scope: Optional specific scope to search (defaults to current scope)
            
        Returns:
            SymbolEntry if found, None otherwise
        """
        if scope is not None:
            # Search specific scope only
            if scope in self.table and name in self.table[scope]:
                return self.table[scope][name]
            return None
        
        # Search current scope and parent scopes
        scopes_to_search = []
        for i in range(len(self.scope_stack), 0, -1):
            scope_path = ".".join(self.scope_stack[:i])
            scopes_to_search.append(scope_path)
        
        for scope_path in scopes_to_search:
            if scope_path in self.table and name in self.table[scope_path]:
                symbol = self.table[scope_path][name]
                # Mark as used
                symbol.used = True
                return symbol
        
        return None
    
    def update(self, name: str, **kwargs) -> bool:
        """
        Update an existing symbol's attributes.
        
        Args:
            name: Identifier name
            **kwargs: Attributes to update (value, initialized, used, etc.)
            
        Returns:
            True if update successful, False if symbol not found
        """
        symbol = self.lookup(name)
        if symbol is None:
            return False
        
        # Update attributes
        if 'value' in kwargs:
            symbol.value = kwargs['value']
        if 'initialized' in kwargs:
            symbol.initialized = kwargs['initialized']
        if 'used' in kwargs:
            symbol.used = kwargs['used']
        if 'constant' in kwargs:
            symbol.constant = kwargs['constant']
        if 'attributes' in kwargs:
            symbol.attributes.update(kwargs['attributes'])
        
        return True
    
    def delete(self, name: str, scope: Optional[str] = None) -> bool:
        """
        Delete a symbol from the table.
        
        Args:
            name: Identifier name
            scope: Optional specific scope (defaults to current scope)
            
        Returns:
            True if deletion successful, False if symbol not found
        """
        target_scope = scope if scope is not None else self._get_full_scope_path()
        
        if target_scope in self.table and name in self.table[target_scope]:
            del self.table[target_scope][name]
            return True
        
        return False
    
    def enter_scope(self, scope_name: Optional[str] = None) -> str:
        """
        Enter a new scope level.
        
        Args:
            scope_name: Optional name for the scope (auto-generated if not provided)
            
        Returns:
            The full path of the new scope
        """
        if scope_name is None:
            self.scope_counter += 1
            scope_name = f"block{self.scope_counter}"
        
        self.scope_stack.append(scope_name)
        new_scope = self._get_full_scope_path()
        
        if new_scope not in self.table:
            self.table[new_scope] = {}
        
        return new_scope
    
    def exit_scope(self) -> Optional[str]:
        """
        Exit the current scope and return to parent scope.
        
        Returns:
            The scope that was exited, or None if already at global scope
        """
        if len(self.scope_stack) <= 1:
            return None  # Can't exit global scope
        
        exited_scope = self.scope_stack.pop()
        return exited_scope
    
    def get_symbols_in_scope(self, scope: Optional[str] = None) -> List[SymbolEntry]:
        """
        Get all symbols in a specific scope.
        
        Args:
            scope: Scope to retrieve symbols from (defaults to current scope)
            
        Returns:
            List of SymbolEntry objects in the scope
        """
        target_scope = scope if scope is not None else self._get_full_scope_path()
        
        if target_scope in self.table:
            return list(self.table[target_scope].values())
        
        return []
    
    def get_all_symbols(self) -> List[SymbolEntry]:
        """
        Get all symbols from all scopes.
        
        Returns:
            List of all SymbolEntry objects
        """
        all_symbols = []
        for scope_symbols in self.table.values():
            all_symbols.extend(scope_symbols.values())
        return all_symbols
    
    def display(self, show_unused: bool = True) -> None:
        """
        Display the symbol table in a formatted manner.
        
        Args:
            show_unused: Whether to show unused variables
        """
        print("\n" + "="*80)
        print("SYMBOL TABLE")
        print("="*80)
        
        if not self.table:
            print("(empty)")
            return
        
        # Sort scopes for consistent display
        sorted_scopes = sorted(self.table.keys())
        
        for scope in sorted_scopes:
            symbols = self.table[scope]
            if not symbols:
                continue
            
            print(f"\nScope: {scope}")
            print("-" * 80)
            print(f"{'Name':<15} {'Type':<10} {'Line':<6} {'Init':<6} {'Used':<6} {'Value':<15}")
            print("-" * 80)
            
            for name in sorted(symbols.keys()):
                symbol = symbols[name]
                
                if not show_unused and not symbol.used:
                    continue
                
                value_str = str(symbol.value) if symbol.value is not None else "-"
                if len(value_str) > 15:
                    value_str = value_str[:12] + "..."
                
                print(f"{symbol.name:<15} {symbol.symbol_type:<10} "
                      f"{symbol.line_number:<6} {str(symbol.initialized):<6} "
                      f"{str(symbol.used):<6} {value_str:<15}")
        
        print("="*80)
    
    def get_statistics(self) -> Dict[str, int]:
        """
        Get statistics about the symbol table.
        
        Returns:
            Dictionary with statistics (total symbols, scopes, etc.)
        """
        total_symbols = sum(len(symbols) for symbols in self.table.values())
        initialized_count = sum(
            1 for symbols in self.table.values() 
            for symbol in symbols.values() 
            if symbol.initialized
        )
        used_count = sum(
            1 for symbols in self.table.values() 
            for symbol in symbols.values() 
            if symbol.used
        )
        
        return {
            'total_symbols': total_symbols,
            'total_scopes': len(self.table),
            'initialized': initialized_count,
            'used': used_count,
            'unused': total_symbols - used_count
        }
    
    def __str__(self) -> str:
        """String representation of the symbol table."""
        stats = self.get_statistics()
        return (f"SymbolTable(symbols={stats['total_symbols']}, "
                f"scopes={stats['total_scopes']})")


if __name__ == "__main__":
    # Demo usage
    print("Symbol Table Manager - Demo")
    print("="*50)
    
    st = SymbolTable()
    
    # Insert some symbols
    st.insert("x", "int", 1, value=10)
    st.insert("y", "float", 2)
    st.insert("name", "string", 3, value="John")
    
    # Enter a new scope
    st.enter_scope("function1")
    st.insert("local_var", "int", 5, value=20)
    st.insert("x", "float", 6)  # Shadow global x
    
    # Lookup
    symbol = st.lookup("x")
    print(f"\nLookup 'x' in current scope: {symbol}")
    
    # Exit scope
    st.exit_scope()
    symbol = st.lookup("x")
    print(f"Lookup 'x' after exiting scope: {symbol}")
    
    # Display table
    st.display()
    
    # Statistics
    print(f"\nStatistics: {st.get_statistics()}")
