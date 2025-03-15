from src.lexer import sql_lexer

def main():
    while True:
        try:
            query = input("SQL> ").strip()
            if query.lower() == "exit":
                print("Exiting lexer...")
                break

            tokens = sql_lexer(query)
            print("\nTokens:")
            for token_type, value in tokens:
                print(f"{token_type.name}: {value}")

            print("\n")

        except KeyboardInterrupt:
            print("\nExiting lexer...")
            break

if __name__ == "__main__":
    main()
