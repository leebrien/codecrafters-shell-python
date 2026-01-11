import sys

# Build your own shell
def main():
    while True:
        # Prompt for user input
        sys.stdout.write("$ ")
        command = input()

        # If input is exit
        if command.lower() == "exit":
            break # This will exit the loop
        
        print(f"{command}: command not found")

if __name__ == "__main__":
    main()
