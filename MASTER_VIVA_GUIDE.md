# 📘 MASTER VIVA GUIDE - Symbol Table Manager (Read This Before Your Viva!)

**Course:** CSCS4573 – Compiler Construction | **Group 6** | **Language: Python**

> This guide explains **everything** in simple words. No confusing terms. Read it once and you will be able to answer every question.

---

# 🧠 PART 1: WHAT IS THIS PROJECT? (The Big Picture)

## Think of it like a Post Office

When you write a letter and send it, the post office:
1. **Reads your address** (Lexical Analysis)
2. **Checks if your format is correct** (Syntax Analysis)
3. **Understands the meaning and delivers it** (Semantic Analysis)
4. **Keeps a record** (Symbol Table)

Your project (a **Mini Compiler**) does the exact same thing, but for **code** instead of letters.

---

## What is a Compiler?

A **Compiler** converts code written by humans (like `int x = 10;`) into something a computer understands.

Your project builds the **first 3 phases** of this process:
1. **Lexical Phase** → Break code into small pieces (tokens)
2. **Syntax Phase** → Check if the code is written correctly (grammar)
3. **Semantic Phase** → Check if the code *makes sense* (logic)

---

# 📁 PART 2: THE FILES (Your Project's Blueprint)

Your project has **5 key files**. Think of each file as a worker in a factory:

```
mini_compiler/
│
├── compiler.py        ← The BOSS (runs everything)
├── lexer.py           ← The SCANNER (reads words)
├── parser.py          ← The BRAIN (checks grammar + logic)
├── symbol_table.py    ← The MEMORY (stores all variables)
└── examples/          ← Test programs (like test subjects)
```

---

## File 1: `compiler.py` — The Manager
**What it does:** This is the file you actually **run**. It is the starting point.

**How it works:**
1. It reads the source code file you give it
2. Sends the code to the **Lexer**
3. Sends the tokens to the **Parser**
4. Displays the final **Symbol Table**

**In plain English:** It's like the **manager** who tells workers what to do. It does not do the work itself, it coordinates.

**How to run it:**
```powershell
python compiler.py examples/test_advanced.txt
```

---

## File 2: `lexer.py` — The Scanner (Phase 1: Lexical Analysis)

### What is Lexical Analysis? (In Simple Words)
Imagine you are reading a sentence: `"The cat sat on the mat."`

You automatically **identify each word** separately. That is what the Lexer does with code.

**Example:**
```
Input:  int x = 10;
Output: [int] [x] [=] [10] [;]
        KEYWORD IDENTIFIER OPERATOR NUMBER DELIMITER
```

The Lexer breaks the code into **Tokens**. A Token is just a labeled piece of text.

### Token Types in Your Project:
| Token Type | Example | What it means |
|---|---|---|
| **KEYWORD** | `int`, `float`, `const`, `if` | Reserved words |
| **IDENTIFIER** | `x`, `counter`, `myVariable` | Variable names |
| **NUMBER** | `10`, `3.14`, `100` | Numeric values |
| **STRING** | `"Hello"`, `"World"` | Text values |
| **OPERATOR** | `=`, `+`, `-`, `==` | Math/logic operations |
| **DELIMITER** | `;`, `{`, `}`, `(`, `)` | Punctuation of code |

### What does the Lexer actually do?
- Reads the code **character by character** (one letter at a time)
- Groups characters into meaningful tokens
- Skips **whitespace** (spaces, empty lines) and **comments** (`// ...`)
- Tracks **line numbers** so errors can point to exact lines

---

## File 3: `parser.py` — The Brain (Phase 2 & 3: Syntax + Semantics)

### What is Syntax Analysis? (In Simple Words)
After getting the tokens, the Parser checks: **"Are the tokens in the right order?"**

Think of it like grammar in English:
- ✅ `"I am happy"` → Correct grammar
- ❌ `"happy am I"` → Wrong grammar (even though same words)

Similarly:
- ✅ `int x = 10;` → Correct syntax
- ❌ `x int = 10;` → Wrong syntax (type must come before name)

### What is Semantic Analysis? (In Simple Words)
Even if the code has correct syntax, it might not *make sense*:
- ✅ `int x = 10;` → Makes sense (assigning a number to an integer)
- ❌ `int x = "Hello";` → Does NOT make sense (giving text to an integer)

Your parser performs these **4 semantic checks**:

| Check | Example of Error Caught |
|---|---|
| **Duplicate Declaration** | Declaring `int x;` twice in same scope |
| **Undeclared Variable** | Using `y = 5;` without first declaring `y` |
| **Type Mismatch** | Error: `int age = "twenty";` |
| **Constant Reassignment** | Error: `PI = 3.0;` after declaring `const float PI = 3.14;` |

### How does the Parser work?
The Parser uses **Grammar Rules** (like a rulebook). In your project, the grammar looks like this:
```
declaration → (const)? type IDENTIFIER (= expression)? ;
```

This means: **"Optionally `const`, then a type, then a name, optionally `= value`, then a semicolon"**

---

