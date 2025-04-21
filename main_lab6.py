from src.parser import sql_parser
from src.lexer import sql_lexer
from src.ast import ASTNode

def main():
    print("SQL Parser and AST Builder")
    print("Enter SQL queries or 'exit' to quit\n")

    while True:
        try:
            query = input("SQL> ").strip()
            if query.lower() == "exit":
                print("Exiting parser...")
                break

            # Lexical analysis
            tokens = sql_lexer(query)
            print("\nLexical Analysis Results:")
            for token_type, value in tokens:
                print(f"{token_type.name}: {value}")

            # Syntax analysis and AST building
            print("\nSyntax Analysis Results:")
            try:
                ast = sql_parser(query)
                if ast:
                    print("Abstract Syntax Tree:")
                    print(ast)
                else:
                    print("No AST generated (empty or unsupported query)")
            except Exception as e:
                print(f"Syntax Error: {e}")

            print("\n" + "=" * 50 + "\n")

        except KeyboardInterrupt:
            print("\nExiting parser...")
            break

if __name__ == "__main__":
    main()
