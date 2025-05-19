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
        code.append("#include <bits/stdc++.h>")
        code.append("using namespace std;")
        code.append("")
        
        # First, collect all function definitions
        function_defs = []
        other_statements = []
        for statement in program.statements:
            if isinstance(statement, FunctionDef):
                function_defs.append(statement)
            else:
                other_statements.append(statement)
        
        # Generate all function declarations first
        for func_def in function_defs:
            params = []
            for param in func_def.params:
                if param == "arr":
                    params.append("vector<int>& arr")
                else:
                    params.append("int " + param)
            # Use void return type for functions that don't return anything
            return_type = "void" if func_def.name == "quick_sort" else "int"
            code.append(f"{return_type} {func_def.name}({', '.join(params)});")
        
        code.append("")
        
        # Generate all function definitions
        for func_def in function_defs:
            params = []
            for param in func_def.params:
                if param == "arr":
                    params.append("vector<int>& arr")
                else:
                    params.append("int " + param)
            # Use void return type for functions that don't return anything
            return_type = "void" if func_def.name == "quick_sort" else "int"
            code.append(f"{return_type} {func_def.name}({', '.join(params)}) {{")
            self.indent_level += 1
            
            # Generate function body
            for stmt in func_def.body:
                if isinstance(stmt, FunctionDef):
                    # Skip nested function definitions
                    continue
                code.extend(self.generate_statement(stmt))
            
            self.indent_level -= 1
            code.append("}")
            code.append("")
        
        # Generate main function
        code.append("int main() {")
        self.indent_level += 1
        
        # Generate all non-function statements in main
        for statement in other_statements:
            if isinstance(statement, FunctionDef):
                # Skip function definitions in main
                continue
            code.extend(self.generate_statement(statement))
        
        self.indent_level -= 1
        code.append("    return 0;")
        code.append("}")
        
        return "\n".join(code)
    
    def generate_statement(self, statement):
        """Generate code for a statement."""
        if isinstance(statement, list):
            code = []
            for stmt in statement:
                if isinstance(stmt, FunctionDef):
                    # Skip nested function definitions
                    continue
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
        elif isinstance(statement, Return):
            return self.generate_return(statement)
        elif isinstance(statement, ListAssignment):
            return self.generate_list_assignment(statement)
        elif isinstance(statement, FunctionCall):
            code = []
            indent = "    " * self.indent_level
            code.append(f"{indent}{self.generate_expression(statement)};")
            return code
        elif isinstance(statement, FunctionDef):
            # Skip function definitions in statement generation
            # They are handled in generate_program
            return []
        else:
            raise Exception(f"Unknown statement type: {type(statement)}")
    
    def generate_print(self, print_stmt):
        """Generate code for a print statement."""
        code = []
        indent = "    " * self.indent_level
        
        if len(print_stmt.expressions) == 1:
            expr = print_stmt.expressions[0]
            if isinstance(expr, List):
                # Special handling for printing arrays
                code.append(f"{indent}cout << \"Array: \";")
                code.append(f"{indent}for (int x : {self.generate_expression(expr)}) {{")
                code.append(f"{indent}    cout << x << \" \";")
                code.append(f"{indent}}}")
                code.append(f"{indent}cout << endl;")
            else:
                code.append(f"{indent}cout << {self.generate_expression(expr)} << endl;")
        else:
            parts = []
            for expr in print_stmt.expressions:
                if isinstance(expr, str):
                    parts.append(f"\"{expr}\"")
                else:
                    parts.append(self.generate_expression(expr))
            code.append(f"{indent}cout << {' << '.join(parts)} << endl;")
        
        return code
    
    def generate_assignment(self, assignment):
        """Generate code for a variable assignment."""
        code = []
        indent = "    " * self.indent_level
        var_name = assignment.name.name if isinstance(assignment.name, Variable) else assignment.name
        
        if var_name not in self.variables:
            value = self.generate_expression(assignment.value)
            if isinstance(assignment.value, List):
                code.append(f"{indent}vector<int> {var_name} = {value};")
            elif isinstance(assignment.value, String):
                code.append(f"{indent}string {var_name} = {value};")
            elif isinstance(assignment.value, Float):
                code.append(f"{indent}double {var_name} = {value};")
            elif isinstance(assignment.value, Number):
                code.append(f"{indent}int {var_name} = {value};")
            else:
                code.append(f"{indent}auto {var_name} = {value};")
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
            start = self.generate_expression(for_stmt.iterable.start)
            end_expr = for_stmt.iterable.end
            # SAFETY PATCH: If end is a List, extract the last element
            if isinstance(end_expr, List) and len(end_expr.elements) == 2:
                end = self.generate_expression(end_expr.elements[1])
            else:
                end = self.generate_expression(end_expr)
            
            if hasattr(for_stmt.iterable, 'step') and for_stmt.iterable.step is not None:
                step = self.generate_expression(for_stmt.iterable.step)
                code.append(f"{indent}for (int {for_stmt.var_name} = {start}; {for_stmt.var_name} < {end}; {for_stmt.var_name} += {step}) {{")
            else:
                code.append(f"{indent}for (int {for_stmt.var_name} = {start}; {for_stmt.var_name} < {end}; {for_stmt.var_name}++) {{")
            
            self.indent_level += 1
            for statement in for_stmt.body:
                code.extend(self.generate_statement(statement))
            self.indent_level -= 1
            code.append(f"{indent}}}")
        elif isinstance(for_stmt.iterable, List):
            # Handle iterating over a list
            iterable = self.generate_expression(for_stmt.iterable)
            code.append(f"{indent}for (int {for_stmt.var_name} : {iterable}) {{")
            self.indent_level += 1
            for statement in for_stmt.body:
                code.extend(self.generate_statement(statement))
            self.indent_level -= 1
            code.append(f"{indent}}}")
        else:
            # Handle other types of for loops
            iterable = self.generate_expression(for_stmt.iterable)
            code.append(f"{indent}for (auto {for_stmt.var_name} : {iterable}) {{")
            self.indent_level += 1
            for statement in for_stmt.body:
                code.extend(self.generate_statement(statement))
            self.indent_level -= 1
            code.append(f"{indent}}}")
        
        return code
    
    def generate_return(self, return_stmt):
        """Generate code for a return statement."""
        code = []
        indent = "    " * self.indent_level
        
        if return_stmt.value is not None:
            code.append(f"{indent}return {self.generate_expression(return_stmt.value)};")
        else:
            code.append(f"{indent}return;")
        
        return code
    
    def generate_list_assignment(self, list_assign):
        """Generate code for list assignment."""
        code = []
        indent = "    " * self.indent_level
        
        if isinstance(list_assign.value, ListAccess):
            # Handle swap operation
            code.append(f"{indent}swap({self.generate_expression(list_assign.list_expr)}[{self.generate_expression(list_assign.index)}], {self.generate_expression(list_assign.value.list_expr)}[{self.generate_expression(list_assign.value.index)}]);")
        else:
            # Regular assignment
            code.append(f"{indent}{self.generate_expression(list_assign.list_expr)}[{self.generate_expression(list_assign.index)}] = {self.generate_expression(list_assign.value)};")
        
        return code
    
    def generate_expression(self, expr):
        """Generate code for an expression."""
        if isinstance(expr, Number):
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
            return f"({left} {expr.op} {right})"
        elif isinstance(expr, UnaryOp):
            return f"{expr.op}{self.generate_expression(expr.operand)}"
        elif isinstance(expr, List):
            elements = [self.generate_expression(e) for e in expr.elements]
            return f"{{{', '.join(elements)}}}"
        elif isinstance(expr, ListAccess):
            return f"{self.generate_expression(expr.list_expr)}[{self.generate_expression(expr.index)}]"
        elif isinstance(expr, FunctionCall):
            if expr.name == "len":
                return f"{self.generate_expression(expr.args[0])}.size()"
            args = [self.generate_expression(arg) for arg in expr.args]
            return f"{expr.name}({', '.join(args)})"
        elif isinstance(expr, RangeCall):
            # Handle range() function call
            if expr.end is None:
                return f"range({self.generate_expression(expr.start)})"
            elif expr.step is None:
                return f"range({self.generate_expression(expr.start)}, {self.generate_expression(expr.end)})"
            else:
                return f"range({self.generate_expression(expr.start)}, {self.generate_expression(expr.end)}, {self.generate_expression(expr.step)})"
        else:
            raise Exception(f"Unknown expression type: {type(expr)}")