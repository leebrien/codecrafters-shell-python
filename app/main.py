import sys
import os

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
    
    # check if command is an executable in PATH
    path_env = os.getenv("PATH")
    if path_env:
        paths = path_env.split(os.pathsep)
        for path in paths:
            full_path = os.path.join(path, command)
            if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                return "{command} is {full_path}".format(command=command, full_path=full_path)
            
    return "{command} is a shell builtin"
    
if __name__ == "__main__":
    main()
