from ast_nodes import (
    Program, Print, BinaryOp, Number, String, Boolean, Variable,
    Assignment, IfStatement, WhileLoop, ForLoop, RangeCall,
    FunctionDef, FunctionCall, Return, List, ListAccess,
    ListAssignment, LenCall, UnaryOp, Float
)

class CodeGenerator:
    """Generates C++ code from an AST."""
    
    def __init__(self):
        self.indent_level = 0
        self.variables = set()
        self.functions = set()
    
    def generate(self, ast):
        """Main function to generate C++ code."""
        return self.generate_program(ast)
    
    def generate_program(self, program):
        """Generate code for the entire program."""
        code = []
        code.append("#include <iostream>")
        code.append("#include <vector>")
        code.append("#include <string>")
        code.append("#include <cmath>")
        code.append("")
        code.append("using namespace std;")
        code.append("")
        
        for statement in program.statements:
            code.extend(self.generate_statement(statement))
        
        return "\n".join(code)
    
    def generate_statement(self, statement):
        """Generate code for a statement."""
        if isinstance(statement, list):
            # Handle lists of statements (e.g., from tuple unpacking)
            code = []
            for stmt in statement:
                code.extend(self.generate_statement(stmt))
            return code
        elif isinstance(statement, Print):
            return self.generate_print(statement)
        elif isinstance(statement, Assignment):
            return self.generate_assignment(statement)
        elif isinstance(statement, IfStatement):
            return self.generate_if(statement)
        elif isinstance(statement, WhileLoop):
            return self.generate_while(statement)
        elif isinstance(statement, ForLoop):
            return self.generate_for(statement)
        elif isinstance(statement, FunctionDef):
            return self.generate_function_def(statement)
        elif isinstance(statement, Return):
            return self.generate_return(statement)
        elif isinstance(statement, ListAssignment):
            return self.generate_list_assignment(statement)
        elif isinstance(statement, FunctionCall):
            # Handle function calls as statements
            code = []
            indent = "    " * self.indent_level
            code.append(f"{indent}{self.generate_expression(statement)};")
            return code
        else:
            raise Exception(f"Unknown statement type: {type(statement)}")
    
    def generate_print(self, print_stmt):
        """Generate code for a print statement."""
        code = []
        indent = "    " * self.indent_level
        
        if len(print_stmt.expressions) == 1:
            code.append(f"{indent}cout << {self.generate_expression(print_stmt.expressions[0])} << endl;")
        else:
            parts = []
            for expr in print_stmt.expressions:
                parts.append(f"cout << {self.generate_expression(expr)}")
            code.append(f"{indent}{' << '.join(parts)} << endl;")
        
        return code
    
    def generate_assignment(self, assignment):
        """Generate code for a variable assignment."""
        code = []
        indent = "    " * self.indent_level
        var_name = assignment.name
        
        if var_name not in self.variables:
            code.append(f"{indent}auto {var_name} = {self.generate_expression(assignment.value)};")
            self.variables.add(var_name)
        else:
            code.append(f"{indent}{var_name} = {self.generate_expression(assignment.value)};")
        
        return code
    
    def generate_if(self, if_stmt):
        """Generate code for an if statement."""
        code = []
        indent = "    " * self.indent_level
        
        code.append(f"{indent}if ({self.generate_expression(if_stmt.condition)}) {{")
        self.indent_level += 1
        
        for statement in if_stmt.body:
            code.extend(self.generate_statement(statement))
        
        self.indent_level -= 1
        code.append(f"{indent}}}")
        
        if if_stmt.else_body:
            code.append(f"{indent}else {{")
            self.indent_level += 1
            
            for statement in if_stmt.else_body:
                code.extend(self.generate_statement(statement))
            
            self.indent_level -= 1
            code.append(f"{indent}}}")
        
        return code
    
    def generate_while(self, while_stmt):
        """Generate code for a while loop."""
        code = []
        indent = "    " * self.indent_level
        
        code.append(f"{indent}while ({self.generate_expression(while_stmt.condition)}) {{")
        self.indent_level += 1
        
        for statement in while_stmt.body:
            code.extend(self.generate_statement(statement))
        
        self.indent_level -= 1
        code.append(f"{indent}}}")
        
        return code
    
    def generate_for(self, for_stmt):
        """Generate code for a for loop."""
        code = []
        indent = "    " * self.indent_level
        
        if isinstance(for_stmt.iterable, RangeCall):
            # Handle range() function
            start = self.generate_expression(for_stmt.iterable.start)
            end = self.generate_expression(for_stmt.iterable.end)
            
            # Handle step parameter
            if hasattr(for_stmt.iterable, 'step') and for_stmt.iterable.step is not None:
                step = self.generate_expression(for_stmt.iterable.step)
                code.append(f"{indent}for (int {for_stmt.var_name} = {start}; {for_stmt.var_name} < {end}; {for_stmt.var_name} += {step}) {{")
            else:
                code.append(f"{indent}for (int {for_stmt.var_name} = {start}; {for_stmt.var_name} < {end}; {for_stmt.var_name}++) {{")
        else:
            # Handle other iterables (lists, etc.)
            iterable = self.generate_expression(for_stmt.iterable)
            code.append(f"{indent}for (const auto& {for_stmt.var_name} : {iterable}) {{")
        
        self.indent_level += 1
        
        for statement in for_stmt.body:
            code.extend(self.generate_statement(statement))
        
        self.indent_level -= 1
        code.append(f"{indent}}}")
        
        return code
    
    def generate_function_def(self, func_def):
        """Generate code for a function definition."""
        code = []
        indent = "    " * self.indent_level
        
        # Generate function signature
        params = []
        for param in func_def.params:
            params.append(f"auto {param}")
        
        code.append(f"{indent}auto {func_def.name}({', '.join(params)}) {{")
        self.indent_level += 1
        
        # Generate function body
        for statement in func_def.body:
            code.extend(self.generate_statement(statement))
        
        self.indent_level -= 1
        code.append(f"{indent}}}")
        code.append("")
        
        self.functions.add(func_def.name)
        return code
    
    def generate_return(self, return_stmt):
        """Generate code for a return statement."""
        code = []
        indent = "    " * self.indent_level
        
        if return_stmt.value is None:
            code.append(f"{indent}return;")
        else:
            code.append(f"{indent}return {self.generate_expression(return_stmt.value)};")
        
        return code
    
    def generate_list_assignment(self, list_assign):
        """Generate code for a list assignment."""
        code = []
        indent = "    " * self.indent_level
        
        list_expr = self.generate_expression(list_assign.list_expr)
        index = self.generate_expression(list_assign.index)
        value = self.generate_expression(list_assign.value)
        
        code.append(f"{indent}{list_expr}[{index}] = {value};")
        return code
    
    def generate_expression(self, expr):
        """Generate code for an expression."""
        if isinstance(expr, Number):
            return str(expr.value)
        elif isinstance(expr, Float):
            return str(expr.value)
        elif isinstance(expr, String):
            return f'"{expr.value}"'
        elif isinstance(expr, Boolean):
            return "true" if expr.value else "false"
        elif isinstance(expr, Variable):
            return expr.name
        elif isinstance(expr, BinaryOp):
            left = self.generate_expression(expr.left)
            right = self.generate_expression(expr.right)
            
            # Handle string concatenation
            if expr.op == '+':
                # If either operand is a string or str() call, use string concatenation
                if isinstance(expr.left, String) or isinstance(expr.right, String) or \
                   (isinstance(expr.left, FunctionCall) and expr.left.name == 'str') or \
                   (isinstance(expr.right, FunctionCall) and expr.right.name == 'str'):
                    return f"std::string({left}) + std::string({right})"
            
            # Map Python operators to C++ operators
            operator_map = {
                '+': '+',
                '-': '-',
                '*': '*',
                '/': '/',
                '%': '%',
                '==': '==',
                '!=': '!=',
                '<': '<',
                '>': '>',
                '<=': '<=',
                '>=': '>=',
                'and': '&&',
                'or': '||'
            }
            op = operator_map.get(expr.op, expr.op)
            return f"({left} {op} {right})"
        elif isinstance(expr, UnaryOp):
            operand = self.generate_expression(expr.operand)
            return f"({expr.operator}{operand})"
        elif isinstance(expr, FunctionCall):
            args = [self.generate_expression(arg) for arg in expr.args]
            if expr.name == "str":
                return f"std::to_string({args[0]})"
            return f"{expr.name}({', '.join(args)})"
        elif isinstance(expr, List):
            elements = [self.generate_expression(elem) for elem in expr.elements]
            return f"std::vector<auto>{{{', '.join(elements)}}}"
        elif isinstance(expr, ListAccess):
            list_expr = self.generate_expression(expr.list_expr)
            index = self.generate_expression(expr.index)
            return f"{list_expr}[{index}]"
        elif isinstance(expr, LenCall):
            arg = self.generate_expression(expr.arg)
            return f"{arg}.size()"
        else:
            raise Exception(f"Unknown expression type: {type(expr)}")
