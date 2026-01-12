import sys
import os
import subprocess
import shlex
from contextlib import redirect_stdout

def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        
        command_line = sys.stdin.readline().strip()

        # Handle empty input
        if not command_line:
            continue

        # Parsing the string input into command and arguments
        # shlex.split correctly handles quoted strings and escape characters
        parts = shlex.split(command_line)
        command = parts[0]
        args = parts[1:]

        
        """
        Built-in commands:
        - exit: Exit the shell
        - pwd: Print the current working directory
        - echo: Print arguments (string) to the console
        - cat: Concatenate and display file contents
        - type: Identify if a command is built-in or external
        - cd: Change the current working directory
        """
        
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
            if args and args[-2] == '>':
                redirect_output_to_file(args[-1], " ".join(args[1:-2]))
            else:
                print(" ".join(args))
        # Cat command
        elif command == "cat":
            if args:
                for filename in args:
                    try:
                        with open(filename, 'r') as file:
                            print(file.read(), end='')
                    except FileNotFoundError:
                        print(f"cat: {filename}: No such file or directory")
            else:
                # If no arguments, read from standard input
                print(sys.stdin.read(), end='')
                        
        # Type command
        elif command == "type":
            if args:
                print(type_of_command(args[0]).format(command=args[0]))
            continue
        # cd command
        elif command == "cd":
            if args:
                path = os.path.expanduser(args[0])
                try:
                    os.chdir(path)
                except FileNotFoundError:
                    print(f"cd: {args[0]}: No such file or directory")

            # cd with no arguments goes to the home directory
            else:
                os.chdir(os.path.expanduser("~"))

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
    builtins = ["echo", "exit", "type", "pwd"]
    if command in builtins:
        return "{command} is a shell builtin"
    
    path = find_in_path(command)
    if path:
        return f"{{command}} is {path}"
        
    return "{command}: not found"

def redirect_output_to_file(file_path, command_line):
    with open(file_path, 'w') as file:
        with redirect_stdout(file):
            parts = shlex.split(command_line)
            subprocess.run(parts)

if __name__ == "__main__":
    main()