from typing import List, Optional, Tuple, Any
from src.tokenizer import Token, TokenType
from src.errors import SyntaxError

class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class Declaration(ASTNode):
    def __init__(self, identifier, dtype, is_array=False, array_bounds=None, is_constant=False):
        self.identifier = identifier
        self.dtype = dtype
        self.is_array = is_array
        self.array_bounds = array_bounds  # List of (lower, upper) tuples for each dimension
        self.is_constant = is_constant

class ConstantDeclaration(ASTNode):
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value

class Assignment(ASTNode):
    def __init__(self, identifier, expression, index=None):
        self.identifier = identifier
        self.expression = expression
        self.index = index  # For array assignments

class ArrayAccess(ASTNode):
    def __init__(self, identifier, indices):
        self.identifier = identifier
        self.indices = indices  # List of index expressions

class IfStatement(ASTNode):
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

class CaseStatement(ASTNode):
    def __init__(self, expression, cases, otherwise=None):
        self.expression = expression
        self.cases = cases  # List of (value_list, statements) tuples
        self.otherwise = otherwise

class ForLoop(ASTNode):
    def __init__(self, variable, start_value, end_value, body, step_value=None):
        self.variable = variable
        self.start_value = start_value
        self.end_value = end_value
        self.step_value = step_value
        self.body = body

