# 🎯 How to Demo Core Symbol Table Operations (Viva Guide)

If your teacher asks you to **demonstrate** a specific operation, use this guide!

---

## 1. 🟢 INSERT (Adding a New Symbol)
**Question**: *"Show me how you insert a variable into the table."*

**Action**: 
1. Open `examples/test_advanced.txt`.
2. Point to Line 12: `int valid_int = 10;`.
3. Run the compiler: `python compiler.py examples/test_advanced.txt`.
4. Point to the **Symbol Table** output under `Scope: global`.
5. **Show**: `valid_int | int | 12 | True | False | 10`.
6. **Explanation**: *"Sir, when the parser sees a declaration, it calls `symbol_table.insert()`. You can see 'valid_int' was successfully added to the 'global' scope."*

---

## 2. 🔍 LOOKUP (Finding a Symbol)
**Question**: *"How does the compiler find a variable when it's used later?"*

**Action**:
1. Point to Line 31: `counter = counter + 1;` in `examples/test_advanced.txt`.
2. **Explanation**: *"Sir, every time a variable is used (like 'counter' here), the Parser calls `symbol_table.lookup('counter')`. It searches from the current scope (block1) upwards to the global scope to find the matching symbol."*
3. Show in Output: The variable `counter` in the table has `Used: True`.

---

## 🔄 3. UPDATE (Modifying a Symbol)
**Question**: *"Show me an update operation where a value changes."*

**Action**:
1. Run `python compiler.py examples/test_advanced.txt`.
2. Point to the variable `counter` in the `global` scope table.
3. **Show**: The `Value` column says `counter + 1`.
4. **Explanation**: *"Initially, 'counter' was 0. After the line `counter = counter + 1;`, the Parser called `symbol_table.update()` to store the new expression or value. You can see the updated value in the table."*

---

## 🗑️ 4. DELETE (Removing a Symbol)
**Question**: *"Can you delete a variable?"*

**Action**:
1. Open `symbol_table.py` and show the `delete()` method (around line 175).
2. **Explanation**: *"Sir, we have a `delete()` method in our `SymbolTable` class. While our compiler doesn't need to delete variables during a simple compile run (as we show the final state), the functionality is there to remove a symbol from a specific scope if needed."*

---

## 🧱 5. SCOPE MANAGEMENT (Enters & Exits)
**Question**: *"Show me how you handle nested scopes (like an `if` block)."*

**Action**:
1. Run `python compiler.py examples/test_advanced.txt`.
2. **Show**: The different scope headers like `Scope: global.block1` and `Scope: global.block3.block4`.
3. **Explanation**: *"Sir, when the Parser sees a `{`, it calls `enter_scope()`. When it sees a `}`, it calls `exit_scope()`. This creates the hierarchy you see here. Variables inside `global.block3.block4` (like `deep_val`) automatically disappear when we leave that block."*

---

## 🚩 6. ERROR DETECTION (Handling Mistakes)
**Question**: *"Show me how you catch a Duplicate Declaration or an Undeclared variable."*

**Action**:
1. Run `python compiler.py examples/test_failure.txt`.
2. **Show**: The errors for `Line 18: Duplicate declaration of variable 'temperature'`.
3. **Show**: The error for `Line 27: Undeclared variable 'local_scope'`.
4. **Explanation**: *"Sir, the Symbol Table refuses to `insert()` if the name already exists in that scope. Also, `lookup()` returns None if a variable is used outside its scope, triggering our 'Undeclared' error message."*

---

## 💡 Pro-Tip for Viva
If the examiner asks you to add an error live:
1. Open `examples/test_advanced.txt`.
2. Add a line at the bottom: `undeclared_var = 100;`.
3. Run `python compiler.py examples/test_advanced.txt`.
4. The error will appear at the bottom!
