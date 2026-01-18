# Symbol Table Manager - Project Report

**Group 6: Compiler Construction Project**  
**Course:** CSCS4573 - Compiler Construction  
**Semester:** BSCS 7th Semester  
**Instructor:** Tanveer Ahmed

---

## Table of Contents
1. [Introduction](#introduction)
2. [Project Objectives](#project-objectives)
3. [System Architecture](#system-architecture)
4. [Phase Explanation](#phase-explanation)
5. [Language Grammar](#language-grammar)
6. [Implementation Details](#implementation-details)
7. [Sample Outputs](#sample-outputs)
8. [Testing and Verification](#testing-and-verification)
9. [Conclusion](#conclusion)

---

## 1. Introduction

This project implements a **Symbol Table Manager** as a core component of a mini compiler. The symbol table is a critical data structure in compilation that stores information about program identifiers such as variables, functions, and constants.

### What is a Symbol Table?

A symbol table is a data structure used by compilers to track identifiers in source code. For each identifier, it stores:
- **Name**: The identifier's name
- **Type**: Data type (int, float, string, bool)
- **Scope**: Where the identifier is valid
- **Line Number**: Location in source code
- **Value**: Initial or current value
- **Metadata**: Initialization status, usage tracking, etc.

### Project Scope

Our mini compiler demonstrates:
- Complete symbol table implementation with CRUD operations
- Lexical analysis (tokenization)
- Syntax analysis (parsing)
- Semantic analysis (error detection)
- Scope management with nesting support

---

## 2. Project Objectives

### Primary Objectives
1. ✅ Design and implement a symbol table data structure
2. ✅ Support insert, lookup, update, and delete operations
3. ✅ Implement hierarchical scope management
4. ✅ Detect semantic errors (duplicate declarations, undeclared variables)
5. ✅ Integrate with lexer and parser

### Learning Outcomes
- Understanding of compiler phases
- Symbol table design and implementation
- Scope resolution mechanisms
- Error detection and reporting
- Python programming for language processing

---

## 3. System Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Source Code File                     │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              Phase 1: Lexical Analyzer                  │
│                    (lexer.py)                           │
│  • Tokenization                                         │
│  • Keyword recognition                                  │
│  • Operator/delimiter identification                    │
└─────────────────────┬───────────────────────────────────┘
                      │ Tokens
                      ▼
┌─────────────────────────────────────────────────────────┐
│         Phase 2: Parser & Semantic Analyzer             │
│                    (parser.py)                          │
│  • Syntax analysis                                      │
│  • Symbol table population                              │
│  • Error detection                                      │
└─────────────────────┬───────────────────────────────────┘
                      │ Symbols
                      ▼
┌─────────────────────────────────────────────────────────┐
│              Symbol Table Manager                       │
│                (symbol_table.py)                        │
│  • Insert/Lookup/Update/Delete                          │
│  • Scope management                                     │
│  • Statistics tracking                                  │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│                   Output Display                        │
│  • Symbol table                                         │
│  • Error messages                                       │
│  • Statistics                                           │
└─────────────────────────────────────────────────────────┘
```

---

## 4. Phase Explanation

### Phase 1: Lexical Analysis (Lexer)

**Purpose:** Break source code into tokens

**Input:** Source code as text  
**Output:** List of tokens

**Token Types:**
- KEYWORD: `int`, `float`, `string`, `bool`, `if`, `while`, etc.
- IDENTIFIER: Variable names (e.g., `x`, `counter`, `name`)
- NUMBER: Numeric literals (e.g., `10`, `3.14`)
- STRING: String literals (e.g., `"Hello"`)
- OPERATOR: `+`, `-`, `*`, `/`, `=`, `==`, etc.
- DELIMITER: `{`, `}`, `(`, `)`, `;`, `,`

**Key Features:**
- Multi-character operator recognition (`==`, `!=`, `<=`, etc.)
- String escape sequence handling (`\n`, `\t`, etc.)
- Comment skipping (`//` style)
- Line number tracking for error reporting

**Example:**
```
Input:  int x = 10;
Output: [KEYWORD(int), IDENTIFIER(x), OPERATOR(=), NUMBER(10), DELIMITER(;)]
```

---

### Phase 2: Syntax and Semantic Analysis (Parser)

**Purpose:** Analyze syntax and populate symbol table

**Input:** List of tokens  
**Output:** Populated symbol table, error list

**Grammar Rules:**
```
program        → statement_list
statement_list → statement*
statement      → declaration | assignment | block
declaration    → type IDENTIFIER (= expression)? ;
assignment     → IDENTIFIER = expression ;
block          → { statement_list }
type           → int | float | string | bool
```

**Semantic Checks:**
1. **Duplicate Declaration Detection**
   - Check if variable already exists in current scope
   - Error: "Duplicate declaration of variable 'x'"

2. **Undeclared Variable Detection**
   - Check if variable exists before use
   - Error: "Undeclared variable 'y'"

3. **Scope Validation**
   - Ensure variables are accessed within valid scope
   - Support variable shadowing in nested scopes

**Example:**
```
int x = 10;     // ✓ Valid: Insert 'x' into symbol table
int x = 20;     // ✗ Error: Duplicate declaration
y = 15;         // ✗ Error: 'y' not declared
```

---

### Phase 3: Symbol Table Management

**Purpose:** Store and manage identifier information

**Data Structure:**
```python
{
    "global": {
        "x": SymbolEntry(name="x", type="int", scope="global", line=1, value=10),
        "y": SymbolEntry(name="y", type="float", scope="global", line=2)
    },
    "global.block1": {
        "local_var": SymbolEntry(name="local_var", type="int", scope="global.block1", line=5)
    }
}
```

**Operations:**

1. **Insert(name, type, line, value)**
   - Add new symbol to current scope
   - Return False if duplicate exists

2. **Lookup(name, scope)**
   - Search for symbol in current scope
   - If not found, search parent scopes
   - Return SymbolEntry or None

3. **Update(name, attributes)**
   - Modify existing symbol attributes
   - Update value, initialization status, etc.

4. **Delete(name, scope)**
   - Remove symbol from specified scope

5. **Scope Management**
   - `enter_scope()`: Create new nested scope
   - `exit_scope()`: Return to parent scope

**Scope Hierarchy:**
```
global
  ├── global.block1
  │     └── global.block1.block2
  └── global.block3
```

---

## 5. Language Grammar

### Complete Grammar Specification

```
program        → statement_list

statement_list → statement*

statement      → declaration
               | assignment
               | block

declaration    → type IDENTIFIER ;
               | type IDENTIFIER = expression ;

assignment     → IDENTIFIER = expression ;

block          → { statement_list }

expression     → term ((+ | -) term)*

term           → factor ((* | /) factor)*

factor         → NUMBER
               | STRING
               | IDENTIFIER
               | ( expression )

type           → int | float | string | bool
```

### Keywords
```
int, float, string, bool
if, else, elif, while, for
return, break, continue
true, false, null
const, function, begin, end
```

### Operators
```
Arithmetic: +, -, *, /, %
Assignment: =, +=, -=, *=, /=
Comparison: ==, !=, <, >, <=, >=
Logical: &&, ||, !
```

### Delimiters
```
{ } ( ) [ ] ; , : .
```

---

## 6. Implementation Details

### 6.1 Symbol Table Class

**Key Methods:**

```python
class SymbolTable:
    def __init__(self):
        self.table = {}              # Nested dictionary
        self.scope_stack = ["global"] # Scope hierarchy
        
    def insert(self, name, type, line, value=None):
        # Insert symbol into current scope
        # Return False if duplicate
        
    def lookup(self, name, scope=None):
        # Search current scope → parent scopes
        # Return SymbolEntry or None
        
    def update(self, name, **kwargs):
        # Modify symbol attributes
        
    def delete(self, name, scope=None):
        # Remove symbol from scope
        
    def enter_scope(self, name=None):
        # Create new nested scope
        
    def exit_scope(self):
        # Return to parent scope
```

### 6.2 Lexer Class

**Tokenization Process:**

```python
class Lexer:
    def __init__(self, source_code):
        self.source = source_code
        self.position = 0
        self.line_number = 1
        
    def tokenize(self):
        # Main tokenization loop
        while not at_end():
            skip_whitespace()
            skip_comments()
            
            if is_digit():
                token = read_number()
            elif is_alpha():
                token = read_identifier_or_keyword()
            elif is_operator():
                token = read_operator()
            elif is_delimiter():
                token = read_delimiter()
                
            tokens.append(token)
```

### 6.3 Parser Class

**Parsing Strategy:**

```python
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.symbol_table = SymbolTable()
        
    def parse_declaration(self):
        # type IDENTIFIER (= expression)? ;
        type = parse_type()
        name = expect(IDENTIFIER)
        
        if current_token == '=':
            value = parse_expression()
            
        symbol_table.insert(name, type, line, value)
        
    def parse_assignment(self):
        # IDENTIFIER = expression ;
        name = expect(IDENTIFIER)
        
        if not symbol_table.lookup(name):
            error("Undeclared variable")
            
        value = parse_expression()
        symbol_table.update(name, value=value)
```

---

## 7. Sample Outputs

### 7.1 Test Program 1: Basic Declarations

**Input (test_program1.txt):**
```
int x = 10;
float pi = 3.14159;
string message = "Hello, Compiler!";
bool flag = true;

{
    int local_x = 20;
    float local_y = 2.5;
    x = 15;
    
    {
        int inner_var = 100;
        string inner_msg = "Inner scope";
    }
}

int y = 25;
int z;
```

**Output:**
```
================================================================================
MINI COMPILER - Symbol Table Manager Demo
================================================================================

[Phase 1: Lexical Analysis]
✓ Tokenization complete: 57 tokens generated

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
flag            bool       8      True   False  true
message         string     7      True   False  Hello, Compiler!
pi              float      6      True   False  3.14159
x               int        5      True   True   15
y               int        26     True   False  25
z               int        27     False  False  -

Scope: global.block1
--------------------------------------------------------------------------------
Name            Type       Line   Init   Used   Value
--------------------------------------------------------------------------------
local_x         int        12     True   False  20
local_y         float      13     True   False  2.5

Scope: global.block1.block2
--------------------------------------------------------------------------------
Name            Type       Line   Init   Used   Value
--------------------------------------------------------------------------------
inner_msg       string     21     True   False  Inner scope
inner_var       int        20     True   False  100
================================================================================

COMPILATION STATISTICS
================================================================================
Total Tokens:        57
Total Symbols:       10
Total Scopes:        3
Initialized Vars:    9
Used Vars:           1
Unused Vars:         9
Compilation Errors:  0
================================================================================
```

---

### 7.2 Test Program 2: Error Detection

**Input (test_program2.txt):**
```
int a = 5;
float b = 2.5;

int a = 10;      // ERROR: Duplicate declaration

c = 15;          // ERROR: Undeclared variable

{
    int local_a = 100;  // OK: Different scope
    string name = "Test";
    b = 3.5;            // OK: 'b' exists in parent scope
}

result = a + b;  // ERROR: 'result' not declared

int result = 0;
result = a + b;  // OK: Now declared
```

**Output:**
```
[Phase 2: Syntax and Semantic Analysis]
ERROR: Line 9: Duplicate declaration of variable 'a'
ERROR: Line 12: Undeclared variable 'c'
ERROR: Line 24: Undeclared variable 'result'

✗ Compilation failed with 3 error(s)

COMPILATION STATISTICS
================================================================================
Total Symbols:       5
Total Scopes:        2
Compilation Errors:  3
================================================================================
```

---

### 7.3 Unit Test Results

**Test Execution:**
```
======================================================================
SYMBOL TABLE MANAGER - UNIT TESTS
======================================================================
test_insert_symbol ............................ ok
test_duplicate_declaration .................... ok
test_lookup_symbol ............................ ok
test_update_symbol ............................ ok
test_delete_symbol ............................ ok
test_scope_management ......................... ok
test_scope_shadowing .......................... ok
test_nested_scopes ............................ ok
test_get_symbols_in_scope ..................... ok
test_statistics ............................... ok
test_symbol_entry_creation .................... ok
test_symbol_entry_string_representation ....... ok

----------------------------------------------------------------------
Ran 12 tests in 1.013s

OK

======================================================================
TEST SUMMARY
======================================================================
Tests run: 12
Successes: 12
Failures: 0
Errors: 0
======================================================================
```

---

## 8. Testing and Verification

### 8.1 Unit Testing

**Test Coverage:**
- ✅ Symbol insertion with duplicate detection
- ✅ Lookup with scope resolution
- ✅ Update operations
- ✅ Delete operations
- ✅ Scope management (enter/exit)
- ✅ Variable shadowing
- ✅ Nested scopes (3+ levels)
- ✅ Statistics generation

**Test Results:** 12/12 tests passed (100% success rate)

### 8.2 Integration Testing

**Test Programs:**
1. **test_program1.txt** - Basic declarations and scopes
2. **test_program2.txt** - Error detection scenarios
3. **test_program3.txt** - Complex nested scopes

**Results:**
- All test programs compiled successfully
- Error detection working correctly
- Scope hierarchy properly maintained
- Symbol table accurately populated

### 8.3 Error Handling

**Detected Errors:**
- Duplicate variable declarations
- Undeclared variable usage
- Scope violations

**Error Reporting:**
- Line number tracking
- Descriptive error messages
- Batch error collection

---

## 9. Conclusion

### Project Achievements

✅ **Complete Implementation**
- Fully functional symbol table with all required operations
- Integrated lexer, parser, and semantic analyzer
- Comprehensive error detection and reporting

✅ **Quality Assurance**
- 100% unit test pass rate (12/12 tests)
- Multiple integration test scenarios
- Well-documented, clean code

✅ **Learning Outcomes**
- Deep understanding of symbol table design
- Practical experience with compiler phases
- Scope management implementation
- Error detection techniques

### Key Features

1. **Efficient Data Structure** - O(1) average lookup time
2. **Hierarchical Scopes** - Support for unlimited nesting
3. **Variable Shadowing** - Proper scope resolution
4. **Error Detection** - Meaningful error messages
5. **Statistics Tracking** - Compilation metrics
6. **Extensible Design** - Easy to add new features

### Future Enhancements

Potential extensions:
- Function declarations with parameters
- Type checking for expressions
- Array and struct support
- Intermediate code generation
- Optimization warnings
- Symbol table serialization

### Final Notes

This project successfully demonstrates all core concepts of symbol table management in compiler construction. The implementation is clean, well-tested, and suitable for academic presentation.

**Project Status:** ✅ Complete and ready for submission

---

**GitHub Repository:** https://github.com/mirzaumerikram/symbol-table-manager

**Team:** Group 6  
**Course:** CSCS4573 - Compiler Construction  
**Instructor:** Tanveer Ahmed
