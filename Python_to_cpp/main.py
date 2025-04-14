from lexer import Lexer
from parser import Parser
from codegen import CodeGenerator

code = """
a = 5 + 3
print(a)
"""

# Tokenize the input
lexer = Lexer(code)
tokens = lexer.tokenize()

# Parse the tokens into an AST
parser = Parser(tokens)
ast_tree = parser.parse()

# Generate C++ code
codegen = CodeGenerator(ast_tree)
cpp_code = codegen.generate_code()

# Save to file
with open("output.cpp", "w") as f:
    f.write(cpp_code)

# Print the generated C++ code
print("Generated C++ Code:\n")
print(cpp_code)