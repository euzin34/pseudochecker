#
# Semantic Analyzer for CIE 9618 Pseudocode
# Performs semantic analysis including:
# - Symbol table management
# - Type checking
# - Scope management
# - Variable declaration validation
# - Function return type verification
# - Logic validation

from src.parser import *
from src.errors import SemanticError, TypeError, WarningError, ErrorCollector
from src.builtin_functions import BuiltInFunctionRegistry
from src.constants import VALID_DATA_TYPES
from src.tokenizer import TokenType

COMPARISON_OPS = {
    TokenType.EQ, TokenType.NEQ, TokenType.LT,
    TokenType.GT, TokenType.LTE, TokenType.GTE,
}
LOGICAL_OPS = {TokenType.AND, TokenType.OR}


class Symbol:
        # Represents a symbol in the symbol table
    def __init__(self, name, symbol_type, data_type=None, value=None, line=None):
        self.name = name
        self.symbol_type = symbol_type  # 'variable', 'constant', 'function', 'procedure', 'type', 'parameter'
        self.data_type = data_type
        self.value = value
        self.line = line
        self.is_initialized = False
        self.is_used = False
        
        # For functions/procedures
        self.parameters = []
        self.return_type = None
        
        # For arrays
        self.is_array = False
        self.array_bounds = None


class Scope:
        # Represents a scope with its own symbol table
    def __init__(self, name, scope_type, parent=None):
        self.name = name
        self.scope_type = scope_type  # 'global', 'function', 'procedure', 'block'
        self.parent = parent
        self.symbols = {}
        self.children = []
        
        if parent:
            parent.children.append(self)
    
    def declare(self, symbol):
                # Declare a symbol in this scope
        if symbol.name in self.symbols:
            return False  # Already declared
        self.symbols[symbol.name] = symbol
        return True
    
    def lookup(self, name, recursive=True):
                # Look up a symbol in this scope and parent scopes
        if name in self.symbols:
            return self.symbols[name]
        if recursive and self.parent:
            return self.parent.lookup(name)
        return None
    
    def lookup_local(self, name):
                # Look up a symbol only in this scope
        return self.symbols.get(name)


