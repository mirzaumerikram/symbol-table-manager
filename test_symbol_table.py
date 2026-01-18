"""
Unit Tests for Symbol Table Manager
Group 6: Compiler Construction Project
Course: CSCS4573

This module contains unit tests for the symbol table operations.
"""

import unittest
from symbol_table import SymbolTable, SymbolEntry


class TestSymbolTable(unittest.TestCase):
    """Test cases for Symbol Table operations."""
    
    def setUp(self):
        """Set up a fresh symbol table for each test."""
        self.st = SymbolTable()
    
    def test_insert_symbol(self):
        """Test inserting a symbol into the table."""
        result = self.st.insert("x", "int", 1, value=10)
        self.assertTrue(result)
        
        # Verify symbol exists
        symbol = self.st.lookup("x")
        self.assertIsNotNone(symbol)
        self.assertEqual(symbol.name, "x")
        self.assertEqual(symbol.symbol_type, "int")
        self.assertEqual(symbol.value, 10)
    
    def test_duplicate_declaration(self):
        """Test that duplicate declarations are rejected."""
        self.st.insert("x", "int", 1)
        result = self.st.insert("x", "float", 2)
        self.assertFalse(result)
    
    def test_lookup_symbol(self):
        """Test looking up symbols."""
        self.st.insert("x", "int", 1, value=10)
        self.st.insert("y", "float", 2, value=3.14)
        
        symbol_x = self.st.lookup("x")
        self.assertIsNotNone(symbol_x)
        self.assertEqual(symbol_x.name, "x")
        
        symbol_y = self.st.lookup("y")
        self.assertIsNotNone(symbol_y)
        self.assertEqual(symbol_y.name, "y")
        
        # Non-existent symbol
        symbol_z = self.st.lookup("z")
        self.assertIsNone(symbol_z)
    
    def test_update_symbol(self):
        """Test updating symbol attributes."""
        self.st.insert("x", "int", 1)
        
        # Update value
        result = self.st.update("x", value=20, initialized=True)
        self.assertTrue(result)
        
        symbol = self.st.lookup("x")
        self.assertEqual(symbol.value, 20)
        self.assertTrue(symbol.initialized)
    
    def test_delete_symbol(self):
        """Test deleting symbols."""
        self.st.insert("x", "int", 1)
        
        # Verify exists
        self.assertIsNotNone(self.st.lookup("x"))
        
        # Delete
        result = self.st.delete("x")
        self.assertTrue(result)
        
        # Verify deleted
        self.assertIsNone(self.st.lookup("x"))
    
    def test_scope_management(self):
        """Test entering and exiting scopes."""
        # Global scope
        self.st.insert("global_var", "int", 1)
        
        # Enter new scope
        self.st.enter_scope("function1")
        self.st.insert("local_var", "int", 2)
        
        # Both should be accessible
        self.assertIsNotNone(self.st.lookup("global_var"))
        self.assertIsNotNone(self.st.lookup("local_var"))
        
        # Exit scope
        self.st.exit_scope()
        
        # Only global should be accessible
        self.assertIsNotNone(self.st.lookup("global_var"))
        self.assertIsNone(self.st.lookup("local_var"))
    
    def test_scope_shadowing(self):
        """Test variable shadowing in nested scopes."""
        # Global x
        self.st.insert("x", "int", 1, value=10)
        
        # Enter scope and shadow x
        self.st.enter_scope("block1")
        self.st.insert("x", "float", 2, value=3.14)
        
        # Should find local x
        symbol = self.st.lookup("x")
        self.assertEqual(symbol.symbol_type, "float")
        self.assertEqual(symbol.value, 3.14)
        
        # Exit scope
        self.st.exit_scope()
        
        # Should find global x
        symbol = self.st.lookup("x")
        self.assertEqual(symbol.symbol_type, "int")
        self.assertEqual(symbol.value, 10)
    
    def test_nested_scopes(self):
        """Test multiple levels of nested scopes."""
        self.st.insert("global_var", "int", 1)
        
        self.st.enter_scope("level1")
        self.st.insert("level1_var", "int", 2)
        
        self.st.enter_scope("level2")
        self.st.insert("level2_var", "int", 3)
        
        # All should be accessible
        self.assertIsNotNone(self.st.lookup("global_var"))
        self.assertIsNotNone(self.st.lookup("level1_var"))
        self.assertIsNotNone(self.st.lookup("level2_var"))
        
        # Exit to level1
        self.st.exit_scope()
        self.assertIsNotNone(self.st.lookup("global_var"))
        self.assertIsNotNone(self.st.lookup("level1_var"))
        self.assertIsNone(self.st.lookup("level2_var"))
        
        # Exit to global
        self.st.exit_scope()
        self.assertIsNotNone(self.st.lookup("global_var"))
        self.assertIsNone(self.st.lookup("level1_var"))
    
    def test_get_symbols_in_scope(self):
        """Test retrieving all symbols in a scope."""
        self.st.insert("x", "int", 1)
        self.st.insert("y", "float", 2)
        
        symbols = self.st.get_symbols_in_scope("global")
        self.assertEqual(len(symbols), 2)
        
        self.st.enter_scope("block1")
        self.st.insert("local_var", "int", 3)
        
        symbols = self.st.get_symbols_in_scope()
        self.assertEqual(len(symbols), 1)
    
    def test_statistics(self):
        """Test symbol table statistics."""
        self.st.insert("x", "int", 1, value=10)
        self.st.insert("y", "float", 2)
        self.st.insert("z", "string", 3, value="test")
        
        # Mark one as used
        self.st.lookup("x")
        
        stats = self.st.get_statistics()
        self.assertEqual(stats['total_symbols'], 3)
        self.assertEqual(stats['total_scopes'], 1)
        self.assertEqual(stats['initialized'], 2)
        self.assertEqual(stats['used'], 1)
        self.assertEqual(stats['unused'], 2)


class TestSymbolEntry(unittest.TestCase):
    """Test cases for SymbolEntry class."""
    
    def test_symbol_entry_creation(self):
        """Test creating a symbol entry."""
        entry = SymbolEntry(
            name="x",
            symbol_type="int",
            scope="global",
            line_number=1,
            value=10,
            initialized=True
        )
        
        self.assertEqual(entry.name, "x")
        self.assertEqual(entry.symbol_type, "int")
        self.assertEqual(entry.scope, "global")
        self.assertEqual(entry.line_number, 1)
        self.assertEqual(entry.value, 10)
        self.assertTrue(entry.initialized)
        self.assertFalse(entry.used)
        self.assertFalse(entry.constant)
    
    def test_symbol_entry_string_representation(self):
        """Test string representation of symbol entry."""
        entry = SymbolEntry("x", "int", "global", 1)
        str_repr = str(entry)
        
        self.assertIn("x", str_repr)
        self.assertIn("int", str_repr)
        self.assertIn("global", str_repr)


def run_tests():
    """Run all tests and display results."""
    print("\n" + "="*70)
    print("SYMBOL TABLE MANAGER - UNIT TESTS")
    print("="*70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestSymbolTable))
    suite.addTests(loader.loadTestsFromTestCase(TestSymbolEntry))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
