from ast_nodes import Assignment, Variable, BinaryOp, Number, Print

class CodeGenerator:
    """Converts AST into C++ code."""
    
    def __init__(self, ast):
        self.ast = ast
        self.cpp_code = []

    def generate_code(self):
        """Generate C++ code from the AST."""
        self.cpp_code.append("#include <iostream>\nusing namespace std;\n\nint main() {\n")

        for node in self.ast:
            self.cpp_code.append(self.generate_statement(node))
        
        self.cpp_code.append("    return 0;\n}")
        return "\n".join(self.cpp_code)

    def generate_statement(self, node):
        """Generate C++ code for a statement."""
        if isinstance(node, Assignment):
            return f"    int {node.variable.name} = {self.generate_expression(node.expression)};\n"
        
        elif isinstance(node, Print):
            return f"    cout << {self.generate_expression(node.expression)} << endl;\n"

        else:
            raise RuntimeError(f"Unknown AST node: {node}")

    def generate_expression(self, node):
        """Generate C++ code for an expression."""
        if isinstance(node, Number):
            return str(node.value)
        
        elif isinstance(node, Variable):
            return node.name
        
        elif isinstance(node, BinaryOp):
            return f"({self.generate_expression(node.left)} {node.operator} {self.generate_expression(node.right)})"
        
        else:
            raise RuntimeError(f"Unknown expression node: {node}")
