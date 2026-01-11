import sys

# Build your own shell
def main():
    while True:
        # Prompt for user input
        sys.stdout.write("$ ")
        command = input()

        # if input is echo, print the input back
        if (command.strip().startswith("echo ")):
            echo_string = command.strip()[5:] # Since "echo " is 5 characters, we slice from index 5
            print(echo_string)
            continue
        
        # If input is exit
        if command.strip().lower() == "exit":
            break # This will exit the loop

        print(f"{command}: command not found")

if __name__ == "__main__":
    main()
