# Symbol Table Manager - Mini Compiler

**Group 6: Compiler Construction Project**  
**Course:** CSCS4573 - Compiler Construction  
**Semester:** BSCS 7th Semester

## Project Overview

This project implements a **Symbol Table Manager** as part of a mini compiler for a simple custom language. The symbol table tracks program identifiers (variables) during compilation, storing information such as name, data type, scope, and line number.

### Team Members
- [Add your team member names here]

## Features

### Core Symbol Table Operations
- ✅ **Insert**: Add new symbols with metadata
- ✅ **Lookup**: Search for symbols with scope-aware resolution
- ✅ **Update**: Modify symbol attributes
- ✅ **Delete**: Remove symbols from the table
- ✅ **Scope Management**: Hierarchical scope support (global, nested blocks)
- ✅ **Error Detection**: Duplicate declarations, undeclared variable usage

### Compiler Components
1. **Lexical Analyzer** (`lexer.py`) - Tokenizes source code
2. **Parser** (`parser.py`) - Performs syntax and semantic analysis
3. **Symbol Table** (`symbol_table.py`) - Core data structure for identifier tracking
4. **Compiler Driver** (`compiler.py`) - Main orchestration program

## Language Syntax

Our simple language supports:

```
// Variable declarations
int x = 10;
float pi = 3.14;
string name = "Alice";
bool flag = true;

// Scopes (blocks)
{
    int local_var = 20;
    x = 15;  // Update outer variable
}

// Uninitialized variables
int y;
y = 25;
```

### Supported Data Types
- `int` - Integer numbers
- `float` - Floating-point numbers
- `string` - Text strings
- `bool` - Boolean values

### Keywords
`int`, `float`, `string`, `bool`, `if`, `else`, `while`, `for`, `return`, `true`, `false`, `null`, `const`, `function`, `begin`, `end`

## Installation & Setup

### Prerequisites
- Python 3.7 or higher

### Installation
```bash
# Clone or download the project
cd mini_compiler

# No additional dependencies required - uses Python standard library only
```

## Usage

### Running the Compiler

```bash
python compiler.py <source_file>
```

### Examples

```bash
# Test basic declarations and scopes
python compiler.py examples/test_program1.txt

# Test error detection
python compiler.py examples/test_program2.txt

# Test complex nested scopes
python compiler.py examples/test_program3.txt
```

### Running Unit Tests

```bash
python test_symbol_table.py
```

## Project Structure

```
mini_compiler/
├── symbol_table.py          # Core symbol table implementation
├── lexer.py                 # Lexical analyzer (tokenizer)
├── parser.py                # Parser and semantic analyzer
├── compiler.py              # Main compiler driver
├── test_symbol_table.py     # Unit tests
├── examples/
│   ├── test_program1.txt    # Basic declarations and scopes
│   ├── test_program2.txt    # Error detection examples
│   └── test_program3.txt    # Complex nested scopes
└── README.md                # This file
```

## Symbol Table Design

### SymbolEntry Class
Represents a single symbol with attributes:
- `name`: Identifier name
- `symbol_type`: Data type (int, float, string, bool)
- `scope`: Scope where declared (e.g., "global", "global.block1")
- `line_number`: Line number of declaration
- `value`: Optional initial value
- `initialized`: Whether variable has been assigned
- `used`: Whether variable has been referenced
- `constant`: Whether symbol is constant
- `attributes`: Additional metadata

### SymbolTable Class
Main data structure with operations:

#### Insert Operation
```python
st.insert(name, symbol_type, line_number, value=None, **kwargs)
```
Adds a new symbol to the current scope. Returns `False` if symbol already exists in scope.

#### Lookup Operation
```python
st.lookup(name, scope=None)
```
Searches for a symbol using scope hierarchy (current scope → parent scopes → global).

#### Update Operation
```python
st.update(name, value=None, initialized=None, **kwargs)
```
Modifies attributes of an existing symbol.

#### Delete Operation
```python
st.delete(name, scope=None)
```
Removes a symbol from the specified scope.

#### Scope Management
```python
st.enter_scope(scope_name=None)  # Create new scope
st.exit_scope()                   # Return to parent scope
```

### Scope Hierarchy
Scopes are represented as dot-separated paths:
- `global` - Global scope
- `global.block1` - First nested block
- `global.block1.block2` - Deeper nesting

## Example Output

```
================================================================================
MINI COMPILER - Symbol Table Manager Demo
Group 6: Compiler Construction Project (CSCS4573)
================================================================================

[Phase 1: Lexical Analysis]
✓ Tokenization complete: 45 tokens generated

[Phase 2: Syntax and Semantic Analysis]
✓ Syntax and semantic analysis complete

[Phase 3: Symbol Table]
================================================================================
SYMBOL TABLE
================================================================================

Scope: global
--------------------------------------------------------------------------------
Name            Type       Line   Init   Used   Value          
--------------------------------------------------------------------------------
flag            bool       8      True   False  True           
message         string     7      True   False  Hello, Compiler!
pi              float      6      True   False  3.14159        
x               int        5      True   True   15             
y               int        24     False  False  -              
z               int        25     False  False  -              

Scope: global.block1
--------------------------------------------------------------------------------
Name            Type       Line   Init   Used   Value          
--------------------------------------------------------------------------------
local_x         int        12     True   False  20             
local_y         float      13     True   False  2.5            
================================================================================

COMPILATION STATISTICS
================================================================================
Total Tokens:        45
Total Symbols:       8
Total Scopes:        3
Initialized Vars:    6
Used Vars:           1
Unused Vars:         7
Compilation Errors:  0
================================================================================
```

## Learning Outcomes

This project demonstrates:

1. **Symbol Table Design**: Efficient data structure for identifier tracking
2. **Scope Management**: Hierarchical scope resolution
3. **Lexical Analysis**: Breaking source code into tokens
4. **Syntax Analysis**: Parsing declarations and statements
5. **Semantic Analysis**: Error detection (duplicate declarations, undeclared variables)
6. **Compiler Phases**: Integration of lexer, parser, and symbol table

## Testing

The project includes comprehensive unit tests covering:
- Symbol insertion and duplicate detection
- Lookup with scope resolution
- Update and delete operations
- Scope management and nesting
- Variable shadowing
- Statistics generation

Run tests with:
```bash
python test_symbol_table.py
```

## Error Detection Examples

The compiler detects various semantic errors:

```python
int x = 10;
int x = 20;     // ERROR: Duplicate declaration of 'x'

y = 15;         // ERROR: Undeclared variable 'y'

{
    int x = 5;  // OK: Different scope (shadows outer x)
}
```

## Future Enhancements

Potential extensions for this project:
- Function declarations and scope
- Type checking for expressions
- Constant enforcement
- Array and struct support
- Optimization warnings (unused variables)
- Symbol table serialization

## References

- Course: CSCS4573 - Compiler Construction
- Textbook: [Add your course textbook reference]
- Instructor: Tanveer Ahmed

## License

This is an academic project for educational purposes.

---

**Note**: This is a mini compiler for demonstration purposes. It implements core compiler concepts but is not a production-ready compiler.
