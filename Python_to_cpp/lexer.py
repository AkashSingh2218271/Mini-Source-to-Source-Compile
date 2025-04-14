import re
from tokens import TokenType

class Token:
    """Represents a single token."""
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

class Lexer:
    """Converts Python code into tokens."""
    
    def __init__(self, source_code):
        self.source_code = source_code
        self.position = 0
        self.tokens = []
    
    def tokenize(self):
        """Main function to generate tokens from source code."""
        token_specification = [
            (TokenType.PRINT, r'\bprint\b'),
            (TokenType.IF, r'\bif\b'),
            (TokenType.ELSE, r'\belse\b'),
            (TokenType.IDENTIFIER, r'[a-zA-Z_][a-zA-Z0-9_]*'),
            (TokenType.NUMBER, r'\d+'),
            (TokenType.EQUALS, r'='),
            (TokenType.PLUS, r'\+'),
            (TokenType.MINUS, r'-'),
            (TokenType.MULTIPLY, r'\*'),
            (TokenType.DIVIDE, r'/'),
            (TokenType.GREATER, r'>'),
            (TokenType.LESS, r'<'),
            (TokenType.LPAREN, r'\('),
            (TokenType.RPAREN, r'\)'),
        ]

        token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)
        
        for match in re.finditer(token_regex, self.source_code):
            token_type = match.lastgroup
            token_value = match.group(token_type)

            if token_type == TokenType.NUMBER:
                token_value = int(token_value)  # Convert number tokens to int
            
            self.tokens.append(Token(token_type, token_value))

        self.tokens.append(Token(TokenType.EOF, None))  # Append End-of-File token
        return self.tokens
