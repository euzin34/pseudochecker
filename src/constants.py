#
# Constants and configuration for the CIE 9618 Pseudocode Checker.
# Complete specification with all keywords, data types, and built-in functions.

# Version information
VERSION = "2.0.0"
APP_NAME = "Cambridge 9618 Pseudocode Analyzer"
APP_SUBTITLE = "CIE A-Level Computer Science - Complete Semantic Analyzer"

# Valid data types in CIE 9618
VALID_DATA_TYPES = ["INTEGER", "REAL", "STRING", "CHAR", "BOOLEAN", "DATE"]

# All CIE 9618 keywords (70+ keywords)
KEYWORDS = [
    # Control Flow
    "IF",
    "THEN",
    "ELSE",
    "ENDIF",
    "FOR",
    "TO",
    "STEP",
    "NEXT",
    "WHILE",
    "DO",
    "ENDWHILE",
    "REPEAT",
    "UNTIL",
    "CASE",
    "OF",
    "OTHERWISE",
    "ENDCASE",
    # Declarations
    "DECLARE",
    "CONSTANT",
    "TYPE",
    "ENDTYPE",
    "ARRAY",
    # Procedures and Functions
    "PROCEDURE",
    "ENDPROCEDURE",
    "FUNCTION",
    "ENDFUNCTION",
    "RETURN",
    "RETURNS",
    "CALL",
    "BYREF",
    "BYVAL",
    # I/O
    "INPUT",
    "OUTPUT",
    # File Handling
    "OPENFILE",
    "CLOSEFILE",
    "READFILE",
    "WRITEFILE",
    "SEEK",
    "GETRECORD",
    "PUTRECORD",
    # File Modes
    "READ",
    "WRITE",
    "APPEND",
    "RANDOM",
    # Logical Operators
    "AND",
    "OR",
    "NOT",
    # Arithmetic Keywords
    "MOD",
    "DIV",
    # Boolean Literals
    "TRUE",
    "FALSE",
    # Pointer
    "POINTER",
]

# Built-in Functions in CIE 9618
BUILTIN_FUNCTIONS = {
    # String Functions
    "LENGTH": {"params": 1, "param_types": ["STRING"], "return_type": "INTEGER"},
    "LEFT": {
        "params": 2,
        "param_types": ["STRING", "INTEGER"],
        "return_type": "STRING",
    },
    "RIGHT": {
        "params": 2,
        "param_types": ["STRING", "INTEGER"],
        "return_type": "STRING",
    },
    "MID": {
        "params": 3,
        "param_types": ["STRING", "INTEGER", "INTEGER"],
        "return_type": "STRING",
    },
    "LCASE": {"params": 1, "param_types": ["CHAR"], "return_type": "CHAR"},
    "UCASE": {"params": 1, "param_types": ["CHAR"], "return_type": "CHAR"},
    "TO_UPPER": {"params": 1, "param_types": ["STRING"], "return_type": "STRING"},
    "TO_LOWER": {"params": 1, "param_types": ["STRING"], "return_type": "STRING"},
    "NUM_TO_STR": {"params": 1, "param_types": ["INTEGER"], "return_type": "STRING"},
    "STR_TO_NUM": {"params": 1, "param_types": ["STRING"], "return_type": "INTEGER"},
    "IS_NUM": {"params": 1, "param_types": ["STRING"], "return_type": "BOOLEAN"},
    "ASC": {"params": 1, "param_types": ["CHAR"], "return_type": "INTEGER"},
    "CHR": {"params": 1, "param_types": ["INTEGER"], "return_type": "CHAR"},
    # Math Functions
    "INT": {"params": 1, "param_types": ["REAL"], "return_type": "INTEGER"},
    "RAND": {"params": 1, "param_types": ["INTEGER"], "return_type": "INTEGER"},
    "RANDOM": {"params": 1, "param_types": ["INTEGER"], "return_type": "INTEGER"},
    "ROUND": {"params": 1, "param_types": ["REAL"], "return_type": "INTEGER"},
    # Date Functions
    "DAY": {"params": 1, "param_types": ["DATE"], "return_type": "INTEGER"},
    "MONTH": {"params": 1, "param_types": ["DATE"], "return_type": "INTEGER"},
    "YEAR": {"params": 1, "param_types": ["DATE"], "return_type": "INTEGER"},
    # File Functions
    "EOF": {"params": 1, "param_types": ["STRING"], "return_type": "BOOLEAN"},
}