## File 4: `symbol_table.py` — The Memory (Phase 3: Symbol Table)

### What is a Symbol Table? (In Simple Words)
Imagine a **school register**. Every time a student (variable) joins, they are recorded:
- Their Name
- Their Type (variable type, like int)
- Which class they are in (scope)
- Their value

Your Symbol Table does exactly this for **every variable** in the code.

### How does it store data?
It uses a **Nested Dictionary** (Python data structure):
```python
{
    "global": {
        "x":  SymbolEntry(name="x",  type="int",   value=10,  line=1),
        "PI": SymbolEntry(name="PI", type="float", value=3.14, constant=True)
    },
    "global.block1": {
        "counter": SymbolEntry(name="counter", type="int", value=5, line=12)
    }
}
```

`global.block1` means a variable that lives *inside* a `{ }` block.

### 4 Operations (CRUD):
| Operation | Method | What it does |
|---|---|---|
| **Insert** | `insert(name, type, line)` | Add a new variable |
| **Lookup** | `lookup(name)` | Find a variable |
| **Update** | `update(name, value)` | Change a variable's value |
| **Delete** | `delete(name)` | Remove a variable |

### What is a Scope?
A **Scope** is the region where a variable is valid.

```cpp
int x = 10;          // x lives in "global" scope

{                    // NEW SCOPE starts here
    int y = 20;      // y lives in "global.block1"
    // x is STILL visible here because it's from the parent
}

// y is DEAD here (out of scope)
// x is still ALIVE here
```

Your project manages this using a **Scope Stack** (like a stack of plates). When a `{` is seen, a plate is added. When `}` is seen, the top plate is removed.

---

# 🔄 PART 3: THE COMPLETE FLOW (Step by Step)

Let's trace **one line of code** through your entire project:

### Source Code: `const int MAX = 100;`

**Step 1 — Lexer reads it:**
```
[const] [int] [MAX] [=] [100] [;]
  KW     KW    ID   OP   NUM   DL
```

**Step 2 — Parser processes the tokens:**
- Sees `const` → sets flag: `is_constant = True`
- Sees `int` → sets: `var_type = "int"`
- Sees `MAX` → extracts name: `var_name = "MAX"`
- Sees `=` → enters initialization path
- Sees `100` → sets: `value = "100"`
- Sees `;` → declaration is complete!

**Step 3 — Parser calls Symbol Table:**
```python
symbol_table.insert("MAX", "int", line=1, value="100", constant=True)
```

**Step 4 — Symbol Table saves it:**
```
Scope: global
 MAX | int | line 1 | value: 100 | constant: TRUE
```

**Step 5 — Later if someone writes `MAX = 200;`:**
- Parser calls `symbol_table.update("MAX", value="200")`
- Symbol Table sees: `"MAX" has constant=True`
- Symbol Table returns `False` (REJECTED!)
- Parser reports: `ERROR: Cannot reassign constant 'MAX'`

---

# 🧪 PART 4: HOW TO RUN AND TEST

## Setting Up (One Time)
Make sure you have **Python** installed. Check with:
```powershell
python --version
```

Navigate to your project folder:
```powershell
cd C:\Users\mzees\.gemini\antigravity\scratch\mini_compiler
```

## Running Tests

### Test 1: The Success Test (Advanced Features)
```powershell
python compiler.py examples/test_advanced.txt
```
**What to look for:**
- Tokens are counted
- Scopes like `global`, `global.block1` are shown
- Constants `PI` and `MAX_USERS` appear with `True` in the Const column
- Arrays like `scores[5]` appear with their metadata

### Test 2: The Error Test (Failure Scenarios)
```powershell
python compiler.py examples/test_failure.txt
```
**What to look for:**
- RED error messages for Type Mismatches
- Error for Duplicate Declaration of `temperature`
- Error for Undeclared variable `local_scope` (used outside its block)
- Total of **7 errors** detected

### Test 3: Unit Tests (All 12 Core Tests)
```powershell
python test_symbol_table.py
```
**What to look for:**
- `12 tests` listed
- All `ok` statuses
- `Ran 12 tests in X.XXs — OK`

### Creating a New Test File (For Live Demo)
1. Create a file in `examples/` folder — e.g., `my_demo.txt`
2. Write your code:
```cpp
int age = 21;
const string name = "Ali";
float gpa = 3.8;

if (age > 18) {
    bool is_adult = true;
}
```
3. Run it:
```powershell
python compiler.py examples/my_demo.txt
```

---

# ❓ PART 5: VIVA Q&A — ALL POSSIBLE QUESTIONS

## Basic Questions (Everyone Gets These)

**Q: What is this project about?**
> "Sir, this is a Symbol Table Manager — the core component of any compiler. It stores information about all the variables in a program: their names, types, scopes, and values. We also built a Lexer and Parser that feeds data into the Symbol Table and performs error checking."

**Q: What language did you use?**
> "We used **Python**. Its built-in dictionary data structure is a hash map, which gives us O(1) — near-instant — lookup performance, making it ideal for a Symbol Table."

