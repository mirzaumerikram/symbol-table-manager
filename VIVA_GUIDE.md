# 🎓 Ultimate 100% Complete Viva Guide: Symbol Table Manager

This is your master script for a perfect viva. It covers **every file**, the **logic flow**, and **operational instructions**.

---

## 📂 1. File-by-File Technical Deep Dive

### 📄 `symbol_table.py` (The Core Engine)
**Logic**: Manages memory representation of identifiers.
- **`SymbolEntry`**: A data object storing `name`, `type`, `scope`, `line`, `value`, and **A+ Metadata** (`constant`, `is_array`).
- **`scope_stack`**: A LIFO list (e.g., `['global', 'global.block1']`) tracking the current active context.
- **`lookup()`**: Iterates through the `scope_stack` from top to bottom. This ensures **Variable Shadowing** (finding the nearest local variable first).
- **`update()`**: Acts as a **Logic Guard**. If a symbol is marked `constant`, it returns `False`, effectively blocking illegal reassignments.

### 📄 `lexer.py` (Phase 1: Lexical Analysis)
**Logic**: Converts raw text into a stream of logical "Tokens".
- **`tokenize()`**: Scans text character-by-character.
- **Greedy Matching**: Correctly handles multi-char sequences (e.g., `==` isn't two `=` tokens, but one `EQUALS` token).
- **Line Tracking**: Crucial for the Parser to point to the exact line of a mistake.

### 📄 `parser.py` (Phase 2 & 3: Syntax & Semantics)
**Logic**: A **Recursive Descent Parser** that enforces our EBNF grammar.
- **`parse_declaration()`**: Extracts metadata. If it sees `const`, it tells the Symbol Table to protect this variable.
- **`_infer_type()`**: Determines types for `int`, `float`, `string`, and `bool` literals and compares them with the target variable's type.
- **`parse_block()`**: Automatically handles `enter_scope()` and `exit_scope()`, managing the lifecycle of block-local variables.

### 📄 `compiler.py` (The Driver)
**Logic**: Coordinates the entire pipeline. It takes a file path, feeds it to the Lexer, passes tokens to the Parser, and finally prints the Symbol Table.

---

## 🔄 2. The Complete Code Flow (Demo Script)
Explain this sequence to the examiner:

1.  **Read**: Source code is read (e.g., `const int x = 10;`).
2.  **Lex**: Lexer breaks it into distinct tokens.
3.  **Parse**: Parser recognizes a "Declaration" rule.
4.  **Semantic Check**:
    - Parser calls **`SymbolTable.insert`**.
    - If duplicate, it returns `False` -> Error Reported.
    - If `const` is present, the entry is flagged as immutable.
5.  **Display**: The final state of memory is printed for the user to see.

---

## 🛠️ 3. How to Create and Test New Files (Operational Guide)
If the examiner asks you to demo a custom scenario:

1.  **Create a New File**:
    In your IDE, right-click the `examples` folder and create `demo.txt`.
2.  **Write Test Code**:
    ```cpp
    int my_val = 50;
    const float RATE = 0.05;
    {
        string local_msg = "Hello";
        my_val = 100;
    }
    ```
3.  **Run Compilation**:
    ```powershell
    python compiler.py examples/demo.txt
    ```
4.  **Point to Results**:
    - Show the **Value Change** of `my_val` in the table.
    - Show the **Scope Column** for `local_msg` (it should be `global.block1`).

---

## ❓ 4. Advanced Viva Q&A (A+ Level)

**Q: How did you implement Type Checking?**
> **A**: We built an inference engine (`_infer_type`) in `parser.py`. It looks at the value (e.g., does it have quotes? is it numeric?) and compares it against the declared type in the symbol table. It even allows "Promotion" (assigning an `int` to a `float`).

**Q: How does the compiler know a variable is "Constant"?**
> **A**: Every `SymbolEntry` has a `constant` attribute. The `Parser` sets this during declaration. If an assignment happens later, the Symbol Table's `update()` method detects this flag and denies the operation.

**Q: How do you handle deep nesting (e.g., a block inside a block)?**
> **A**: Our `scope_stack` uses a dot-notation (e.g., `global.block1.block2`). This ensures that symbols are uniquely stored in their specific nested context while remaining accessible to deeper children.

**Q: What happens if an error is found?**
> **A**: The compiler doesn't crash. It "collects" the error message with the line number and continues parsing. After the parse is complete, it prints all found errors in a batch so the developer can fix them all at once.

---

## 🏆 Final Summary
Your project is an **Integrated Front-End Compiler**. It performs **Lexing**, **Parsing**, and **Active Semantic Defense (Constants, Types, Scopes)**. It uses O(1) hashing for performance and LIFO stacks for scope resolution.
