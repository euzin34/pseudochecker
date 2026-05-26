from enum import Enum, auto
from typing import Optional, List, Dict, Set, Any
from src.errors import SyntaxError

class TokenType(Enum):
    # Keywords - Control Flow
    IF = auto()
    THEN = auto()
    ELSE = auto()
    ENDIF = auto()
    FOR = auto()
    TO = auto()
    STEP = auto()
    NEXT = auto()
    WHILE = auto()
    DO = auto()
    ENDWHILE = auto()
    REPEAT = auto()
    UNTIL = auto()
    INPUT = auto()
    OUTPUT = auto()
    DECLARE = auto()
    CONSTANT = auto()
    
    # Procedures and Functions
    PROCEDURE = auto()
    ENDPROCEDURE = auto()
    FUNCTION = auto()
    ENDFUNCTION = auto()
    RETURN = auto()
    RETURNS = auto()
    CALL = auto()
    BYREF = auto()
    BYVAL = auto()
    
    # Case Statement
    CASE = auto()
    OF = auto()
    OTHERWISE = auto()
    ENDCASE = auto()
    
    # Array and Types
    ARRAY = auto()
    TYPE = auto()
    ENDTYPE = auto()
    POINTER = auto()
    
    # File Handling
    OPENFILE = auto()
    CLOSEFILE = auto()
    READFILE = auto()
    WRITEFILE = auto()
    SEEK = auto()
    GETRECORD = auto()
    PUTRECORD = auto()
    
    # File Modes
    READ = auto()
    WRITE = auto()
    APPEND = auto()
    RANDOM = auto()
    
    # Boolean Literals
    TRUE = auto()
    FALSE = auto()
    
    # Logical Operators
    AND = auto()
    OR = auto()
    NOT = auto()
    
    # Arithmetic Operators (Keywords)
    MOD = auto()
    DIV_INT = auto()
    

    # Operators and Punctuation
    ASSIGN = auto()       # <-
    EQ = auto()           # =
    NEQ = auto()          # <>
    LT = auto()           # <
    GT = auto()           # >
    LTE = auto()          # <=
    GTE = auto()          # >=
    PLUS = auto()         # +
    MINUS = auto()        # -
    MULTIPLY = auto()     # *
    DIVIDE = auto()       # /

    LPAREN = auto()       # (
    RPAREN = auto()       # )
    LBRACKET = auto()     # [
    RBRACKET = auto()     # ]
    COMMA = auto()        # ,
    COLON = auto()        # :
    DOT = auto()          # .
    CARET = auto()        # ^ (for pointer)
    
    # Literals and Identifiers
    IDENTIFIER = auto()
    INTEGER = auto()
    REAL = auto()
    STRING = auto()
    CHAR = auto()
    
    # Built-in Functions (recognized as special identifiers)
    BUILTIN_FUNC = auto()
    
    # End of File
    EOF = auto()

class Token:
    def __init__(self, type: TokenType, value: Any, line: int, column: int) -> None:
        self.type: TokenType = type
        self.value: Any = value
        self.line: int = line
        self.column: int = column

    def __repr__(self) -> str:
        return f"Token({self.type.name}, '{self.value}', Line:{self.line})"