**Q: How many phases are in your compiler?**
> "We implemented **3 phases**:
> 1. Lexical Analysis (Lexer) — Tokenization
> 2. Syntax + Semantic Analysis (Parser) — Grammar + Error Checking
> 3. Symbol Table Management — Storage + Scope Resolution"

---

## Intermediate Questions

**Q: What is Lexical Analysis?**
> "It is the first phase. The Lexer reads the raw source code character-by-character and groups them into meaningful units called **Tokens**. For example, `int x = 10;` becomes 5 tokens: KEYWORD, IDENTIFIER, OPERATOR, NUMBER, DELIMITER. It also skips whitespace and comments."

**Q: What is Syntax Analysis?**
> "The Parser takes the tokens from the Lexer and checks if they are in the correct order according to our **Grammar Rules**. If someone writes `x int = 10;` instead of `int x = 10;`, the Parser catches it because the grammar says the TYPE must come before the IDENTIFIER."

**Q: What is Semantic Analysis?**
> "Semantic means 'meaning'. Even if the syntax is correct, the code might not make logical sense. For example, `int x = "Hello";` is syntactically fine but semantically wrong because we are trying to put text into an integer. Our Parser's `_infer_type()` method catches this."

**Q: What is a Scope?**
> "A scope defines the 'lifetime' and 'visibility' of a variable. A variable declared inside `{ }` only exists within that block. Our project manages this with a **Scope Stack** — when we enter a block, we push a new scope; when we leave it, we pop it off."

---

## Advanced Questions (A+ Features)

**Q: How does Constant Enforcement work?**
> "In `symbol_table.py`, every `SymbolEntry` has a `constant` boolean flag. The `update()` method checks this flag before allowing any modification. If `constant=True`, the update is rejected and an error is returned to the Parser, which then reports it to the user."

**Q: How does Type Checking work?**
> "We wrote a helper function called `_infer_type()` in `parser.py`. After parsing the right-hand side of an assignment, this function analyzes the value string to determine its type — is it in quotes (string)? Does it have a dot (float)? Is it `true/false` (bool)? We then compare this inferred type with the declared type of the variable."

**Q: What is Variable Shadowing?**
> "Shadowing happens when you declare a variable with the same name in an inner scope as one in an outer scope. Our `lookup()` method searches from the innermost (current) scope outward, so it always finds the nearest one first. In our test output, you can see `counter` exists in both `global` and `global.block3` — they are two separate variables."

**Q: How is the Symbol Table implemented internally?**
> "It's a nested Python dictionary. The outer key is the scope name (e.g., `'global.block1'`). The inner key is the variable name. Each value is a `SymbolEntry` dataclass containing all the metadata about that variable."

**Q: What is the time complexity of your lookup?**
> "O(1) on average. Python dictionaries use hash maps internally, so accessing a key is near-instantaneous regardless of how many variables are in the table."

---

# 🚀 PART 6: THE LIVE DEMO SCRIPT

When the examiner says "show me", follow these steps:

### Demo 1 — Show a clean run:
```powershell
python compiler.py examples/test_advanced.txt
```
Say: *"Sir, see here: we have 5 scopes, 16 symbols, and 0 errors. The constants PI and MAX_USERS are stored, and the while-loop created its own scope called `global.block1`."*

### Demo 2 — Show error detection:
```powershell
python compiler.py examples/test_failure.txt
```
Say: *"Now, I'm running a file with intentional mistakes. Watch how our compiler catches 7 errors — type mismatches, duplicate declarations, and scope violations — all with exact line numbers."*

### Demo 3 — Create a new file live:
Open Notepad or VS Code, create `examples/live.txt`, type:
```cpp
const int limit = 10;
int count = 0;
while (count < 5) {
    float temp = 1.5;
    count = count + 1;
}
```
Run: `python compiler.py examples/live.txt`

---

# 📊 PART 7: QUICK STATISTICS FROM YOUR PROJECT

| Metric | Value |
|---|---|
| **Language** | Python 3.x |
| **Files** | 5 core files + examples |
| **Unit Tests** | 12 (100% pass rate) |
| **Scopes Supported** | Unlimited nesting |
| **Errors Detected** | 7 types of semantic errors |
| **Lookup Speed** | O(1) average |
| **Features** | Constants, Type Checking, Arrays, Control Flow Scopes |

---

# ✅ FINAL CHECKLIST BEFORE VIVA

- [ ] Can you run `python compiler.py examples/test_advanced.txt`? ✅
- [ ] Can you point to the Scope columns in the output? ✅
- [ ] Can you run `python compiler.py examples/test_failure.txt` and explain the errors? ✅
- [ ] Can you explain what a Symbol Table is (in 2 sentences)? ✅
- [ ] Can you explain what Lexical Analysis does (in 2 sentences)? ✅
- [ ] Can you explain what a Scope is (with an example)? ✅

---

> 💡 **Tip**: If you get confused during the viva, just say: *"Let me demonstrate it."* Then run the compiler and point to the output. The output is your best evidence!
