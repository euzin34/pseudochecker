# Cambridge 9618 Pseudocode Syntax Checker

A comprehensive syntax checker and transpiler for Cambridge A-Level Computer Science (9618) pseudocode. This tool validates pseudocode syntax and provides detailed error reporting with line numbers and helpful suggestions.

## Features ✨

### Comprehensive CIE 9618 Syntax Support

#### Data Types
- `INTEGER` - Whole numbers
- `REAL` - Decimal numbers (e.g., 3.14)
- `STRING` - Text in double quotes
- `CHAR` - Single character in single quotes
- `BOOLEAN` - TRUE or FALSE values

#### Variable Declarations
```pseudocode
DECLARE x : INTEGER
DECLARE name : STRING
DECLARE isValid : BOOLEAN
```

#### Constants
```pseudocode
CONSTANT PI = 3.14159
CONSTANT MAX_SIZE = 100
```

#### Arrays
```pseudocode
// 1D Array
DECLARE numbers : ARRAY[1:10] OF INTEGER

// 2D Array
DECLARE matrix : ARRAY[1:5, 1:5] OF REAL

// Array access and assignment
numbers[1] <- 42
matrix[1, 1] <- 1.5
x <- numbers[1] + numbers[2]
```

#### Conditional Statements
```pseudocode
// IF-THEN-ELSE
IF x > 5 THEN
  OUTPUT "Greater than 5"
ELSE
  OUTPUT "5 or less"
ENDIF

// CASE Statement
CASE OF x
  1 : OUTPUT "One"
  2 : OUTPUT "Two"
  10 : OUTPUT "Ten"
ENDCASE
```

#### Loops
```pseudocode
// FOR Loop
FOR i <- 1 TO 10 STEP 1
  OUTPUT i
NEXT i

// FOR Loop with negative step
FOR j <- 10 TO 1 STEP -1
  OUTPUT j
NEXT j

// WHILE Loop
WHILE x > 0 DO
  OUTPUT x
  x <- x - 1
ENDWHILE

// REPEAT-UNTIL Loop
REPEAT
  INPUT x
UNTIL x > 0
```

#### Operators
- **Arithmetic**: `+`, `-`, `*`, `/`, `MOD`, `DIV`
- **Comparison**: `=`, `<>`, `<`, `>`, `<=`, `>=`
- **Logical**: `AND`, `OR`, `NOT`

#### Input/Output
```pseudocode
INPUT name
OUTPUT "Hello, ", name
OUTPUT x, y, z
```

#### Procedures and Functions
```pseudocode
// Procedure Declaration
PROCEDURE PrintMessage(msg : STRING)
  OUTPUT msg
ENDPROCEDURE

// Function Declaration
FUNCTION Add(a : INTEGER, b : INTEGER) RETURNS INTEGER
  RETURN a + b
ENDFUNCTION

// Calling
CALL PrintMessage("Hello")
result <- Add(5, 3)
```

## Error Reporting 🔍

The syntax checker provides detailed error messages with:
- **Error Type**: Syntax Error, Semantic Error, Type Error, etc.
- **Line Number**: Exact location of the error
- **Description**: Clear explanation of what went wrong
- **Suggestion**: Helpful hint on how to fix the error

### Example Error Output
```
============================================================
❌ SYNTAX ERROR
============================================================
📍 Location: Line 12, Column 5
💬 Description: Expected THEN, but found OUTPUT
💡 Suggestion: Add 'THEN' after the IF condition
============================================================
```

## Usage 🚀

### Running the Syntax Checker

```bash
python main.py
```

### Commands

- `run [filename]` - Check pseudocode in specified file (default: test_input.txt)
- `help` - Show help message
- `exit` - Quit the program

### Examples

```bash
>> run                          # Check test_input.txt
>> run test_comprehensive.txt   # Check test_comprehensive.txt
>> run my_code.txt             # Check my_code.txt
```

## Project Structure 📁

```
Pesudochecker/
├── main.py                      # Main entry point with CLI
├── src/
│   ├── tokenizer.py            # Lexical analyzer
│   ├── parser.py               # Syntax analyzer and AST generator
│   ├── transpiler.py           # Code generator (Pseudocode → Python)
│   └── errors.py               # Custom error classes
├── test_input.txt              # Sample test file
├── test_comprehensive.txt      # Comprehensive syntax examples
├── test_errors.txt             # Error testing file
└── README.md                   # This file
```

## Supported Syntax Summary 📋

### Keywords
`IF`, `THEN`, `ELSE`, `ENDIF`, `FOR`, `TO`, `STEP`, `NEXT`, `WHILE`, `DO`, `ENDWHILE`, `REPEAT`, `UNTIL`, `CASE`, `OF`, `OTHERWISE`, `ENDCASE`, `DECLARE`, `CONSTANT`, `PROCEDURE`, `FUNCTION`, `RETURN`, `RETURNS`, `CALL`, `INPUT`, `OUTPUT`, `ARRAY`, `BYREF`, `BYVAL`, `AND`, `OR`, `NOT`, `MOD`, `DIV`, `TRUE`, `FALSE`

### Operators
- Assignment: `<-`
- Arithmetic: `+`, `-`, `*`, `/`, `MOD`, `DIV`
- Comparison: `=`, `<>`, `<`, `>`, `<=`, `>=`
- Logical: `AND`, `OR`, `NOT`

### Literals
- Integers: `42`, `0`, `-5`
- Real numbers: `3.14`, `0.5`, `-2.718`
- Strings: `"Hello, World!"`
- Characters: `'A'`, `'x'`
- Booleans: `TRUE`, `FALSE`

### Comments
```pseudocode
// This is a single-line comment
```

## Testing 🧪

### Test Files Included

1. **test_input.txt** - Basic syntax examples
2. **test_comprehensive.txt** - Comprehensive feature demonstration
3. **test_errors.txt** - Intentional errors for testing error reporting

### Running Tests

```bash
python main.py
>> run test_comprehensive.txt
```

## Implementation Details 🔧

### Three-Phase Architecture

1. **Tokenization** (Lexical Analysis)
   - Breaks source code into tokens
   - Handles keywords, operators, literals, identifiers
   - Tracks line and column numbers for error reporting

2. **Parsing** (Syntax Analysis)
   - Builds Abstract Syntax Tree (AST)
   - Validates syntax structure
   - Enforces operator precedence
   - Provides detailed syntax error messages

3. **Transpilation** (Code Generation)
   - Converts AST to Python code
   - Validates semantic correctness
   - Handles all CIE 9618 constructs

### Operator Precedence
1. Parentheses `()`
2. Unary operators: `NOT`, `-` (negation)
3. Multiplicative: `*`, `/`, `DIV`, `MOD`
4. Additive: `+`, `-`
5. Comparison: `=`, `<>`, `<`, `>`, `<=`, `>=`
6. Logical AND: `AND`
7. Logical OR: `OR`

## Future Enhancements 🚧

- String methods (LENGTH, SUBSTRING, UCASE, LCASE)
- File I/O operations (OPENFILE, READFILE, WRITEFILE, CLOSEFILE)
- More advanced semantic analysis
- Type checking and validation
- Runtime execution with proper type handling
- Custom data types and records

## Requirements 📦

- Python 3.7 or higher
- No external dependencies required

## Author 👨‍💻

Built for Cambridge A-Level Computer Science (9618) pseudocode syntax checking and validation.

## License 📄

This project is created for educational purposes to help students learn and validate CIE 9618 pseudocode syntax.