class Tokenizer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.pos = 0
        self.line = 1
        self.column = 1
        self.current_char = self.source_code[0] if self.source_code else None
        
        self.keywords = {
            'IF': TokenType.IF,
            'THEN': TokenType.THEN,
            'ELSE': TokenType.ELSE,
            'ENDIF': TokenType.ENDIF,
            'FOR': TokenType.FOR,
            'TO': TokenType.TO,
            'STEP': TokenType.STEP,
            'NEXT': TokenType.NEXT,
            'WHILE': TokenType.WHILE,
            'DO': TokenType.DO,
            'ENDWHILE': TokenType.ENDWHILE,
            'REPEAT': TokenType.REPEAT,
            'UNTIL': TokenType.UNTIL,
            'INPUT': TokenType.INPUT,
            'OUTPUT': TokenType.OUTPUT,
            'DECLARE': TokenType.DECLARE,
            'CONSTANT': TokenType.CONSTANT,
            'PROCEDURE': TokenType.PROCEDURE,
            'ENDPROCEDURE': TokenType.ENDPROCEDURE,
            'FUNCTION': TokenType.FUNCTION,
            'ENDFUNCTION': TokenType.ENDFUNCTION,
            'RETURN': TokenType.RETURN,
            'RETURNS': TokenType.RETURNS,
            'CALL': TokenType.CALL,
            'BYREF': TokenType.BYREF,
            'BYVAL': TokenType.BYVAL,
            'CASE': TokenType.CASE,
            'OF': TokenType.OF,
            'OTHERWISE': TokenType.OTHERWISE,
            'ENDCASE': TokenType.ENDCASE,
            'ARRAY': TokenType.ARRAY,
            'TYPE': TokenType.TYPE,
            'ENDTYPE': TokenType.ENDTYPE,
            'POINTER': TokenType.POINTER,
            'OPENFILE': TokenType.OPENFILE,
            'CLOSEFILE': TokenType.CLOSEFILE,
            'READFILE': TokenType.READFILE,
            'WRITEFILE': TokenType.WRITEFILE,
            'SEEK': TokenType.SEEK,
            'GETRECORD': TokenType.GETRECORD,
            'PUTRECORD': TokenType.PUTRECORD,
            'READ': TokenType.READ,
            'WRITE': TokenType.WRITE,
            'APPEND': TokenType.APPEND,
            'RANDOM': TokenType.RANDOM,
            'TRUE': TokenType.TRUE,
            'FALSE': TokenType.FALSE,
            'AND': TokenType.AND,
            'OR': TokenType.OR,
            'NOT': TokenType.NOT,
            'MOD': TokenType.MOD,
            'DIV': TokenType.DIV_INT,
        }
        
        # Built-in functions - will be recognized but treated specially
        self.builtin_functions = {
            'LENGTH', 'LEFT', 'RIGHT', 'MID',
            'LCASE', 'UCASE', 'TO_UPPER', 'TO_LOWER',
            'NUM_TO_STR', 'STR_TO_NUM', 'IS_NUM',
            'ASC', 'CHR',
            'INT', 'RAND', 'RANDOM', 'ROUND',
            'DAY', 'MONTH', 'YEAR',
            'EOF'
        }

    def advance(self) -> None:
        if self.current_char == '\n':
            self.line += 1
            self.column = 0
        
        self.pos += 1
        if self.pos < len(self.source_code):
            self.current_char = self.source_code[self.pos]
        else:
            self.current_char = None
        self.column += 1

    def peek(self) -> Optional[str]:
        peek_pos = self.pos + 1
        if peek_pos < len(self.source_code):
            return self.source_code[peek_pos]
        return None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        while self.current_char is not None and self.current_char != '\n':
            self.advance()

    def number(self) -> Token:
        result = ''
        start_col = self.column
        has_decimal = False
        
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                if has_decimal:
                    raise SyntaxError("Invalid number format: multiple decimal points", self.line, self.column)
                has_decimal = True
            result += self.current_char
            self.advance()
        
        if has_decimal:
            return Token(TokenType.REAL, float(result), self.line, start_col)
        else:
            return Token(TokenType.INTEGER, int(result), self.line, start_col)

    def identifier(self) -> Token:
        result = ''
        start_col = self.column
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        
        # Check if it's a keyword
        token_type = self.keywords.get(result.upper(), None)
        if token_type:
            return Token(token_type, result, self.line, start_col)
        
        # Check if it's a built-in function
        if result.upper() in self.builtin_functions:
            return Token(TokenType.BUILTIN_FUNC, result, self.line, start_col)
        
        # Otherwise it's a regular identifier
        return Token(TokenType.IDENTIFIER, result, self.line, start_col)

    def string(self) -> Token:
        result = ''
        start_col = self.column
        quote_char = self.current_char  # Can be " or '
        self.advance() # Skip opening quote
        
        while self.current_char is not None and self.current_char != quote_char:
            result += self.current_char
            self.advance()
            
        if self.current_char == quote_char:
            self.advance() # Skip closing quote
            # Single quotes for CHAR, double quotes for STRING
            if quote_char == "'" and len(result) == 1:
                return Token(TokenType.CHAR, result, self.line, start_col)
            elif quote_char == "'" and len(result) != 1:
                raise SyntaxError(f"CHAR literal must contain exactly one character, found {len(result)}", self.line, start_col,
                                "Use double quotes for strings or ensure single quotes contain exactly one character")
            return Token(TokenType.STRING, result, self.line, start_col)
        else:
            raise SyntaxError("Unterminated string literal", self.line, self.column,
                            f"Add closing {quote_char} at the end of the string")

    def tokenize(self) -> List[Token]:
        tokens = []
        
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            # Handle comments
            if self.current_char == '/' and self.peek() == '/':
                self.skip_comment()
                continue
                
            if self.current_char.isdigit():
                tokens.append(self.number())
                continue
                
            if self.current_char.isalpha() or self.current_char == '_':
                tokens.append(self.identifier())
                continue
                
            if self.current_char == '"' or self.current_char == "'":
                tokens.append(self.string())
                continue
                
            if self.current_char == '<':
                if self.peek() == '-':
                    self.advance()
                    self.advance()
                    tokens.append(Token(TokenType.ASSIGN, '<-', self.line, self.column - 2))
                elif self.peek() == '>':
                    self.advance()
                    self.advance()
                    tokens.append(Token(TokenType.NEQ, '<>', self.line, self.column - 2))
                elif self.peek() == '=':
                    self.advance()
                    self.advance()
                    tokens.append(Token(TokenType.LTE, '<=', self.line, self.column - 2))
                else:
                    self.advance()
                    tokens.append(Token(TokenType.LT, '<', self.line, self.column - 1))
                continue
                
            if self.current_char == '>':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    tokens.append(Token(TokenType.GTE, '>=', self.line, self.column - 2))
                else:
                    self.advance()
                    tokens.append(Token(TokenType.GT, '>', self.line, self.column - 1))
                continue

            if self.current_char == '=':
                self.advance()
                tokens.append(Token(TokenType.EQ, '=', self.line, self.column - 1))
                continue
                
            if self.current_char == '+':
                self.advance()
                tokens.append(Token(TokenType.PLUS, '+', self.line, self.column - 1))
                continue
                
            if self.current_char == '-':
                self.advance()
                tokens.append(Token(TokenType.MINUS, '-', self.line, self.column - 1))
                continue
                
            if self.current_char == '*':
                self.advance()
                tokens.append(Token(TokenType.MULTIPLY, '*', self.line, self.column - 1))
                continue
                
            if self.current_char == '/':
                self.advance()
                tokens.append(Token(TokenType.DIVIDE, '/', self.line, self.column - 1))
                continue
                
            if self.current_char == '(':
                self.advance()
                tokens.append(Token(TokenType.LPAREN, '(', self.line, self.column - 1))
                continue
                
            if self.current_char == ')':
                self.advance()
                tokens.append(Token(TokenType.RPAREN, ')', self.line, self.column - 1))
                continue
                
            if self.current_char == ',':
                self.advance()
                tokens.append(Token(TokenType.COMMA, ',', self.line, self.column - 1))
                continue

            if self.current_char == ':':
                self.advance()
                tokens.append(Token(TokenType.COLON, ':', self.line, self.column - 1))
                continue
            
            if self.current_char == '[':
                self.advance()
                tokens.append(Token(TokenType.LBRACKET, '[', self.line, self.column - 1))
                continue
            
            if self.current_char == ']':
                self.advance()
                tokens.append(Token(TokenType.RBRACKET, ']', self.line, self.column - 1))
                continue
            
            if self.current_char == '.':
                self.advance()
                tokens.append(Token(TokenType.DOT, '.', self.line, self.column - 1))
                continue
            
            if self.current_char == '^':
                self.advance()
                tokens.append(Token(TokenType.CARET, '^', self.line, self.column - 1))
                continue
            
            raise SyntaxError(f"Unexpected character: '{self.current_char}'", self.line, self.column,
                            "Remove this character or check if it's a typo")
            
        tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return tokens
