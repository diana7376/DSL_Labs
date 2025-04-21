from .lexer import TokenType, sql_lexer
from .ast import ASTNode, ASTNodeType



class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.token_index = -1
        self.advance()

    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            self.current_token = None
        return self.current_token

    def parse(self):
        if not self.tokens:
            return None

        # Check for SELECT statement
        if (self.current_token and
                self.current_token[0] == TokenType.KEYWORD and
                self.current_token[1].upper() == "SELECT"):
            return self.parse_select()
        else:
            raise SyntaxError("Only SELECT statements are supported at this time")

    def parse_select(self):
        select_node = ASTNode(ASTNodeType.SELECT_STATEMENT)

        # Consume SELECT keyword
        self.advance()

        # Parse columns
        select_node.children.append(self.parse_column_list())

        # Expect FROM keyword
        if not (self.current_token and
                self.current_token[0] == TokenType.KEYWORD and
                self.current_token[1].upper() == "FROM"):
            raise SyntaxError("Expected FROM clause")
        self.advance()

        # Parse table
        select_node.children.append(self.parse_table())

        # Check for WHERE clause
        if (self.current_token and
                self.current_token[0] == TokenType.KEYWORD and
                self.current_token[1].upper() == "WHERE"):
            self.advance()
            select_node.children.append(self.parse_where_clause())

        return select_node

    def parse_column_list(self):
        column_list_node = ASTNode(ASTNodeType.COLUMN_LIST)

        while True:
            if self.current_token[0] == TokenType.IDENTIFIER:
                column_list_node.children.append(
                    ASTNode(ASTNodeType.IDENTIFIER, self.current_token[1])
                )
                self.advance()

                # Check for comma (more columns)
                if (self.current_token and
                        self.current_token[0] == TokenType.DELIMITER and
                        self.current_token[1] == ","):
                    self.advance()
                    continue
                else:
                    break
            else:
                break

        return column_list_node

    def parse_table(self):
        if (self.current_token and
                self.current_token[0] == TokenType.IDENTIFIER):
            table_node = ASTNode(ASTNodeType.TABLE, self.current_token[1])
            self.advance()
            return table_node
        else:
            raise SyntaxError("Expected table name after FROM")

    def parse_where_clause(self):
        where_node = ASTNode(ASTNodeType.WHERE_CLAUSE)
        where_node.children.append(self.parse_condition())
        return where_node

    def parse_condition(self):
        left = self.parse_expression()

        if not (self.current_token and
                self.current_token[0] == TokenType.OPERATOR):
            raise SyntaxError("Expected operator in condition")

        operator = self.current_token[1]
        self.advance()

        right = self.parse_expression()

        condition_node = ASTNode(ASTNodeType.CONDITION)
        condition_node.children.append(
            ASTNode(ASTNodeType.BINARY_OPERATION, operator, [left, right])
        )

        return condition_node

    def parse_expression(self):
        if not self.current_token:
            raise SyntaxError("Unexpected end of input")

        if self.current_token[0] == TokenType.IDENTIFIER:
            node = ASTNode(ASTNodeType.IDENTIFIER, self.current_token[1])
            self.advance()
            return node
        elif self.current_token[0] in (TokenType.NUMBER, TokenType.STRING):
            node = ASTNode(ASTNodeType.LITERAL, self.current_token[1])
            self.advance()
            return node
        else:
            raise SyntaxError(f"Unexpected token in expression: {self.current_token[1]}")


def sql_parser(query):
    tokens = sql_lexer(query)
    parser = Parser(tokens)
    return parser.parse()