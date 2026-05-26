# CIE 9618 Pseudocode Quick Reference

## New Syntax Added

### 1. Data Types
- **REAL** - Decimal numbers (e.g., 3.14, 2.718)
- **CHAR** - Single character in single quotes (e.g., 'A', 'x')
- **BOOLEAN** - TRUE or FALSE

### 2. Constants
```pseudocode
CONSTANT PI = 3.14159
CONSTANT MAX_VALUE = 100
```

### 3. Arrays
```pseudocode
// Declaration
DECLARE numbers : ARRAY[1:10] OF INTEGER
DECLARE matrix : ARRAY[1:5, 1:5] OF REAL

// Access and Assignment
numbers[1] <- 42
x <- numbers[1] + numbers[2]
matrix[1, 1] <- 1.5
```

### 4. CASE Statement
```pseudocode
CASE OF variable
  value1 : statement1
  value2 : statement2
  value3 : statement3
ENDCASE
```

### 5. Procedures
```pseudocode
PROCEDURE ProcedureName(param1 : TYPE1, param2 : TYPE2)
  // statements
ENDPROCEDURE

// Calling
CALL ProcedureName(arg1, arg2)
```

### 6. Functions
```pseudocode
FUNCTION FunctionName(param1 : TYPE1) RETURNS TYPE
  // statements
  RETURN value
ENDFUNCTION

// Calling
result <- FunctionName(arg1)
```

### 7. Parameter Passing Modes
```pseudocode
PROCEDURE Example(BYVAL x : INTEGER, BYREF y : INTEGER)
  // BYVAL = pass by value
  // BYREF = pass by reference
ENDPROCEDURE
```

## Error Reporting Features

The syntax checker now provides:

1. **Error Type Classification**
   - Syntax Error
   - Semantic Error
   - Type Error
   - Undeclared Variable Error

2. **Precise Location**
   - Line number
   - Column number

3. **Clear Description**
   - What went wrong
   - Why it's an error

4. **Helpful Suggestions**
   - How to fix the error
   - Valid alternatives

## Example Error Messages

### Syntax Error
```
============================================================
❌ SYNTAX ERROR
============================================================
📍 Location: Line 5, Column 10
💬 Description: Expected THEN, but found OUTPUT
💡 Suggestion: Add 'THEN' after the IF condition
============================================================
```

### Invalid Data Type
```
============================================================
❌ SYNTAX ERROR
============================================================
📍 Location: Line 3, Column 15
💬 Description: Invalid data type 'FLOAT'
💡 Suggestion: Valid types are: INTEGER, REAL, STRING, CHAR, BOOLEAN
============================================================
```

### Unterminated String
```
============================================================
❌ SYNTAX ERROR
============================================================
📍 Location: Line 8, Column 20
💬 Description: Unterminated string literal
💡 Suggestion: Add closing " at the end of the string
============================================================
```

## Testing Your Code

1. **Run the checker:**
   ```bash
   python main.py
   ```

2. **Check a file:**
   ```
   >> run your_file.txt
   ```

3. **View help:**
   ```
   >> help
   ```

4. **Exit:**
   ```
   >> exit
   ```

## Supported Operators

### Arithmetic
- `+` Addition
- `-` Subtraction
- `*` Multiplication
- `/` Division (real)
- `DIV` Integer division
- `MOD` Modulus

### Comparison
- `=` Equal to
- `<>` Not equal to
- `<` Less than
- `>` Greater than
- `<=` Less than or equal to
- `>=` Greater than or equal to

### Logical
- `AND` Logical AND
- `OR` Logical OR
- `NOT` Logical NOT

## All Supported Keywords

`AND`, `ARRAY`, `BOOLEAN`, `BYREF`, `BYVAL`, `CALL`, `CASE`, `CHAR`, `CONSTANT`, `DECLARE`, `DIV`, `DO`, `ELSE`, `ENDCASE`, `ENDIF`, `ENDWHILE`, `FALSE`, `FOR`, `FUNCTION`, `IF`, `INPUT`, `INTEGER`, `MOD`, `NEXT`, `NOT`, `OF`, `OR`, `OTHERWISE`, `OUTPUT`, `PROCEDURE`, `REAL`, `REPEAT`, `RETURN`, `RETURNS`, `STEP`, `STRING`, `THEN`, `TO`, `TRUE`, `UNTIL`, `WHILE`

## Tips for Writing Valid Pseudocode

1. **Always declare variables before use**
   ```pseudocode
   DECLARE x : INTEGER
   x <- 10
   ```

2. **Match IF with ENDIF, FOR with NEXT, etc.**
   ```pseudocode
   IF condition THEN
     // statements
   ENDIF
   ```

3. **Use correct assignment operator**
   ```pseudocode
   x <- 5  // Correct
   x = 5   // Wrong (= is for comparison)
   ```

4. **Close all strings and characters**
   ```pseudocode
   name <- "Alice"  // Correct
   initial <- 'A'   // Correct
   ```

5. **Use valid data types**
   - INTEGER, REAL, STRING, CHAR, BOOLEAN
   - NOT: int, float, str, etc.

## What's Validated

✅ Syntax correctness
✅ Keyword usage
✅ Operator precedence
✅ Statement structure
✅ Data type validity
✅ String/character literals
✅ Array bounds syntax
✅ Procedure/function signatures
✅ Control flow structure

## What's NOT Validated (Yet)

❌ Runtime errors
❌ Logic errors
❌ Variable initialization
❌ Array bounds checking
❌ Type compatibility
❌ Function return paths
