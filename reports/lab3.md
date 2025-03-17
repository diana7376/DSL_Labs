# Lab3: Lexer & Scanner Report

### Course: Formal Languages & Finite Automata  
### Author: Diana Iachim 

---

## Overview
The term **lexer** comes from *lexical analysis*, which represents the process of extracting lexical tokens from a string of characters. A lexer is also referred to as a **tokenizer** or **scanner**. This lexical analysis is a crucial first step in a compiler or interpreter for various programming, markup, or structured languages.

Tokens are identified based on predefined rules of a language, and the output of the lexer is known as *lexemes*. Lexemes represent sequences of characters that match a particular pattern. These lexemes are then assigned meaningful categories as *tokens*. Tokens categorize lexemes rather than storing their exact value.

I choose _SQL_ for this lexer implementation because it is one of the most widely used languages for managing and querying databases. SQL queries have a structured and well-defined syntax, making them ideal for tokenization. A lexer for SQL queries is essential for building SQL parsers, query optimizers, and database engines, as it allows structured decomposition of input queries into meaningful components. Additionally, SQL queries contain a variety of elements, such as `keywords`, `identifiers`, `operators`, `numbers`, and `strings`, which provide a rich environment for demonstrating lexical analysis.

---

## Objectives
1. Understand what lexical analysis is.
2. Get familiar with the inner workings of a lexer/scanner/tokenizer.
3. Implement a sample lexer and demonstrate how it works.

---

## Implementation Description
This implementation focuses on an SQL lexer that recognizes and tokenizes SQL statements. The lexer can identify various SQL components, including keywords, identifiers, operators, numbers, strings, delimiters, whitespace, and comments. 

To implement this lexer, **regular expressions** (regex) were used because they provide an efficient and precise way to define patterns for various SQL tokens. Regex allows quick pattern matching and classification of `keywords`, `identifiers`, `numbers`, `operators`, and other SQL components, significantly simplifying the lexing process. Instead of manually writing complex string-parsing logic, regex allows for concise, readable, and high-performance tokenization, making it the most convenient method for implementing a lexer. It ensures accuracy, flexibility, and ease of maintenance when extending the lexer to support additional SQL features.

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
The lexer function takes an input string (SQL query) and processes it token by token. It starts by initializing an empty list to store the extracted tokens. 
The function then iterates through the input query character by character, attempting to match substrings against predefined regular expressions representing different token types. When a match is found, the function assigns the corresponding token type based on the pattern and appends it to the list of tokens. 
Whitespace tokens are ignored to avoid unnecessary processing. After identifying a token, the function moves forward in the input string by removing the matched portion. If an unknown character is encountered, it is assigned an `UNKNOWN` token type. 
Finally, the function returns the structured list of tokens, which represents the parsed SQL query ready for further processing, such as syntax analysis or query execution.

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

