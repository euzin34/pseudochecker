#
# Built-in Functions for CIE 9618 Pseudocode
# Complete implementation of all standard library functions

from src.constants import BUILTIN_FUNCTIONS


class BuiltInFunction:
    """Represents a built-in function with validation capabilities."""

    def __init__(self, name, param_count, param_types, return_type):
        self.name = name
        self.param_count = param_count
        self.param_types = param_types
        self.return_type = return_type

    def validate_params(self, actual_params):
        """Validate that the actual parameters match the expected count and types.

        actual_params: List of (value, type) tuples
        Returns: (is_valid, error_message)
        """
        if len(actual_params) != self.param_count:
            return (
                False,
                (
                    f"Function {self.name} expects {self.param_count} parameter(s), "
                    f"but got {len(actual_params)}"
                ),
            )

        for i, (param_value, param_type) in enumerate(actual_params):
            expected_type = self.param_types[i]
            if param_type != expected_type and expected_type != "ANY":
                return (
                    False,
                    (
                        f"Parameter {i+1} of {self.name} should be {expected_type}, "
                        f"but got {param_type}"
                    ),
                )

        return (True, None)

    def get_return_type(self):
        """Get the return type of this function."""
        return self.return_type


class BuiltInFunctionRegistry:
    """Registry of all built-in functions for validation and lookup."""

    def __init__(self):
        self.functions = {}
        self._initialize_functions()

    def _initialize_functions(self):
        """Initialize all built-in functions from constants."""
        for func_name, spec in BUILTIN_FUNCTIONS.items():
            self.functions[func_name.upper()] = BuiltInFunction(
                name=func_name,
                param_count=spec["params"],
                param_types=spec["param_types"],
                return_type=spec["return_type"],
            )

    def is_builtin(self, name):
        """Check if a name is a built-in function."""
        return name.upper() in self.functions

    def get_function(self, name):
        """Get a built-in function by name."""
        return self.functions.get(name.upper())

    def validate_call(self, name, actual_params):
        """Validate a function call.

        Args:
            name: Function name
            actual_params: List of (value, type) tuples

        Returns:
            (is_valid, error_message, return_type) tuple
        """
        func = self.get_function(name)
        if not func:
            return (False, f"Unknown built-in function: {name}", None)

        is_valid, error_msg = func.validate_params(actual_params)
        if not is_valid:
            return (False, error_msg, None)

        return (True, None, func.get_return_type())


# String Functions
STRING_FUNCTIONS = {
    "LENGTH": {
        "description": "Returns the length of a string",
        "syntax": "LENGTH(string: STRING) RETURNS INTEGER",
        "example": 'LENGTH("Hello") returns 5',
    },
    "LEFT": {
        "description": "Returns the leftmost n characters from a string",
        "syntax": "LEFT(string: STRING, n: INTEGER) RETURNS STRING",
        "example": 'LEFT("Hello", 3) returns "Hel"',
    },
    "RIGHT": {
        "description": "Returns the rightmost n characters from a string",
        "syntax": "RIGHT(string: STRING, n: INTEGER) RETURNS STRING",
        "example": 'RIGHT("Hello", 3) returns "llo"',
    },
    "MID": {
        "description": "Returns a substring starting at position x with length y",
        "syntax": "MID(string: STRING, x: INTEGER, y: INTEGER) RETURNS STRING",
        "example": 'MID("Hello", 2, 3) returns "ell"',
    },
    "LCASE": {
        "description": "Converts a character to lowercase",
        "syntax": "LCASE(char: CHAR) RETURNS CHAR",
        "example": "LCASE('A') returns 'a'",
    },
    "UCASE": {
        "description": "Converts a character to uppercase",
        "syntax": "UCASE(char: CHAR) RETURNS CHAR",
        "example": "UCASE('a') returns 'A'",
    },
    "TO_UPPER": {
        "description": "Converts all characters in a string to uppercase",
        "syntax": "TO_UPPER(string: STRING) RETURNS STRING",
        "example": 'TO_UPPER("hello") returns "HELLO"',
    },
    "TO_LOWER": {
        "description": "Converts all characters in a string to lowercase",
        "syntax": "TO_LOWER(string: STRING) RETURNS STRING",
        "example": 'TO_LOWER("HELLO") returns "hello"',
    },
    "NUM_TO_STR": {
        "description": "Converts a number to a string",
        "syntax": "NUM_TO_STR(number: INTEGER) RETURNS STRING",
        "example": 'NUM_TO_STR(42) returns "42"',
    },
    "STR_TO_NUM": {
        "description": "Converts a string to a number",
        "syntax": "STR_TO_NUM(string: STRING) RETURNS INTEGER",
        "example": 'STR_TO_NUM("42") returns 42',
    },
    "IS_NUM": {
        "description": "Checks if a string represents a valid number",
        "syntax": "IS_NUM(string: STRING) RETURNS BOOLEAN",
        "example": 'IS_NUM("42") returns TRUE',
    },
    "ASC": {
        "description": "Returns the ASCII code of a character",
        "syntax": "ASC(char: CHAR) RETURNS INTEGER",
        "example": "ASC('A') returns 65",
    },
    "CHR": {
        "description": "Returns the character for an ASCII code",
        "syntax": "CHR(code: INTEGER) RETURNS CHAR",
        "example": "CHR(65) returns 'A'",
    },
}

