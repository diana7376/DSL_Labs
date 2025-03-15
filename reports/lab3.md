# Lab3: Lexer & Scanner Report

### Course: Formal Languages & Finite Automata  
### Author: Diana Iachim 

---

## Overview
The term **lexer** comes from *lexical analysis*, which represents the process of extracting lexical tokens from a string of characters. A lexer is also referred to as a **tokenizer** or **scanner**. This lexical analysis is a crucial first step in a compiler or interpreter for various programming, markup, or structured languages.

Tokens are identified based on predefined rules of a language, and the output of the lexer is known as *lexemes*. Lexemes represent sequences of characters that match a particular pattern. These lexemes are then assigned meaningful categories as *tokens*. Tokens categorize lexemes rather than storing their exact value.

---

## Objectives
1. Understand what lexical analysis is.
2. Get familiar with the inner workings of a lexer/scanner/tokenizer.
3. Implement a sample lexer and demonstrate how it works.

---

## Implementation Description
This implementation focuses on an SQL lexer that recognizes and tokenizes SQL statements. The lexer can identify various SQL components, including keywords, identifiers, operators, numbers, strings, delimiters, whitespace, and comments. 

### Lexer Implementation
The lexer consists of several core components:

#### 1. Defining Token Types
This section defines an enumeration of possible token types.
```python
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
```

#### 2. Defining SQL Keywords
A predefined set of SQL keywords is stored for token classification.
```python
SQL_KEYWORDS = {"SELECT", "FROM", "WHERE", "INSERT", "UPDATE", "DELETE", "AND", "OR", "LIKE"}
```

#### 3. Defining Token Patterns
A list of regex patterns is created to match different token types.
```python
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
```

#### 4. Implementing the Lexer Function
This function iterates through the input string, matches tokens, and classifies them.
```python
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
                if token_type != TokenType.WHITESPACE:
                    tokens.append((token_type, value))
                query = query[len(value):]
                break
        if not match:
            tokens.append((TokenType.UNKNOWN, query[0]))
            query = query[1:]
    return tokens
```

---

## Results
Below is an example of how the lexer processes an SQL query:

### Input Query:
```sql
SELECT name, age FROM users WHERE age > 21;
```

### Lexer Output:
```python
[(TokenType.KEYWORD, 'SELECT'),
 (TokenType.IDENTIFIER, 'name'),
 (TokenType.DELIMITER, ','),
 (TokenType.IDENTIFIER, 'age'),
 (TokenType.KEYWORD, 'FROM'),
 (TokenType.IDENTIFIER, 'users'),
 (TokenType.KEYWORD, 'WHERE'),
 (TokenType.IDENTIFIER, 'age'),
 (TokenType.OPERATOR, '>'),
 (TokenType.NUMBER, '21'),
 (TokenType.DELIMITER, ';')]
```

---

## Conclusion
This project successfully implemented an SQL lexer capable of identifying and categorizing tokens in an SQL query. The lexer uses **regular expressions** to recognize different token types and assigns them appropriate categories. It provides a fundamental understanding of how **lexical analysis** works and how lexers can be designed to tokenize structured languages.


---

## References
1. [A sample of a lexer implementation](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl01.html)  
2. [Lexical analysis](https://en.wikipedia.org/wiki/Lexical_analysis)

