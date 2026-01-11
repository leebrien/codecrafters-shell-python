import sys
import os
import subprocess
import shlex

def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        
        command_line = sys.stdin.readline().strip()

        # Handle empty input
        if not command_line:
            continue

        # Parsing the input
        # shlex.split correctly handles quoted strings and escape characters
        parts = shlex.split(command_line)
        command = parts[0]
        args = parts[1:]

        # Exit command
        if command == "exit":
            break
        
        elif command == "pwd":
            # This asks the OS kernel for the current working directory
            print(os.getcwd())
            pass

        # Echo command
        elif command == "echo":
            # Use " ".join to handle multiple arguments (ex. echo arg1 arg2)
            print(" ".join(args))

        # Type command
        elif command == "type":
            if args:
                print(type_of_command(args[0]).format(command=args[0]))
            continue

        # External programs
        else:
            full_path = find_in_path(command)
            if full_path:
                # Run the external program with arguments
                # We pass the full parts list to ensure command and args stay synced
                subprocess.run(parts)
            else:
                print(f"{command}: command not found")

def find_in_path(command):
    path_env = os.getenv("PATH")
    if path_env:
        for directory in path_env.split(os.pathsep):
            full_path = os.path.join(directory, command)
            if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                return full_path
    return None

def type_of_command(command):
    builtins = ["echo", "exit", "type"]
    if command in builtins:
        return "{command} is a shell builtin"
    
    path = find_in_path(command)
    if path:
        return f"{{command}} is {path}"
        
    return "{command}: not found"

if __name__ == "__main__":
    main()