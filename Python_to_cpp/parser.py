from lexer import Lexer, TokenType
from ast_nodes import Assignment, Variable, BinaryOp, Number, Print

class Parser:
    """Parses tokens into an Abstract Syntax Tree (AST)."""
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index]

    def eat(self, token_type):
        """Consume a token if it matches the expected type."""
        if self.current_token.type == token_type:
            self.current_token_index += 1
            if self.current_token_index < len(self.tokens):
                self.current_token = self.tokens[self.current_token_index]
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token}")

    def parse_number(self):
        """Parse a number and return a Number AST node."""
        token = self.current_token
        self.eat(TokenType.NUMBER)
        return Number(token.value)

    def parse_variable(self):
        """Parse a variable and return a Variable AST node."""
        token = self.current_token
        self.eat(TokenType.IDENTIFIER)
        return Variable(token.value)

    def parse_factor(self):
        """Parse a single value: either a number or a variable."""
        if self.current_token.type == TokenType.NUMBER:
            return self.parse_number()
        elif self.current_token.type == TokenType.IDENTIFIER:
            return self.parse_variable()
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token}")

    def parse_expression(self):
        """Parse an expression with +, -, *, /."""
        left = self.parse_factor()

        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, TokenType.DIVIDE):
            operator = self.current_token.value
            self.eat(self.current_token.type)
            right = self.parse_factor()
            left = BinaryOp(left, operator, right)  # Construct a BinaryOp node

        return left

    def parse_statement(self):
        """Parse a single statement (assignment or print)."""
        if self.current_token.type == TokenType.IDENTIFIER:
            var_name = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
            self.eat(TokenType.EQUALS)  # Consume '='
            expression = self.parse_expression()
            return Assignment(Variable(var_name), expression)
        
        elif self.current_token.type == TokenType.PRINT:
            self.eat(TokenType.PRINT)
            self.eat(TokenType.LPAREN)
            expression = self.parse_expression()
            self.eat(TokenType.RPAREN)
            return Print(expression)

        else:
            raise SyntaxError(f"Invalid statement: {self.current_token}")

    def parse(self):
        """Parse multiple statements into an AST list."""
        ast = []
        while self.current_token.type != TokenType.EOF:
            ast.append(self.parse_statement())
        return ast
