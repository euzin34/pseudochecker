# Project Structure

## Directory Layout

```
Pesudochecker/
│
├── main.py                          # Main application entry point
│
├── src/                             # Source code package
│   ├── __init__.py                 # Package initialization
│   ├── tokenizer.py                # Lexical analyzer (50+ keywords)
│   ├── parser.py                   # Syntax analyzer & AST builder
│   ├── transpiler.py               # Code generator (Pseudocode → Python)
│   ├── errors.py                   # Custom error classes
│   ├── utils.py                    # Utility functions
│   └── constants.py                # Configuration & constants
│
├── tests/                           # Test files
│   └── buggy_code.txt              # Comprehensive error testing (25 errors)
│
├── examples/                        # Example pseudocode files
│   ├── basic_example.txt           # Basic syntax examples
│   └── advanced_example.txt        # Advanced features (arrays, case, etc.)
│
├── docs/                            # Documentation
│   ├── README.md                   # Full documentation
│   └── QUICK_REFERENCE.md          # Syntax quick reference
│
├── README.md                        # Project overview
├── .gitignore                      # Git ignore rules
└── 697401-2026-pseudocode-guide-for-teachers.pdf  # CIE official guide
```

## Module Descriptions

### Core Modules

#### `main.py`
- **Purpose**: Application entry point and CLI interface
- **Features**:
  - Interactive command-line interface
  - File reading and validation
  - Progress indicators
  - Error display formatting
- **Dependencies**: All src modules

#### `src/tokenizer.py`
- **Purpose**: Lexical analysis (tokenization)
- **Features**:
  - 50+ CIE 9618 keywords
  - All operators (arithmetic, comparison, logical)
  - Number literals (INTEGER, REAL)
  - String and CHAR literals
  - Boolean literals (TRUE, FALSE)
  - Comments support
  - Line/column tracking
- **Classes**: `Tokenizer`, `Token`, `TokenType`

#### `src/parser.py`
- **Purpose**: Syntax analysis and AST generation
- **Features**:
  - Complete CIE 9618 grammar
  - All control structures (IF, FOR, WHILE, REPEAT, CASE)
  - Arrays (multi-dimensional)
  - Procedures and Functions
  - Operator precedence
  - Detailed syntax error messages
- **Classes**: 20+ AST node classes, `Parser`

#### `src/transpiler.py`
- **Purpose**: Code generation and semantic validation
- **Features**:
  - Converts pseudocode AST to Python
  - Validates semantic correctness
  - Handles all CIE 9618 constructs
- **Classes**: `Transpiler`

#### `src/errors.py`
- **Purpose**: Error handling and reporting
- **Features**:
  - Multiple error types (Syntax, Semantic, Type, etc.)
  - Formatted error messages with emojis
  - Line/column information
  - Helpful suggestions
- **Classes**: `TranspilerError`, `SyntaxError`, `SemanticError`, `TypeError`, `UndeclaredVariableError`

#### `src/utils.py`
- **Purpose**: Utility functions
- **Features**:
  - File reading with error handling
  - Code statistics calculation
  - Error formatting helpers
  - Line content extraction
- **Functions**: 8 utility functions

#### `src/constants.py`
- **Purpose**: Configuration and constants
- **Features**:
  - All CIE 9618 keywords list
  - Valid data types
  - Operators lists
  - Display settings
  - Help text
  - Error/success messages
- **Constants**: 15+ configuration constants

### Test Files

#### `tests/buggy_code.txt`
- **Purpose**: Comprehensive error testing
- **Contains**: 25 different types of syntax errors
- **Tests**:
  - Missing keywords (THEN, ENDIF, etc.)
  - Invalid data types
  - Unterminated strings
  - Wrong operators
  - Invalid characters
  - Mismatched loop variables
  - And 19 more error types

### Example Files

#### `examples/basic_example.txt`
- **Purpose**: Basic syntax demonstration
- **Contains**:
  - Variable declarations
  - Simple assignments
  - IF-THEN-ELSE
  - FOR and WHILE loops
  - Input/Output

#### `examples/advanced_example.txt`
- **Purpose**: Advanced features demonstration
- **Contains**:
  - Constants
  - Multi-dimensional arrays
  - CASE statements
  - Complex expressions
  - Boolean operations
  - Array operations

## File Statistics

### Source Code
- **Total Lines**: ~1,500 lines of Python
- **Modules**: 7 Python files
- **Classes**: 25+ classes
- **Functions**: 50+ functions

### Test Coverage
- **Test Files**: 1 buggy file (25 error types)
- **Example Files**: 2 files (basic + advanced)
- **Total Test Lines**: ~200 lines of pseudocode

### Documentation
- **README Files**: 3 files
- **Total Documentation**: ~1,000 lines

## Code Organization Principles

### 1. Separation of Concerns
- **Tokenizer**: Only handles lexical analysis
- **Parser**: Only handles syntax analysis
- **Transpiler**: Only handles code generation
- **Errors**: Centralized error handling
- **Utils**: Reusable utility functions
- **Constants**: Centralized configuration

### 2. Modularity
- Each module has a single, well-defined purpose
- Clear interfaces between modules
- Easy to test and maintain

### 3. Scalability
- Easy to add new keywords
- Easy to add new syntax features
- Easy to add new error types
- Easy to add new utility functions

### 4. Maintainability
- Clear naming conventions
- Comprehensive docstrings
- Consistent code style
- Centralized constants

## Dependencies

### External
- **None** - Pure Python 3.7+

### Internal
```
main.py
  ├── src.tokenizer
  ├── src.parser
  ├── src.transpiler
  ├── src.errors
  ├── src.utils
  └── src.constants

src.parser
  ├── src.tokenizer
  └── src.errors

src.transpiler
  ├── src.parser
  └── src.tokenizer

src.utils
  └── (no dependencies)

src.constants
  └── (no dependencies)

src.errors
  └── (no dependencies)
```

## Future Enhancements

### Planned Features
1. String methods (LENGTH, SUBSTRING, UCASE, LCASE)
2. File I/O operations
3. More semantic analysis
4. Type checking
5. Variable scope validation
6. Procedure/function call validation

### Possible Additions
1. Web interface
2. Syntax highlighting
3. Auto-completion
4. Code formatting
5. Performance optimization
6. More test cases
