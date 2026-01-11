import sys

# Build your own shell
def main():
    while True:
        # Prompt for user input
        sys.stdout.write("$ ")
        command = input()
        print(f"{command}: command not found")

        # If input is exit
        if command.lower() == "exit":
            break # This will exit the loop

if __name__ == "__main__":
    main()
