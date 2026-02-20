# Symbol Table Manager - Viva Guide 🎓
**Group 6: Compiler Construction Project (CSCS4573)**

This guide provides a complete overview of the project, including theoretical concepts and the specific workings of our code files.

---

## 1. Project Theory

### What is a Symbol Table?
A **Symbol Table** is a data structure used by a compiler to keep track of all **Identifiers** (variable names, function names, etc.) in the source code. It acts as a "central database" for the compiler to store and retrieve metadata about variables.

### Why do we use it?
Compilers use symbol tables to perform **Semantic Analysis**. It helps the compiler answer:
1.  **Existence**: Has this variable been declared?
2.  **Type Safety**: Is this an `int` or a `string`? Can I perform this operation on it?
3.  **Scope**: Which "version" of variable `x` am I currently using?

### How it Works (Core Operations)
- **Insert**: Adding a new variable during its declaration.
- **Lookup**: Finding a variable's details when it is used in an expression.
- **Update**: Changing the value or status of an existing variable.
- **Scope Management**: Handling variable visibility inside `{}` blocks.

---

## 2. Project Files & Workings

### 📄 `symbol_table.py` (The Heart)
This is the core of our project. It contains two main classes:
- **`SymbolEntry`**: A container that stores name, type, scope, value, and line number for a single variable.
- **`SymbolTable`**: 
    - Uses a **Nested Dictionary** to represent scopes.
    - Uses a **Scope Stack** (a list) to track the "current" scope (e.g., `['global', 'block1']`).
    - **Logic**: When looking up a variable, it searches the current scope, then recursively travels up parental scopes until it reaches `global`.

### 📄 `lexer.py` (Phase 1: Lexical Analysis)
The **Lexer** (or Scanner) reads the raw source code as a string and breaks it into **Tokens**.
- It categorizes text into `KEYWORD`, `IDENTIFIER`, `NUMBER`, `OPERATOR`, etc.
- **Benefit**: It removes whitespace and comments so the compiler can focus only on the logic.

### 📄 `parser.py` (Phase 2: Syntax & Semantic Analysis)
The **Parser** is the logic engine. It takes the tokens from the Lexer and:
1.  Verifies the **Syntax** (e.g., does every statement end with a `;`?).
2.  Performs **Advanced Semantic Analysis**:
    - **Constant Enforcement**: Blocks reassignment of `const` variables.
    - **Type Checking**: Detects mismatches like `int x = "hello"`.
    - **Array Metadata**: Manages `is_array` and `size` attributes.
3.  **Error Detection**: It checks for duplicate declarations, undeclared variables, type mismatches, and constant violations.

### 📄 `compiler.py` (The Driver)
This is the entry point of the application.
- It loads the `.txt` source file.
- It triggers the **Lexer** → then the **Parser**.
- Finally, it prints the **Symbol Table** and **Compilation Statistics** (Total symbols, errors, etc.) to the terminal.

### 📄 `test_symbol_table.py` (The Validator)
This file contains 12 **Unit Tests**.
- It tests the Symbol Table class in isolation (without the lexer or parser).
- It proves that the "Insert", "Lookup", and "Scope Shadowing" logic is 100% correct.

### 📁 `examples/` (Test Cases)
Contains sample code used to demonstrate the project:
- `test_program1.txt`: Shows basic declarations and nesting.
- `test_program2.txt`: Shows how the system catches errors.

---

## 3. The Benefits & Learning Outcomes

1.  **Conflict Resolution**: Handles multiple variables with the same name via **Hierarchical Scopes**.
2.  **Advanced Semantic Checks**: Catching Constant reassignments and Type mismatches (A+ features).
3.  **Complex Metadata**: Storing array sizes and data types in the symbol entry.
4.  **Error Detection**: Meaningful error messages for developers (Line numbers included).
5.  **Optimization**: Identifies **Unused Variables** (Dead Code) to save memory.
4.  **Efficiency**: O(1) average lookup time using Python dictionaries.

---

## 4. Final Submission Summary
- **Source Code**: Python (Modular and Clean).
- **GitHub**: All files pushed to `mirzaumerikram/symbol-table-manager`.
- **Requirements**: Group 6 objectives (Insert, Lookup, Update, Scope) are fully met.
