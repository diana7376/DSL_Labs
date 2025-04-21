# Lab6: Parser & Abstract Syntax Tree Builder

### Course: Formal Languages & Finite Automata  
Author: Iachim Diana

---

## Overview

This lab focuses on implementing a parser and constructing an Abstract Syntax Tree (AST) for a simplified subset of SQL queries. The parser processes input queries, validates their syntax, and builds a hierarchical AST that represents the structure of the parsed SQL. The main constructs supported include `SELECT`, `FROM`, and optional `WHERE` clauses.

The goal is to bridge the gap between lexical analysis and structural representation of code through ASTs, a concept widely applied in compilers, interpreters, and code analyzers.

---

## Objectives

1. Understand the purpose and implementation of a parser.
2. Create a type system to categorize tokens during lexical analysis using `TokenType`.
3. Implement an Abstract Syntax Tree (AST) structure.
4. Develop a parser that transforms SQL-like input into AST nodes.
5. Use regular expressions to tokenize input text.

---

## Grammar Handled

The parser supports a minimal grammar of the form:
```
SELECT <column_list> FROM <table> [WHERE <condition>]
```
Where:
- `<column_list>` is one or more identifiers separated by commas
- `<table>` is a single identifier
- `<condition>` is a binary operation such as `age >= 18` or `name = 'John'`

---

## Implementation Description

### 1. **Token Types (Lexer)**
To break down the raw SQL input into meaningful elements, a lexical analyzer (lexer) uses regular expressions to identify different kinds of tokens such as keywords (`SELECT`, `FROM`), identifiers (column and table names), operators (`=`, `>=`), and literals (numbers or strings).

**Example logic:**
```python
(TokenType.KEYWORD, r'\b(?:SELECT|FROM|WHERE)\b', SQL_KEYWORDS)
```
This ensures that SQL keywords are recognized properly and differentiated from identifiers, aiding the parser in interpreting the structure correctly.

### 2. **AST Structure**
The Abstract Syntax Tree (AST) is a tree-based representation of the SQL query's structure. Each node represents a syntactic construct. For example, a `SELECT_STATEMENT` node will have children nodes representing selected columns, source tables, and conditions.

**Simplified structure:**
```python
ASTNode(ASTNodeType.SELECT_STATEMENT, children=[...])
```
The use of recursive node nesting makes it easy to visualize and traverse the logical hierarchy of the query.

### 3. **Parser Logic**
The parser performs a top-down analysis of the token list. It verifies that the input follows the expected SQL structure and constructs corresponding AST nodes.

**Core logic:**
```python
if current_token == SELECT:
    parse_column_list()
    expect FROM
    parse_table()
    if WHERE: parse_condition()
```
This flow allows the parser to build a tree-like representation of the query with clear separation between components like columns, tables, and filtering conditions.

### 4. **Main Driver**
The main script runs an input loop where users can write SQL queries. The program then:
- Tokenizes the input
- Parses it into an AST
- Prints both the tokens and the hierarchical AST structure

**Snippet:**
```python
query = input("SQL> ")
tokens = sql_lexer(query)
ast = sql_parser(query)
print(ast)
```
This offers an interactive experience to test and debug queries in real-time.

---

## Example

### Input:
```sql
SELECT id, name FROM users WHERE age >= 18
```

### Token Output:
```
KEYWORD: SELECT
IDENTIFIER: id
DELIMITER: ,
IDENTIFIER: name
KEYWORD: FROM
IDENTIFIER: users
KEYWORD: WHERE
IDENTIFIER: age
OPERATOR: >=
NUMBER: 18
```

### AST Output:
```
SELECT_STATEMENT
  COLUMN_LIST
    IDENTIFIER: id
    IDENTIFIER: name
  TABLE: users
  WHERE_CLAUSE
    CONDITION
      BINARY_OPERATION: >=
        IDENTIFIER: age
        LITERAL: 18
```


---

## Conclusion

This lab successfully demonstrates how to tokenize input, validate syntax, and represent code structure using an Abstract Syntax Tree. The approach integrates lexical analysis using regular expressions with a recursive-descent parser that validates and interprets simplified SQL queries. Through this, we gain insights into the design and construction of compilers and interpreters, particularly in terms of breaking down source code into hierarchical, semantically meaningful components.


By implementing and visually verifying each component of the parsing pipeline, this lab equips students with both conceptual clarity and practical tools needed for building domain-specific languages, interpreters, and advanced analysis tools for structured input data. how to tokenize input, validate syntax, and represent code structure using an Abstract Syntax Tree. The solution mimics the early stages of a compiler front-end and reinforces foundational concepts in parsing and language analysis. It prepares the ground for more complex language processing and compiler construction.

---

## References
1. [Parsing - Wikipedia](https://en.wikipedia.org/wiki/Parsing)
2. [Abstract Syntax Tree - Wikipedia](https://en.wikipedia.org/wiki/Abstract_syntax_tree)
3. [Python re Documentation](https://docs.python.org/3/library/re.html)

