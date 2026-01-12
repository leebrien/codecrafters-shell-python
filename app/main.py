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

        # Handle output redirection
        if '>' in parts or '1>' in parts or '2>' in parts or '>>' in parts or '1>>' in parts or '2>>' in parts:
            redirect_index = -1
            if '>' in parts:
                redirect_index = parts.index('>')
            elif '1>' in parts:
                redirect_index = parts.index('1>')
            elif '2>' in parts:
                redirect_index = parts.index('2>')
            elif '>>' in parts:
                redirect_index = parts.index('>>')
            elif '1>>' in parts:
                redirect_index = parts.index('1>>')
            elif '2>>' in parts:
                redirect_index = parts.index('2>>')
                
            if redirect_index < len(parts) - 1:
                output_file = parts[redirect_index + 1]
                command_parts = parts[:redirect_index]

                # stderr redirection
                if parts[redirect_index] == '2>':
                    redirect_error_to_file(output_file, " ".join(command_parts))
                # stdout redirection
                elif parts[redirect_index] in ('>', '1>'):
                    redirect_output_to_file(output_file, " ".join(command_parts))
                # stdout append redirection
                elif parts[redirect_index] in ('>>', '1>>'):
                    append_output_to_file(output_file, " ".join(command_parts))
                # stderr append redirection
                elif parts[redirect_index] == '2>>':
                    append_error_to_file(output_file, " ".join(command_parts))
                continue    

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
            continue
        # Echo command
        elif command == "echo":
            # Use " ".join to handle multiple arguments (ex. echo arg1 arg2)
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
    builtins = ["echo", "exit", "type", "pwd", "cd"]
    if command in builtins:
        return "{command} is a shell builtin"
    
    path = find_in_path(command)
    if path:
        return f"{{command}} is {path}"
        
    return "{command}: not found"

def redirect_output_to_file(file_path, command_line):
    # Create directory only if there's a directory path
    dir_path = os.path.dirname(file_path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    
    with open(file_path, 'w') as file:
        with redirect_stdout(file):
            parts = shlex.split(command_line)
            subprocess.run(parts, stdout=file)

def redirect_error_to_file(file_path, command_line):
    # Create directory only if there's a directory path
    dir_path = os.path.dirname(file_path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    
    with open(file_path, 'w') as file:
        parts = shlex.split(command_line)
        subprocess.run(parts, stderr=file)

def append_output_to_file(file_path, command_line):
    # Create directory only if there's a directory path
    dir_path = os.path.dirname(file_path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    
    with open(file_path, 'a') as file:
        with redirect_stdout(file):
            parts = shlex.split(command_line)
            subprocess.run(parts, stdout=file)

def append_error_to_file(file_path, command_line):
    # Create directory only if there's a directory path
    dir_path = os.path.dirname(file_path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    
    with open(file_path, 'a') as file:
        parts = shlex.split(command_line)
        subprocess.run(parts, stderr=file)

if __name__ == "__main__":
    main()