from src.parser import *
from src.tokenizer import TokenType

class Transpiler:
    def __init__(self):
        self.indent_level = 0

    def transpile(self, node):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f"No visit_{type(node).__name__} method")

    def indent(self):
        return '    ' * self.indent_level

    def visit_Program(self, node):
        result = ""
        for stmt in node.statements:
            result += self.transpile(stmt) + "\n"
        return result

    def visit_Declaration(self, node):
        if node.is_array:
            bounds_str = ", ".join([f"{self.transpile(lower)}:{self.transpile(upper)}" 
                                   for lower, upper in node.array_bounds])
            return f"{self.indent()}# DECLARE {node.identifier} : ARRAY[{bounds_str}] OF {node.dtype}"
        return f"{self.indent()}# DECLARE {node.identifier} : {node.dtype}"
    
    def visit_ConstantDeclaration(self, node):
        return f"{self.indent()}{node.identifier} = {self.transpile(node.value)}  # CONSTANT"

    def visit_Assignment(self, node):
        if node.index:
            indices = "][".join([self.transpile(idx) for idx in node.index])
            return f"{self.indent()}{node.identifier}[{indices}] = {self.transpile(node.expression)}"
        return f"{self.indent()}{node.identifier} = {self.transpile(node.expression)}"
    
    def visit_ArrayAccess(self, node):
        indices = "][".join([self.transpile(idx) for idx in node.indices])
        return f"{node.identifier}[{indices}]"

    def visit_IfStatement(self, node):
        result = f"{self.indent()}if {self.transpile(node.condition)}:\n"
        self.indent_level += 1
        for stmt in node.then_branch:
            result += self.transpile(stmt) + "\n"
        self.indent_level -= 1
        
        if node.else_branch:
            result += f"{self.indent()}else:\n"
            self.indent_level += 1
            for stmt in node.else_branch:
                result += self.transpile(stmt) + "\n"
            self.indent_level -= 1
        return result.rstrip()
    
    def visit_CaseStatement(self, node):
        # Convert CASE to if-elif-else chain
        result = ""
        expr = self.transpile(node.expression)
        
        for i, (values, statements) in enumerate(node.cases):
            # Build condition for this case
            conditions = [f"{expr} == {self.transpile(val)}" for val in values]
            condition = " or ".join(conditions)
            
            if i == 0:
                result += f"{self.indent()}if {condition}:\n"
            else:
                result += f"{self.indent()}elif {condition}:\n"
            
            self.indent_level += 1
            for stmt in statements:
                result += self.transpile(stmt) + "\n"
            self.indent_level -= 1
        
        if node.otherwise:
            result += f"{self.indent()}else:\n"
            self.indent_level += 1
            for stmt in node.otherwise:
                result += self.transpile(stmt) + "\n"
            self.indent_level -= 1
        
        return result.rstrip()
    
    def visit_ProcedureDeclaration(self, node):
        params = ", ".join([name for name, _, _ in node.parameters])
        result = f"{self.indent()}def {node.name}({params}):\n"
        self.indent_level += 1
        if node.body:
            for stmt in node.body:
                result += self.transpile(stmt) + "\n"
        else:
            result += f"{self.indent()}pass\n"
        self.indent_level -= 1
        return result.rstrip()
    
    def visit_FunctionDeclaration(self, node):
        params = ", ".join([name for name, _, _ in node.parameters])
        result = f"{self.indent()}def {node.name}({params}):  # RETURNS {node.return_type}\n"
        self.indent_level += 1
        if node.body:
            for stmt in node.body:
                result += self.transpile(stmt) + "\n"
        else:
            result += f"{self.indent()}pass\n"
        self.indent_level -= 1
        return result.rstrip()
    
    def visit_ProcedureCall(self, node):
        args = ", ".join([self.transpile(arg) for arg in node.arguments])
        return f"{self.indent()}{node.name}({args})"
    
    def visit_FunctionCall(self, node):
        args = ", ".join([self.transpile(arg) for arg in node.arguments])
        return f"{node.name}({args})"
    
    def visit_ReturnStatement(self, node):
        return f"{self.indent()}return {self.transpile(node.expression)}"

    def visit_ForLoop(self, node):
  
        
        var = node.variable
        start = self.transpile(node.start_value)
        end = self.transpile(node.end_value)
        
        if node.step_value:
            step = self.transpile(node.step_value)
    
            result = f"{self.indent()}for {var} in range({start}, {end} + 1, {step}):\n"
        else:
            result = f"{self.indent()}for {var} in range({start}, {end} + 1):\n"
        
        self.indent_level += 1
        for stmt in node.body:
            result += self.transpile(stmt) + "\n"
        self.indent_level -= 1
        return result.rstrip()

    def visit_WhileLoop(self, node):
        result = f"{self.indent()}while {self.transpile(node.condition)}:\n"
        self.indent_level += 1
        for stmt in node.body:
            result += self.transpile(stmt) + "\n"
        self.indent_level -= 1
        return result.rstrip()

    def visit_RepeatLoop(self, node):

        result = f"{self.indent()}while True:\n"
        self.indent_level += 1
        for stmt in node.body:
            result += self.transpile(stmt) + "\n"
        
        # Break condition
        result += f"{self.indent()}if {self.transpile(node.condition)}:\n"
        self.indent_level += 1
        result += f"{self.indent()}break\n"
        self.indent_level -= 1
        
        self.indent_level -= 1
        return result.rstrip()

    def visit_Output(self, node):
        args = ", ".join([self.transpile(expr) for expr in node.expressions])
        return f"{self.indent()}print({args})"

    def visit_Input(self, node):
        return f"{self.indent()}{node.variable} = input()"

    def visit_BinaryOp(self, node):
        left = self.transpile(node.left)
        right = self.transpile(node.right)
        op_map = {
            TokenType.PLUS: '+',
            TokenType.MINUS: '-',
            TokenType.MULTIPLY: '*',
            TokenType.DIVIDE: '/',
            TokenType.DIV_INT: '//',
            TokenType.MOD: '%',
            TokenType.EQ: '==',
            TokenType.NEQ: '!=',
            TokenType.LT: '<',
            TokenType.GT: '>',
            TokenType.LTE: '<=',
            TokenType.GTE: '>=',
            TokenType.AND: 'and',
            TokenType.OR: 'or'
        }
        op = op_map.get(node.operator.type)
        if not op:
            raise Exception(f"Unknown operator {node.operator.type}")
        return f"({left} {op} {right})"

    def visit_UnaryOp(self, node):
        operand = self.transpile(node.operand)
        if node.operator.type == TokenType.NOT:
            return f"(not {operand})"
        elif node.operator.type == TokenType.MINUS:
            return f"(-{operand})"
        else:
            raise Exception(f"Unknown unary operator {node.operator.type}")

    def visit_Literal(self, node):
        if node.literal_type == 'STRING' or isinstance(node.value, str):
            return f'"{node.value}"'
        elif node.literal_type == 'CHAR':
            return f"'{node.value}'"
        elif node.literal_type == 'BOOLEAN':
            return str(node.value)
        return str(node.value)

    def visit_Identifier(self, node):
        return node.name

    def visit_BuiltInFunctionCall(self, node):
        args = ", ".join([self.transpile(arg) for arg in node.arguments])
        name = node.name.upper()
        return f"{name}({args})"

    def visit_RecordFieldAccess(self, node):
        record = self.transpile(node.record)
        return f"{record}.{node.field}"

    def visit_TypeDeclaration(self, node):
        return f"{self.indent()}# TYPE {node.name} ... ENDTYPE"
