import os
from pathlib import Path
from .project_context import parse_project_context


def parse_project(args):
    if len(args) < 1:
        # todo list proejcts dir
        print("Usage: belllm project <help|create|context>")
        return

    command = args[0]
    if command == "help":
        print("`belllm project help`: Shows this help message")
        print("`belllm project create`: Create a project in the current directory")
        print("`belllm project context`: Get the project context")
        print("`belllm project context help`: Get the help for the project context")
        print("`belllm project context set <message>`: Set the project context")
        print("`belllm project context clear`: Clear the project context")

    elif command == "create":
        current_working_dir = Path(os.getcwd()) / ".belllm"
        if current_working_dir.exists():
            print("Project already exists in this directory. Skipping creation.")
            return

        current_working_dir.mkdir()
        print(f"Project created at {str(current_working_dir)}")

    elif command == "context":
        parse_project_context(args[1:])

    else:
        print("Unknown command.")
