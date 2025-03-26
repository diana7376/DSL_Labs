from src.regex import generate_with_steps

def main():
    result, steps = generate_with_steps()
    print("Generated String:", result)
    print("\nSequence of Steps:")
    for step in steps:
        print("-", step)

if __name__ == "__main__":
    main()
