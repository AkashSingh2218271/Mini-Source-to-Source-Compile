from lexer import Lexer
from parser import Parser
from codegen import CodeGenerator
from ast_nodes import Program
import sys

def transpile_python_to_cpp(input_file, output_file):
    try:
        # Read Python code
        with open(input_file, "r") as f:
            code = f.read()

        # Tokenize
        print("Tokenizing Python code...")
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        print("Tokenization successful!")

        # Parse
        print("\nParsing tokens into AST...")
        parser = Parser(tokens)
        statements = parser.parse()
        ast = Program(statements)  # Wrap statements in a Program node
        print("Parsing successful!")

        # Generate C++ code
        print("\nGenerating C++ code...")
        codegen = CodeGenerator()
        cpp_code = codegen.generate(ast)  # Use generate instead of generate_code
        print("Code generation successful!")

        # Save the C++ code
        with open(output_file, "w") as f:
            f.write(cpp_code)
        print(f"\nC++ code has been written to {output_file}")

        # Print the generated C++ code
        print("\nGenerated C++ Code:\n")
        print(cpp_code)

    except FileNotFoundError:
        print(f"Error: Could not find input file '{input_file}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error during transpilation: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    input_file = "my.py"
    output_file = "output.cpp"
    transpile_python_to_cpp(input_file, output_file)