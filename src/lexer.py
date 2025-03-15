import re
from enum import Enum


class TokenType(Enum):
    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"
    OPERATOR = "OPERATOR"
    NUMBER = "NUMBER"
    STRING = "STRING"
    DELIMITER = "DELIMITER"
    WHITESPACE = "WHITESPACE"
    COMMENT = "COMMENT"
    UNKNOWN = "UNKNOWN"

# SQL keywords
SQL_KEYWORDS = {"SELECT", "FROM", "WHERE", "INSERT", "UPDATE", "DELETE", "AND", "OR", "LIKE"}

# token regex patterns
TOKEN_PATTERNS = [
    (TokenType.KEYWORD, r'\b(?:SELECT|FROM|WHERE|INSERT|UPDATE|DELETE|AND|OR|LIKE)\b', SQL_KEYWORDS),
    (TokenType.IDENTIFIER, r'[a-zA-Z_][a-zA-Z0-9_]*', None),
    (TokenType.OPERATOR, r'<=|>=|<>|!=|=|<|>|\+|\-|\*|/', None),
    (TokenType.NUMBER, r'\b\d+(?:\.\d+)?\b', None),
    (TokenType.STRING, r'\'([^\']*)\'|\"([^\"]*)\"', None),
    (TokenType.DELIMITER, r'[(),;]', None),
    (TokenType.WHITESPACE, r'\s+', None),
    (TokenType.COMMENT, r'--.*', None)
]

def sql_lexer(query):
    tokens = []
    while query:
        match = None
        for token_type, pattern, keyword_set in TOKEN_PATTERNS:
            regex = re.compile(pattern, re.IGNORECASE)
            match = regex.match(query)
            if match:
                value = match.group(0)
                if token_type == TokenType.KEYWORD and value.upper() not in SQL_KEYWORDS:
                    token_type = TokenType.IDENTIFIER
                if token_type != TokenType.WHITESPACE:  # ignore whitespace tokens
                    tokens.append((token_type, value))
                query = query[len(value):]  # remove token from query
                break
        if not match:
            tokens.append((TokenType.UNKNOWN, query[0]))
            query = query[1:]  # skip unknown character
    return tokens

# Test the SQL lexer
# query = "SELECT name, age FROM users WHERE age > 21;"
# tokens = sql_lexer(query)
# for token in tokens:
#     print(token)