class SemanticAnalyzer:
        #
    #     Semantic analyzer for 9618 pseudocode
    #     Validates logic, types, and declarations
    #
    
    def __init__(self, ast):
        self.ast = ast
        self.current_scope = Scope('global', 'global')
        self.global_scope = self.current_scope
        self.errors = ErrorCollector()
        self.builtin_registry = BuiltInFunctionRegistry()
        
        # Track function definitions for return validation
        self.current_function = None
        self.has_return_statement = False
        
        # Track types declared
        self.user_types = {}

        # Observations collected during analysis (e.g., known OUTPUT/RETURN values)
        self.observations = []
    
    def analyze(self):
                # Perform complete semantic analysis
        try:
            self.visit(self.ast)
        except Exception as e:
            # Catch any unexpected errors during analysis
            if not isinstance(e, (SemanticError, TypeError, WarningError)):
                # Unknown error, add it as semantic error
                self.errors.add_error(
                    SemanticError(
                        f"Internal analyzer error: {str(e)}",
                        1, 1,
                        "Please report this error"
                    )
                )
        
        return self.errors
    
    def enter_scope(self, name, scope_type):
                # Enter a new scope
        self.current_scope = Scope(name, scope_type, self.current_scope)
    
    def exit_scope(self):
                # Exit current scope
        if self.current_scope.parent:
            self.current_scope = self.current_scope.parent
    
    def visit(self, node):
                # Visit a node and call appropriate visitor method
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
                # Default visitor for unknown nodes
        pass
    
    def evaluate_const(self, node):
                # Attempt to evaluate simple constant expressions at analysis time.
                # Returns (value, literal_type) or (None, None) if not evaluable.
        if node is None:
            return (None, None)

        # Literal
        if type(node).__name__ == 'Literal':
            return (node.value, node.literal_type)

        # Identifier -> check if symbol has a stored constant value
        if type(node).__name__ == 'Identifier':
            symbol = self.current_scope.lookup(node.name)
            if symbol and getattr(symbol, 'value', None) is not None:
                return (symbol.value, symbol.data_type)
            return (None, None)

        # BinaryOp: try evaluate both sides and compute
        if type(node).__name__ == 'BinaryOp':
            left_val, _ = self.evaluate_const(node.left)
            right_val, _ = self.evaluate_const(node.right)
            if left_val is None or right_val is None:
                return (None, None)
            op = getattr(node.operator, 'value', None)
            try:
                if op == '+' or op == 'PLUS':
                    return (left_val + right_val, None)
                if op == '-' or op == 'MINUS':
                    return (left_val - right_val, None)
                if op == '*' or op == 'MULTIPLY':
                    return (left_val * right_val, None)
                if op in ('/', 'DIVIDE'):
                    return (left_val / right_val, None)
                if op in ('DIV', 'DIV_INT'):
                    return (left_val // right_val, None)
                if op == 'MOD':
                    return (left_val % right_val, None)
                if op in ('=', 'EQ'):
                    return (left_val == right_val, 'BOOLEAN')
                if op in ('<>', 'NEQ'):
                    return (left_val != right_val, 'BOOLEAN')
                if op in ('<', 'LT'):
                    return (left_val < right_val, 'BOOLEAN')
                if op in ('>', 'GT'):
                    return (left_val > right_val, 'BOOLEAN')
                if op in ('<=', 'LTE'):
                    return (left_val <= right_val, 'BOOLEAN')
                if op in ('>=', 'GTE'):
                    return (left_val >= right_val, 'BOOLEAN')
            except Exception:
                return (None, None)

        # UnaryOp
        if type(node).__name__ == 'UnaryOp':
            val, _ = self.evaluate_const(node.operand)
            if val is None:
                return (None, None)
            op = getattr(node.operator, 'value', None)
            try:
                if op == '-':
                    return (-val, None)
                if op == 'NOT':
                    return (not val, 'BOOLEAN')
            except Exception:
                return (None, None)

        # Built-in function calls and others are not evaluated here
        return (None, None)

    # Visitor methods for each AST node type
    
    def visit_Program(self, node):
                # Visit program node
        for statement in node.statements:
            self.visit(statement)
    
    def visit_Declaration(self, node):
                # Visit variable declaration
        # Check if already declared in this scope
        if self.current_scope.lookup_local(node.identifier):
            self.errors.add_error(
                SemanticError(
                    f"Variable '{node.identifier}' is already declared in this scope",
                    1, 1,  # We don't have line info in AST nodes yet
                    f"Choose a different name or remove the duplicate declaration"
                )
            )
            return
        
        # Validate data type
        if node.dtype.upper() not in VALID_DATA_TYPES and node.dtype not in self.user_types:
            self.errors.add_error(
                TypeError(
                    f"Invalid data type '{node.dtype}'",
                    1, 1,
                    f"Valid types are: {', '.join(VALID_DATA_TYPES)} or declared custom types"
                )
            )
            return
        
        # Create symbol
        symbol = Symbol(node.identifier, 'variable', node.dtype.upper())
        symbol.is_array = node.is_array
        symbol.array_bounds = node.array_bounds
        
        # For constants, mark as initialized
        if node.is_constant:
            symbol.is_initialized = True
            symbol.symbol_type = 'constant'
        
        self.current_scope.declare(symbol)
    
    def visit_ConstantDeclaration(self, node):
                # Visit constant declaration
        if self.current_scope.lookup_local(node.identifier):
            self.errors.add_error(
                SemanticError(
                    f"Constant '{node.identifier}' is already declared in this scope",
                    1, 1,
                    "Constants cannot be redeclared"
                )
            )
            return
        
        # Visit the value expression to determine its type
        value_type = self.visit(node.value)
        
        # Create symbol
        symbol = Symbol(node.identifier, 'constant', value_type)
        symbol.is_initialized = True
        # Try to evaluate constant value to a primitive (if possible)
        const_val, _ = self.evaluate_const(node.value)
        if const_val is not None:
            symbol.value = const_val
        else:
            # Fallback to storing the AST node so we might evaluate later
            symbol.value = node.value
        
        self.current_scope.declare(symbol)
    
    def visit_Assignment(self, node):
                # Visit assignment statement
        if node.index:
            symbol = self.current_scope.lookup(node.identifier)
            if not symbol:
                self.errors.add_error(
                    SemanticError(
                        f"Array '{node.identifier}' is not declared",
                        1, 1,
                        f"Declare '{node.identifier}' as ARRAY before assignment"
                    )
                )
                return
            if not symbol.is_array:
                self.errors.add_error(
                    SemanticError(
                        f"'{node.identifier}' is not an array",
                        1, 1,
                        "Use array assignment only on ARRAY variables"
                    )
                )
                return
            for idx in node.index:
                idx_type = self.visit(idx)
                if idx_type and idx_type != 'INTEGER':
                    self.errors.add_error(
                        TypeError(
                            f"Array index must be INTEGER, got {idx_type}",
                            1, 1,
                            "Use an integer index"
                        )
                    )
            expr_type = self.visit(node.expression)
            if symbol.data_type and expr_type:
                if not self.types_compatible(symbol.data_type, expr_type):
                    self.errors.add_error(
                        TypeError(
                            f"Type mismatch: Cannot assign {expr_type} to array of {symbol.data_type}",
                            1, 1,
                            f"Expression must be of type {symbol.data_type}"
                        )
                    )
            symbol.is_initialized = True
            # Try to evaluate array element assignment - not tracked per-element currently
            return

        symbol = self.current_scope.lookup(node.identifier)
        if not symbol:
            self.errors.add_error(
                SemanticError(
                    f"Variable '{node.identifier}' is used before being declared",
                    1, 1,
                    f"Add 'DECLARE {node.identifier} : <TYPE>' before using it"
                )
            )
            return
        
        # Check if trying to assign to a constant
        if symbol.symbol_type == 'constant':
            self.errors.add_error(
                SemanticError(
                    f"Cannot assign to constant '{node.identifier}'",
                    1, 1,
                    "Constants cannot be modified after declaration"
                )
            )
            return
        
        # Get type of expression
        expr_type = self.visit(node.expression)
        
        # Check type compatibility
        if symbol.data_type and expr_type:
            if not self.types_compatible(symbol.data_type, expr_type):
                self.errors.add_error(
                    TypeError(
                        f"Type mismatch: Cannot assign {expr_type} to {symbol.data_type}",
                        1, 1,
                        f"Expression must be of type {symbol.data_type}"
                    )
                )
        
        # Mark as initialized
        symbol.is_initialized = True
        # Attempt to statically evaluate the assigned expression and store value for later observations
        const_val, const_type = self.evaluate_const(node.expression)
        if const_val is not None:
            symbol.value = const_val
    
    def visit_TypeDeclaration(self, node):
                # Visit type declaration
        if node.name in self.user_types:
            self.errors.add_error(
                SemanticError(
                    f"Type '{node.name}' is already declared",
                    1, 1,
                    "Choose a different name for the type"
                )
            )
            return
        
        self.user_types[node.name] = {name: dtype for name, dtype in node.fields}
    
    def visit_ProcedureDeclaration(self, node):
                # Visit procedure declaration
        # Declare procedure in current scope
        symbol = Symbol(node.name, 'procedure')
        symbol.parameters = node.parameters
        
        if not self.current_scope.declare(symbol):
            self.errors.add_error(
                SemanticError(
                    f"Procedure '{node.name}' is already declared",
                    1, 1,
                    "Choose a different name"
                )
            )
        
        # Enter procedure scope
        self.enter_scope(node.name, 'procedure')
        
        # Declare parameters
        for param_name, param_type, pass_mode in node.parameters:
            param_symbol = Symbol(param_name, 'parameter', param_type.upper())
            param_symbol.is_initialized = True  # Parameters are initialized by caller
            self.current_scope.declare(param_symbol)
        
        # Visit procedure body
        for statement in node.body:
            self.visit(statement)
        
        # Exit procedure scope
        self.exit_scope()
    
    def visit_FunctionDeclaration(self, node):
                # Visit function declaration
        # Declare function in current scope
        symbol = Symbol(node.name, 'function', node.return_type.upper())
        symbol.parameters = node.parameters
        symbol.return_type = node.return_type.upper()
        
        if not self.current_scope.declare(symbol):
            self.errors.add_error(
                SemanticError(
                    f"Function '{node.name}' is already declared",
                    1, 1,
                    "Choose a different name"
                )
            )
        
        # Enter function scope
        self.enter_scope(node.name, 'function')
        self.current_function = node.name
        self.has_return_statement = False
        
        # Declare parameters
        for param_name, param_type, pass_mode in node.parameters:
            param_symbol = Symbol(param_name, 'parameter', param_type.upper())
            param_symbol.is_initialized = True
            self.current_scope.declare(param_symbol)
        
        # Visit function body
        for statement in node.body:
            self.visit(statement)
        
        # Check if function has return statement
        if not self.has_return_statement:
            self.errors.add_error(
                SemanticError(
                    f"Function '{node.name}' must return a value of type {node.return_type}",
                    1, 1,
                    f"Add 'RETURN <expression>' before the end of the function"
                )
            )
        
        # Exit function scope
        self.exit_scope()
        self.current_function = None
        self.has_return_statement = False
    
    def visit_ReturnStatement(self, node):
                # Visit return statement
        # Mark that we found a return
        self.has_return_statement = True
        
        # Get expression type
        if node.expression:
            expr_type = self.visit(node.expression)
            
            # If we can evaluate the return expression statically, record it
            val, _ = self.evaluate_const(node.expression)
            if val is not None:
                line = getattr(node, 'line', None) or getattr(node.expression, 'line', None)
                self.observations.append({
                    'kind': 'return',
                    'line': line,
                    'value': val,
                    'message': f"Return value: {val}",
                })
            
            # Check if in a function
            if self.current_function:
                func_symbol = self.global_scope.lookup(self.current_function)
                if func_symbol and func_symbol.return_type:
                    if not self.types_compatible(func_symbol.return_type, expr_type):
                        self.errors.add_error(
                            TypeError(
                                f"Return type mismatch: Function expects {func_symbol.return_type} but returns {expr_type}",
                                1, 1,
                                f"Return an expression of type {func_symbol.return_type}"
                            )
                        )

    def visit_FunctionCall(self, node):
                # Visit function call
        # Check if function is declared
        symbol = self.current_scope.lookup(node.name)
        if not symbol:
            self.errors.add_error(
                SemanticError(
                    f"Function '{node.name}' is not defined",
                    1, 1,
                    "Define the function before calling it"
                )
            )
            return None
        
        # Check parameter count
        if len(node.arguments) != len(symbol.parameters):
            self.errors.add_error(
                SemanticError(
                    f"Function '{node.name}' expects {len(symbol.parameters)} arguments but got {len(node.arguments)}",
                    1, 1,
                    f"Provide exactly {len(symbol.parameters)} arguments"
                )
            )
        
        # Visit arguments
        for arg in node.arguments:
            self.visit(arg)
        
        return symbol.return_type
    
    def visit_BuiltInFunctionCall(self, node):
                # Visit built-in function call
        if not self.builtin_registry.is_builtin(node.name):
            self.errors.add_error(
                SemanticError(
                    f"Unknown built-in function '{node.name}'",
                    1, 1,
                    "Check the function name spelling"
                )
            )
            return None
        
        # Get argument types
        arg_types = []
        for arg in node.arguments:
            arg_type = self.visit(arg)
            arg_types.append(('', arg_type) if arg_type else ('', 'ANY'))
        
        # Validate call
        is_valid, error_msg, return_type = self.builtin_registry.validate_call(node.name, arg_types)
        if not is_valid:
            self.errors.add_error(
                SemanticError(error_msg, 1, 1, "Check function parameters")
            )
        
        return return_type
    
    def visit_Identifier(self, node):
                # Visit identifier
        symbol = self.current_scope.lookup(node.name)
        if not symbol:
            self.errors.add_error(
                SemanticError(
                    f"Variable '{node.name}' is used before being declared",
                    1, 1,
                    f"Declare '{node.name}' before using it"
                )
            )
            return None
        
        # Mark as used
        symbol.is_used = True
        
        # Warn if used before initialization
        if not symbol.is_initialized:
            self.errors.add_error(
                WarningError(
                    f"Variable '{node.name}' may be used before initialization",
                    1, 1,
                    "Assign a value before using the variable"
                )
            )
        
        return symbol.data_type
    
    def visit_Literal(self, node):
                # Visit literal value
        return node.literal_type
    
    def visit_BinaryOp(self, node):
                # Visit binary operation
        op_type = node.operator.type
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if op_type in COMPARISON_OPS or op_type in LOGICAL_OPS:
            return 'BOOLEAN'

        if left_type and right_type:
            if left_type != right_type:
                if set([left_type, right_type]) == {'INTEGER', 'REAL'}:
                    return 'REAL'
                self.errors.add_error(
                    TypeError(
                        f"Type mismatch in operation: {left_type} and {right_type}",
                        1, 1,
                        "Operands must be of compatible types"
                    )
                )

        return left_type or right_type

    def visit_UnaryOp(self, node):
                # Visit unary operation
        operand_type = self.visit(node.operand)
        if node.operator.type == TokenType.NOT:
            if operand_type and operand_type != 'BOOLEAN':
                self.errors.add_error(
                    TypeError(
                        f"NOT operand must be BOOLEAN, got {operand_type}",
                        1, 1,
                        "Use a boolean expression with NOT"
                    )
                )
            return 'BOOLEAN'
        return operand_type
    
    def visit_IfStatement(self, node):
                # Visit if statement
        # Visit condition
        cond_type = self.visit(node.condition)
        if cond_type and cond_type != 'BOOLEAN':
            self.errors.add_error(
                TypeError(
                    f"IF condition must be BOOLEAN, got {cond_type}",
                    1, 1,
                    "Use a comparison or boolean expression"
                )
            )
        
        # Visit branches
        for stmt in node.then_branch:
            self.visit(stmt)
        if node.else_branch:
            for stmt in node.else_branch:
                self.visit(stmt)
    
    def visit_WhileLoop(self, node):
                # Visit while loop
        cond_type = self.visit(node.condition)
        if cond_type and cond_type != 'BOOLEAN':
            self.errors.add_error(
                TypeError(
                    f"WHILE condition must be BOOLEAN, got {cond_type}",
                    1, 1,
                    "Use a comparison or boolean expression"
                )
            )
        
        for stmt in node.body:
            self.visit(stmt)
    
    def visit_ForLoop(self, node):
                # Visit for loop
        symbol = self.current_scope.lookup(node.variable)
        if not symbol:
            # 9618 FOR often uses the control variable without a prior DECLARE
            loop_symbol = Symbol(node.variable, 'variable', 'INTEGER')
            loop_symbol.is_initialized = True
            self.current_scope.declare(loop_symbol)
        elif symbol.data_type != 'INTEGER':
            self.errors.add_error(
                TypeError(
                    f"Loop variable must be INTEGER, got {symbol.data_type}",
                    1, 1,
                    "Use an INTEGER variable for the loop"
                )
            )

        self.visit(node.start_value)
        self.visit(node.end_value)
        if node.step_value:
            self.visit(node.step_value)

        for stmt in node.body:
            self.visit(stmt)

    def visit_RepeatLoop(self, node):
                # Visit repeat-until loop
        for stmt in node.body:
            self.visit(stmt)
        cond_type = self.visit(node.condition)
        if cond_type and cond_type != 'BOOLEAN':
            self.errors.add_error(
                TypeError(
                    f"UNTIL condition must be BOOLEAN, got {cond_type}",
                    1, 1,
                    "Use a comparison or boolean expression after UNTIL"
                )
            )

    def visit_CaseStatement(self, node):
                # Visit case statement
        self.visit(node.expression)
        for values, statements in node.cases:
            for val in values:
                self.visit(val)
            for stmt in statements:
                self.visit(stmt)
        if node.otherwise:
            for stmt in node.otherwise:
                self.visit(stmt)

    def visit_ProcedureCall(self, node):
                # Visit procedure call
        symbol = self.current_scope.lookup(node.name)
        if not symbol:
            self.errors.add_error(
                SemanticError(
                    f"Procedure '{node.name}' is not defined",
                    1, 1,
                    "Define the procedure before calling it"
                )
            )
            return
        if symbol.symbol_type != 'procedure':
            self.errors.add_error(
                SemanticError(
                    f"'{node.name}' is not a procedure",
                    1, 1,
                    "Use CALL only with procedures"
                )
            )
            return
        if len(node.arguments) != len(symbol.parameters):
            self.errors.add_error(
                SemanticError(
                    f"Procedure '{node.name}' expects {len(symbol.parameters)} arguments but got {len(node.arguments)}",
                    1, 1,
                    f"Provide exactly {len(symbol.parameters)} arguments"
                )
            )
        for arg in node.arguments:
            self.visit(arg)

    def visit_ArrayAccess(self, node):
                # Visit array access in expression
        symbol = self.current_scope.lookup(node.identifier)
        if not symbol:
            self.errors.add_error(
                SemanticError(
                    f"Array '{node.identifier}' is not declared",
                    1, 1,
                    f"Declare '{node.identifier}' as an ARRAY before use"
                )
            )
            return None
        if not symbol.is_array:
            self.errors.add_error(
                SemanticError(
                    f"'{node.identifier}' is not an array",
                    1, 1,
                    "Use array syntax only on ARRAY variables"
                )
            )
        for idx in node.indices:
            idx_type = self.visit(idx)
            if idx_type and idx_type != 'INTEGER':
                self.errors.add_error(
                    TypeError(
                        f"Array index must be INTEGER, got {idx_type}",
                        1, 1,
                        "Use an integer expression for the index"
                    )
                )
        return symbol.data_type

    def visit_RecordFieldAccess(self, node):
                # Visit record field access
        base_type = self.visit(node.record)
        if base_type and base_type in self.user_types:
            return self.user_types[base_type].get(node.field)
        return None
    
    def visit_Output(self, node):
                # Visit output statement
        for expr in node.expressions:
            # Visit for type checking
            self.visit(expr)
            # Try to evaluate constant output values
            val, _ = self.evaluate_const(expr)
            if val is not None:
                # Prefer expression line, then statement line
                line = getattr(expr, 'line', None) or getattr(node, 'line', None)
                self.observations.append({
                    'kind': 'output',
                    'line': line,
                    'value': val,
                    'message': f"Output value: {val}",
                })
    
    def visit_Input(self, node):
                # Visit input statement
        symbol = self.current_scope.lookup(node.variable)
        if not symbol:
            self.errors.add_error(
                SemanticError(
                    f"Variable '{node.variable}' is not declared",
                    1, 1,
                    f"Declare '{node.variable}' before INPUT"
                )
            )
        else:
            # Mark as initialized after input
            symbol.is_initialized = True
    
    def types_compatible(self, type1, type2):
                # Check if two types are compatible
        if type1 == type2:
            return True
        # INTEGER and REAL are compatible
        if set([type1, type2]) == {'INTEGER', 'REAL'}:
            return True
        return False