# Operators
ARITHMETIC_OPERATORS = ["+", "-", "*", "/", "MOD", "DIV"]
COMPARISON_OPERATORS = ["=", "<>", "<", ">", "<=", ">="]
LOGICAL_OPERATORS = ["AND", "OR", "NOT"]
ASSIGNMENT_OPERATOR = "<-"

# File extensions
VALID_FILE_EXTENSIONS = [".txt", ".pseudo", ".psc"]

# Display settings
SEPARATOR_LENGTH = 70
ERROR_SEPARATOR = "=" * SEPARATOR_LENGTH
INFO_SEPARATOR = "-" * SEPARATOR_LENGTH

# Error messages
ERROR_MESSAGES = {
    "file_not_found": "File '{filename}' does not exist",
    "invalid_extension": "File must have one of these extensions: {extensions}",
    "permission_denied": "Permission denied to read '{filename}'",
    "empty_file": "File '{filename}' is empty",
    # Semantic errors
    "undeclared_variable": "Variable '{name}' is used before being declared",
    "duplicate_declaration": "Variable '{name}' is already declared in this scope",
    "type_mismatch": "Type mismatch: Cannot assign {source_type} to {target_type}",
    "undefined_function": "Function '{name}' is not defined",
    "wrong_param_count": (
        "Function '{name}' expects {expected} parameters, " "but got {actual}"
    ),
    "missing_return": "Function '{name}' must return a value of type {type}",
    "unreachable_code": "Code after RETURN statement is unreachable",
    "uninitialized_variable": "Variable '{name}' may be used before initialization",
    "invalid_array_index": "Array index must be of type INTEGER",
    "array_bounds_error": "Array bounds must be INTEGER constants with lower <= upper",
}

# Success messages
SUCCESS_MESSAGES = {
    "no_errors": "✅ SUCCESS: No errors found in the pseudocode!",
    "syntax_valid": "Your pseudocode follows CIE 9618 syntax correctly.",
    "semantics_valid": "All variables are properly declared and types match.",
}

# Progress indicators
PROGRESS_INDICATORS = {
    "tokenizing": "⏳ Tokenizing {filename}...",
    "parsing": "⏳ Parsing {filename}...",
    "semantic_analysis": "⏳ Performing semantic analysis...",
    "validating": "⏳ Validating logic and types...",
    "complete": "✓ {stage} successful",
}

# Help text
HELP_TEXT = (
    "Commands:\n"
    "  run [filename]  - Analyze pseudocode in specified file\n"
    "                   (default: examples/basic_example.txt)\n"
    "  help            - Show this help message\n"
    "  exit            - Quit the program\n"
    "\n"
    "Examples:\n"
    "  run                              - Check examples/basic_example.txt\n"
    "  run examples/advanced_example.txt - Check advanced example\n"
    "  run tests/buggy_code.txt         - Test error detection\n"
    "\n"
    "Options:\n"
    "  --strict        - Enable all warnings\n"
    "  --explain       - Show detailed error explanations\n"
    "  --context       - Display code context in errors\n"
)


# Color codes (for terminal coloring)
COLORS = {
    "reset": "\033[0m",
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "magenta": "\033[95m",
    "cyan": "\033[96m",
}

# Semantic analysis settings
SEMANTIC_ANALYSIS = {
    "track_initialization": True,
    "warn_unreachable_code": True,
    "warn_unused_variables": False,  # Can be noisy for students
    "strict_type_checking": True,
}

# Error severity levels
ERROR_SEVERITY = {
    "CRITICAL": 3,  # Syntax errors, undeclared variables
    "ERROR": 2,  # Type mismatches, logic errors
    "WARNING": 1,  # Uninitialized variables, unreachable code
}
