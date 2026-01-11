import sys

# Build your own shell
def main():
    while True:
        # Prompt for user input
        sys.stdout.write("$ ")
        sys.stdout.flush()
        command = input()

        # If input is exit
        if command.strip().lower() == "exit":
            break # This will exit the loop

        # if input is echo, print the input back
        elif command.strip().startswith("echo "):
            echo_string = command.strip()[5:] # Since "echo " is 5 characters, we slice from index 5
            print(echo_string)
            continue

        # if input is type, call type_of_command function
        elif command.strip().lower().startswith("type "):
            cmd_to_check = command.strip()[5:]
            result = type_of_command(cmd_to_check)
            print(result.format(command=cmd_to_check))
            continue

        else:
            print(f"{command}: command not found")

def type_of_command(command):
    # bultins list
    bultins = ["echo", "exit", "type"]

    # check if command is in bultins
    if command not in bultins:
        return "{command}: not found"
    
    return "{command} is a shell builtin"
    
if __name__ == "__main__":
    main()