# Math Functions
MATH_FUNCTIONS = {
    "INT": {
        "description": "Returns the integer part of a real number (truncates)",
        "syntax": "INT(number: REAL) RETURNS INTEGER",
        "example": "INT(3.7) returns 3",
    },
    "RAND": {
        "description": "Returns a random integer from 0 to n-1",
        "syntax": "RAND(n: INTEGER) RETURNS INTEGER",
        "example": "RAND(10) returns a number from 0 to 9",
    },
    "RANDOM": {
        "description": "Returns a random integer from 0 to n-1 (alias for RAND)",
        "syntax": "RANDOM(n: INTEGER) RETURNS INTEGER",
        "example": "RANDOM(10) returns a number from 0 to 9",
    },
    "ROUND": {
        "description": "Rounds a real number to the nearest integer",
        "syntax": "ROUND(number: REAL) RETURNS INTEGER",
        "example": "ROUND(3.7) returns 4",
    },
}

# Date Functions
DATE_FUNCTIONS = {
    "DAY": {
        "description": "Extracts the day from a date",
        "syntax": "DAY(date: DATE) RETURNS INTEGER",
        "example": "DAY(15/03/2024) returns 15",
    },
    "MONTH": {
        "description": "Extracts the month from a date",
        "syntax": "MONTH(date: DATE) RETURNS INTEGER",
        "example": "MONTH(15/03/2024) returns 3",
    },
    "YEAR": {
        "description": "Extracts the year from a date",
        "syntax": "YEAR(date: DATE) RETURNS INTEGER",
        "example": "YEAR(15/03/2024) returns 2024",
    },
}

# File Functions
FILE_FUNCTIONS = {
    "EOF": {
        "description": "Checks if end of file has been reached",
        "syntax": "EOF(filename: STRING) RETURNS BOOLEAN",
        "example": 'IF NOT EOF("data.txt") THEN',
    },
}


def get_function_help(func_name):
    """Get help text for a specific function."""
    func_name = func_name.upper()

    for category_name, category in [
        ("String", STRING_FUNCTIONS),
        ("Math", MATH_FUNCTIONS),
        ("Date", DATE_FUNCTIONS),
        ("File", FILE_FUNCTIONS),
    ]:
        if func_name in category:
            info = category[func_name]
            return (
                f"\n{func_name} ({category_name} Function)\n"
                + "=" * 50
                + f"\nDescription: {info['description']}\n"
                f"Syntax: {info['syntax']}\n"
                f"Example: {info['example']}\n"
            )

    return None


def list_all_functions():
    # List all available built-in functions by category
    output = "\n=== CIE 9618 Built-in Functions ===\n\n"

    categories = [
        ("String Functions", STRING_FUNCTIONS),
        ("Math Functions", MATH_FUNCTIONS),
        ("Date Functions", DATE_FUNCTIONS),
        ("File Functions", FILE_FUNCTIONS),
    ]

    for category_name, functions in categories:
        output += f"\n{category_name}:\n"
        output += "-" * 50 + "\n"
        for func_name, info in functions.items():
            output += f"  {info['syntax']}\n"
        output += "\n"

    return output