class WhileLoop(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class RepeatLoop(ASTNode):
    def __init__(self, body, condition):
        self.body = body
        self.condition = condition

class ProcedureDeclaration(ASTNode):
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters  # List of (name, type, pass_mode) tuples
        self.body = body

class FunctionDeclaration(ASTNode):
    def __init__(self, name, parameters, return_type, body):
        self.name = name
        self.parameters = parameters
        self.return_type = return_type
        self.body = body

class ProcedureCall(ASTNode):
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

class FunctionCall(ASTNode):
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

class ReturnStatement(ASTNode):
    def __init__(self, expression):
        self.expression = expression

class Output(ASTNode):
    def __init__(self, expressions):
        self.expressions = expressions

class Input(ASTNode):
    def __init__(self, variable):
        self.variable = variable

class BinaryOp(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class Literal(ASTNode):
    def __init__(self, value, literal_type=None):
        self.value = value
        self.literal_type = literal_type  # 'INTEGER', 'REAL', 'STRING', 'CHAR', 'BOOLEAN'

class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name

class UnaryOp(ASTNode):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

# New AST Nodes for Complete 9618 Support

class TypeDeclaration(ASTNode):
        # TYPE...ENDTYPE user-defined record type
    def __init__(self, name, fields):
        self.name = name
        self.fields = fields  # List of (field_name, field_type) tuples

class RecordFieldAccess(ASTNode):
        # Accessing a field in a record (e.g., Person.Name)
    def __init__(self, record, field):
        self.record = record  # Identifier or expression
        self.field = field    # Field name

class FileOpen(ASTNode):
        # OPENFILE statement
    def __init__(self, filename, mode):
        self.filename = filename  # String expression
        self.mode = mode          # READ, WRITE, APPEND, RANDOM

class FileClose(ASTNode):
        # CLOSEFILE statement
    def __init__(self, filename):
        self.filename = filename

class FileRead(ASTNode):
        # READFILE statement
    def __init__(self, filename, variable):
        self.filename = filename
        self.variable = variable

class FileWrite(ASTNode):
        # WRITEFILE statement
    def __init__(self, filename, expression):
        self.filename = filename
        self.expression = expression

class FileSeek(ASTNode):
        # SEEK statement for random access
    def __init__(self, filename, address):
        self.filename = filename
        self.address = address

class GetRecord(ASTNode):
        # GETRECORD statement
    def __init__(self, filename, variable):
        self.filename = filename
        self.variable = variable

class PutRecord(ASTNode):
        # PUTRECORD statement
    def __init__(self, filename, variable):
        self.filename = filename
        self.variable = variable

class BuiltInFunctionCall(ASTNode):
        # Call to a built-in function like LENGTH, MID, etc.
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

class Parser:
    def __init__(self, tokens: List[Token]) -> None:
        self.tokens: List[Token] = tokens
        self.pos: int = 0
        self.current_token: Token = self.tokens[0] if self.tokens else Token(TokenType.EOF, None, 0, 0)

    def eat(self, token_type: TokenType) -> None:
        if self.current_token.type == token_type:
            self.advance()
        else:
            raise SyntaxError(f"Expected {token_type.name}, but found {self.current_token.type.name}", 
                              self.current_token.line, self.current_token.column)

    def advance(self) -> None:
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = Token(TokenType.EOF, None, 0, 0)

    def parse(self) -> Program:
        statements: List[Any] = []
        while self.current_token.type != TokenType.EOF:
            statements.append(self.statement())
        return Program(statements)

    def statement(self) -> Any:
        if self.current_token.type == TokenType.DECLARE:
            return self.declaration()
        elif self.current_token.type == TokenType.CONSTANT:
            return self.constant_declaration()
        elif self.current_token.type == TokenType.TYPE:
            return self.type_declaration()
        elif self.current_token.type == TokenType.PROCEDURE:
            return self.procedure_declaration()
        elif self.current_token.type == TokenType.FUNCTION:
            return self.function_declaration()
        elif self.current_token.type == TokenType.RETURN:
            return self.return_statement()
        elif self.current_token.type == TokenType.CALL:
            return self.procedure_call()
        elif self.current_token.type == TokenType.IDENTIFIER:
            # Could be assignment, array assignment, or function call
            return self.assignment_or_call()
        elif self.current_token.type == TokenType.IF:
            return self.if_statement()
        elif self.current_token.type == TokenType.CASE:
            return self.case_statement()
        elif self.current_token.type == TokenType.FOR:
            return self.for_loop()
        elif self.current_token.type == TokenType.WHILE:
            return self.while_loop()
        elif self.current_token.type == TokenType.REPEAT:
            return self.repeat_loop()
        elif self.current_token.type == TokenType.OUTPUT:
            return self.output_statement()
        elif self.current_token.type == TokenType.INPUT:
            return self.input_statement()
        # File Operations
        elif self.current_token.type == TokenType.OPENFILE:
            return self.file_open()
        elif self.current_token.type == TokenType.CLOSEFILE:
            return self.file_close()
        elif self.current_token.type == TokenType.READFILE:
            return self.file_read()
        elif self.current_token.type == TokenType.WRITEFILE:
            return self.file_write()
        elif self.current_token.type == TokenType.SEEK:
            return self.file_seek()
        elif self.current_token.type == TokenType.GETRECORD:
            return self.get_record()
        elif self.current_token.type == TokenType.PUTRECORD:
            return self.put_record()
        else:
            raise SyntaxError(
                f"Unexpected token '{self.current_token.value}' in statement", 
                self.current_token.line, 
                self.current_token.column,
                "Expected a statement keyword like DECLARE, IF, FOR, WHILE, OUTPUT, INPUT, TYPE, or file operation"
            )

    def declaration(self):
        self.eat(TokenType.DECLARE)
        identifier = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.COLON)
        
        # Check if it's an array
        is_array = False
        array_bounds = []
        
        if self.current_token.type == TokenType.ARRAY:
            is_array = True
            self.eat(TokenType.ARRAY)
            self.eat(TokenType.LBRACKET)
            
            # Parse array bounds (e.g., [1:10, 1:5] for 2D array)
            while True:
                lower = self.expression()
                self.eat(TokenType.COLON)
                upper = self.expression()
                array_bounds.append((lower, upper))
                
                if self.current_token.type == TokenType.COMMA:
                    self.eat(TokenType.COMMA)
                else:
                    break
            
            self.eat(TokenType.RBRACKET)
            self.eat(TokenType.OF)
        
        # Get the data type
        dtype = self.current_token.value
        valid_types = ['INTEGER', 'REAL', 'STRING', 'CHAR', 'BOOLEAN', 'DATE']
        if dtype.upper() not in valid_types:
            raise SyntaxError(
                f"Invalid data type '{dtype}'",
                self.current_token.line,
                self.current_token.column,
                f"Valid types are: {', '.join(valid_types)}"
            )
        self.eat(TokenType.IDENTIFIER)
        
        return Declaration(identifier, dtype, is_array, array_bounds if is_array else None)

    def assignment_or_call(self):
        identifier = self.current_token.value
        line = self.current_token.line
        self.eat(TokenType.IDENTIFIER)
        
        # Check for array indexing
        if self.current_token.type == TokenType.LBRACKET:
            indices = []
            self.eat(TokenType.LBRACKET)
            indices.append(self.expression())
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                indices.append(self.expression())
            self.eat(TokenType.RBRACKET)
            
            # Array assignment
            if self.current_token.type == TokenType.ASSIGN:
                self.eat(TokenType.ASSIGN)
                expr = self.expression()
                return Assignment(identifier, expr, indices)
            else:
                raise SyntaxError(
                    f"Expected assignment operator '<-' after array index",
                    self.current_token.line,
                    self.current_token.column,
                    "Use '<-' to assign a value to the array element"
                )
        
        # Check for function call (has parentheses but no assignment)
        elif self.current_token.type == TokenType.LPAREN:
            arguments = []
            self.eat(TokenType.LPAREN)
            if self.current_token.type != TokenType.RPAREN:
                arguments.append(self.expression())
                while self.current_token.type == TokenType.COMMA:
                    self.eat(TokenType.COMMA)
                    arguments.append(self.expression())
            self.eat(TokenType.RPAREN)
            return ProcedureCall(identifier, arguments)
        
        # Regular assignment
        elif self.current_token.type == TokenType.ASSIGN:
            self.eat(TokenType.ASSIGN)
            expr = self.expression()
            return Assignment(identifier, expr)
        
        else:
            raise SyntaxError(
                f"Expected '<-' or '[' after identifier '{identifier}'",
                self.current_token.line,
                self.current_token.column,
                "Use '<-' for assignment or '[]' for array access"
            )
    
    def assignment(self):
        identifier = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.ASSIGN)
        expr = self.expression()
        return Assignment(identifier, expr)
    
    def constant_declaration(self):
        self.eat(TokenType.CONSTANT)
        identifier = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.EQ)
        value = self.expression()
        return ConstantDeclaration(identifier, value)
    
    def procedure_declaration(self):
        self.eat(TokenType.PROCEDURE)
        name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        
        parameters = []
        self.eat(TokenType.LPAREN)
        if self.current_token.type != TokenType.RPAREN:
            parameters = self.parse_parameters()
        self.eat(TokenType.RPAREN)
        
        body = []
        while self.current_token.type not in (
            TokenType.ENDPROCEDURE, TokenType.PROCEDURE, TokenType.FUNCTION, TokenType.EOF
        ):
            body.append(self.statement())

        if self.current_token.type == TokenType.ENDPROCEDURE:
            self.eat(TokenType.ENDPROCEDURE)

        return ProcedureDeclaration(name, parameters, body)
    
    def function_declaration(self):
        self.eat(TokenType.FUNCTION)
        name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        
        parameters = []
        self.eat(TokenType.LPAREN)
        if self.current_token.type != TokenType.RPAREN:
            parameters = self.parse_parameters()
        self.eat(TokenType.RPAREN)
        
        self.eat(TokenType.RETURNS)
        return_type = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        
        body = []
        while self.current_token.type not in (
            TokenType.ENDFUNCTION, TokenType.PROCEDURE, TokenType.FUNCTION, TokenType.EOF
        ):
            body.append(self.statement())

        if self.current_token.type == TokenType.ENDFUNCTION:
            self.eat(TokenType.ENDFUNCTION)

        return FunctionDeclaration(name, parameters, return_type, body)
    
    def parse_parameters(self) -> List[Tuple[str, str, str]]:
        parameters = []
        
        while True:
            # Check for BYREF or BYVAL
            pass_mode = 'BYVAL'  # Default
            if self.current_token.type == TokenType.BYREF:
                pass_mode = 'BYREF'
                self.eat(TokenType.BYREF)
            elif self.current_token.type == TokenType.BYVAL:
                pass_mode = 'BYVAL'
                self.eat(TokenType.BYVAL)
            
            param_name = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
            self.eat(TokenType.COLON)
            param_type = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
            
            parameters.append((param_name, param_type, pass_mode))
            
            if self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
            else:
                break
        
        return parameters
    
    def procedure_call(self):
        self.eat(TokenType.CALL)
        name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        
        arguments = []
        self.eat(TokenType.LPAREN)
        if self.current_token.type != TokenType.RPAREN:
            arguments.append(self.expression())
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                arguments.append(self.expression())
        self.eat(TokenType.RPAREN)
        
        return ProcedureCall(name, arguments)
    
    def return_statement(self):
        token = self.current_token
        self.eat(TokenType.RETURN)
        expr = self.expression()
        node = ReturnStatement(expr)
        node.line = token.line
        return node
    
    def case_statement(self):
        self.eat(TokenType.CASE)
        self.eat(TokenType.OF)
        expression = self.expression()
        
        cases = []
        while self.current_token.type not in (TokenType.OTHERWISE, TokenType.ENDCASE, TokenType.EOF):
            # Parse case values (can be multiple values separated by commas)
            values = [self.expression()]
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                # Check if next token is a colon (end of values list)
                if self.current_token.type == TokenType.COLON:
                    break
                values.append(self.expression())
            
            self.eat(TokenType.COLON)
            
            statements = []
            while self.current_token.type not in (
                TokenType.OTHERWISE, TokenType.ENDCASE, TokenType.EOF,
                TokenType.INTEGER, TokenType.STRING, TokenType.REAL,
                TokenType.CHAR, TokenType.TRUE, TokenType.FALSE,
            ):
                statements.append(self.statement())

            cases.append((values, statements))
        
        otherwise = None
        if self.current_token.type == TokenType.OTHERWISE:
            self.eat(TokenType.OTHERWISE)
            self.eat(TokenType.COLON)
            otherwise = []
            # Parse statements until ENDCASE
            while self.current_token.type not in (TokenType.ENDCASE, TokenType.EOF):
                otherwise.append(self.statement())
        
        self.eat(TokenType.ENDCASE)
        return CaseStatement(expression, cases, otherwise)

    def if_statement(self):
        self.eat(TokenType.IF)
        condition = self.expression()
        self.eat(TokenType.THEN)
        
        then_branch = []
        while self.current_token.type not in (TokenType.ELSE, TokenType.ENDIF, TokenType.EOF):
            then_branch.append(self.statement())
            
        else_branch = None
        if self.current_token.type == TokenType.ELSE:
            self.eat(TokenType.ELSE)
            else_branch = []
            while self.current_token.type not in (TokenType.ENDIF, TokenType.EOF):
                else_branch.append(self.statement())
                
        self.eat(TokenType.ENDIF)
        return IfStatement(condition, then_branch, else_branch)

    def for_loop(self):
        self.eat(TokenType.FOR)
        variable = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.ASSIGN)
        start_value = self.expression()
        self.eat(TokenType.TO)
        end_value = self.expression()
        
        # Optional STEP clause
        step_value = None
        if self.current_token.type == TokenType.STEP:
            self.eat(TokenType.STEP)
            step_value = self.expression()
        
        body = []
        while self.current_token.type not in (TokenType.NEXT, TokenType.EOF):
            body.append(self.statement())
            
        self.eat(TokenType.NEXT)
        if self.current_token.type == TokenType.IDENTIFIER:
            next_var = self.current_token.value
            if next_var != variable:
                raise SyntaxError(
                    f"NEXT variable '{next_var}' does not match FOR variable '{variable}'",
                    self.current_token.line,
                    self.current_token.column,
                    f"Use NEXT {variable} to close the loop"
                )
            self.eat(TokenType.IDENTIFIER)

        return ForLoop(variable, start_value, end_value, body, step_value)

    def while_loop(self):
        self.eat(TokenType.WHILE)
        condition = self.expression()
        self.eat(TokenType.DO)
        
        body = []
        while self.current_token.type not in (TokenType.ENDWHILE, TokenType.EOF):
            body.append(self.statement())
            
        self.eat(TokenType.ENDWHILE)
        return WhileLoop(condition, body)

    def repeat_loop(self):
        self.eat(TokenType.REPEAT)
        
        body = []
        while self.current_token.type not in (TokenType.UNTIL, TokenType.EOF):
            body.append(self.statement())
            
        self.eat(TokenType.UNTIL)
        condition = self.expression()
        return RepeatLoop(body, condition)

    def output_statement(self):
        token = self.current_token
        self.eat(TokenType.OUTPUT)
        expressions = [self.expression()]
        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            expressions.append(self.expression())
        node = Output(expressions)
        node.line = token.line
        return node

    def input_statement(self):
        self.eat(TokenType.INPUT)
        variable = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        return Input(variable)

    def expression(self) -> Any:
        return self.logic_or()

    def logic_or(self):
        node = self.logic_and()
        while self.current_token.type == TokenType.OR:
            token = self.current_token
            self.eat(TokenType.OR)
            node = BinaryOp(left=node, operator=token, right=self.logic_and())
        return node

    def logic_and(self):
        node = self.comparison()
        while self.current_token.type == TokenType.AND:
            token = self.current_token
            self.eat(TokenType.AND)
            node = BinaryOp(left=node, operator=token, right=self.comparison())
        return node

    def comparison(self):
        node = self.additive()
        while self.current_token.type in (TokenType.EQ, TokenType.NEQ, TokenType.LT, TokenType.GT, TokenType.LTE, TokenType.GTE):
            token = self.current_token
            self.eat(token.type)
            node = BinaryOp(left=node, operator=token, right=self.additive())
        return node

    def additive(self):
        node = self.multiplicative()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            self.eat(token.type)
            node = BinaryOp(left=node, operator=token, right=self.multiplicative())
        return node

    def multiplicative(self):
        node = self.unary()
        while self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.DIV_INT, TokenType.MOD):
            token = self.current_token
            self.eat(token.type)
            node = BinaryOp(left=node, operator=token, right=self.unary())
        return node

    def unary(self):
        token = self.current_token
        if token.type == TokenType.NOT:
            self.eat(TokenType.NOT)
            return UnaryOp(operator=token, operand=self.unary())
        elif token.type == TokenType.MINUS:
            self.eat(TokenType.MINUS)
            return UnaryOp(operator=token, operand=self.unary())
        return self.primary()

    def primary(self) -> Any:
        token = self.current_token
        if token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            node = Literal(token.value, 'INTEGER')
            node.line = token.line
            return node
        elif token.type == TokenType.REAL:
            self.eat(TokenType.REAL)
            node = Literal(token.value, 'REAL')
            node.line = token.line
            return node
        elif token.type == TokenType.STRING:
            self.eat(TokenType.STRING)
            node = Literal(token.value, 'STRING')
            node.line = token.line
            return node
        elif token.type == TokenType.CHAR:
            self.eat(TokenType.CHAR)
            node = Literal(token.value, 'CHAR')
            node.line = token.line
            return node
        elif token.type == TokenType.TRUE:
            self.eat(TokenType.TRUE)
            node = Literal(True, 'BOOLEAN')
            node.line = token.line
            return node
        elif token.type == TokenType.FALSE:
            self.eat(TokenType.FALSE)
            node = Literal(False, 'BOOLEAN')
            node.line = token.line
            return node
        elif token.type == TokenType.BUILTIN_FUNC:
            # Built-in function call
            func_name = token.value
            func_line = token.line
            self.eat(TokenType.BUILTIN_FUNC)
            arguments = []
            self.eat(TokenType.LPAREN)
            if self.current_token.type != TokenType.RPAREN:
                arguments.append(self.expression())
                while self.current_token.type == TokenType.COMMA:
                    self.eat(TokenType.COMMA)
                    arguments.append(self.expression())
            self.eat(TokenType.RPAREN)
            node = BuiltInFunctionCall(func_name, arguments)
            node.line = func_line
            return node
        elif token.type == TokenType.IDENTIFIER:
            identifier = token.value
            id_line = token.line
            self.eat(TokenType.IDENTIFIER)
            
            # Check for record field access (e.g., Person.Name)
            if self.current_token.type == TokenType.DOT:
                self.eat(TokenType.DOT)
                field_name = self.current_token.value
                self.eat(TokenType.IDENTIFIER)
                node = RecordFieldAccess(Identifier(identifier), field_name)
                node.line = id_line
                return node
            
            # Check for array access
            elif self.current_token.type == TokenType.LBRACKET:
                indices = []
                self.eat(TokenType.LBRACKET)
                indices.append(self.expression())
                while self.current_token.type == TokenType.COMMA:
                    self.eat(TokenType.COMMA)
                    indices.append(self.expression())
                self.eat(TokenType.RBRACKET)
                node = ArrayAccess(identifier, indices)
                node.line = id_line
                return node
            
            # Check for function call
            elif self.current_token.type == TokenType.LPAREN:
                arguments = []
                self.eat(TokenType.LPAREN)
                if self.current_token.type != TokenType.RPAREN:
                    arguments.append(self.expression())
                    while self.current_token.type == TokenType.COMMA:
                        self.eat(TokenType.COMMA)
                        arguments.append(self.expression())
                self.eat(TokenType.RPAREN)
                node = FunctionCall(identifier, arguments)
                node.line = id_line
                return node
            
            else:
                node = Identifier(identifier)
                node.line = id_line
                return node
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expression()
            self.eat(TokenType.RPAREN)
            return node
        else:
            raise SyntaxError(
                f"Unexpected token in expression: '{token.value}'", 
                token.line, 
                token.column,
                "Expected a number, string, boolean, identifier, or '('"
            )
    
    # New parsing methods for complete 9618 support
    
    def type_declaration(self):
                # Parse TYPE...ENDTYPE declaration
        self.eat(TokenType.TYPE)
        type_name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        
        fields = []
        # Parse field declarations
        while self.current_token.type != TokenType.ENDTYPE:
            if self.current_token.type == TokenType.DECLARE:
                self.eat(TokenType.DECLARE)
                field_name = self.current_token.value
                self.eat(TokenType.IDENTIFIER)
                self.eat(TokenType.COLON)
                field_type = self.current_token.value
                self.eat(TokenType.IDENTIFIER)
                fields.append((field_name, field_type))
            else:
                break
        
        self.eat(TokenType.ENDTYPE)
        return TypeDeclaration(type_name, fields)
    
    def file_open(self):
                # Parse OPENFILE statement
        self.eat(TokenType.OPENFILE)
        filename = self.expression()
        
        # Expect FOR keyword
        if self.current_token.value.upper() == 'FOR':
            self.eat(TokenType.IDENTIFIER)  # FOR is not a keyword in our list
        
        # Parse file mode
        mode = None
        if self.current_token.type in (TokenType.READ, TokenType.WRITE, TokenType.APPEND, TokenType.RANDOM):
            mode = self.current_token.value
            self.eat(self.current_token.type)
        else:
            raise SyntaxError(
                f"Expected file mode (READ, WRITE, APPEND, or RANDOM), but got {self.current_token.value}",
                self.current_token.line,
                self.current_token.column,
                "Use READ, WRITE, APPEND, or RANDOM after FOR"
            )
        
        return FileOpen(filename, mode)
    
    def file_close(self):
                # Parse CLOSEFILE statement
        self.eat(TokenType.CLOSEFILE)
        filename = self.expression()
        return FileClose(filename)
    
    def file_read(self):
                # Parse READFILE statement
        self.eat(TokenType.READFILE)
        filename = self.expression()
        self.eat(TokenType.COMMA)
        variable = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        return FileRead(filename, variable)
    
    def file_write(self):
                # Parse WRITEFILE statement
        self.eat(TokenType.WRITEFILE)
        filename = self.expression()
        self.eat(TokenType.COMMA)
        expression = self.expression()
        return FileWrite(filename, expression)
    
    def file_seek(self):
                # Parse SEEK statement
        self.eat(TokenType.SEEK)
        filename = self.expression()
        self.eat(TokenType.COMMA)
        address = self.expression()
        return FileSeek(filename, address)
    
    def get_record(self):
                # Parse GETRECORD statement
        self.eat(TokenType.GETRECORD)
        filename = self.expression()
        self.eat(TokenType.COMMA)
        variable = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        return GetRecord(filename, variable)
    
    def put_record(self):
                # Parse PUTRECORD statement
        self.eat(TokenType.PUTRECORD)
        filename = self.expression()
        self.eat(TokenType.COMMA)
        variable = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        return PutRecord(filename, variable)

