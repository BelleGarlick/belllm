from typing import List


def parse_project_context(args: List[str]):
    if len(args) < 1:
        for value in get_system_message_from_current_context():
            print(value)
        return

    command = args[0]
    if command == "help":
        print("`belllm project context`: Shows the project system message")
        print("`belllm project context help`: Shows this help message")
        print("`belllm project context set <message>`: Sets the context for this projects LLM system message")
        print("`belllm project context clear`: Clears the context for the project's LLM system message")

    elif command == "set":
        current_path = Path(os.getcwd()) / CONTEXT_FILE
        with open(current_path, "w+") as f:
            f.write(" ".join(args[1:]))
            print(f"Updated context of {os.getcwd()}")

    elif command == "clear":
        current_path = Path(os.getcwd()) / CONTEXT_FILE
        if current_path.exists():
            os.remove(current_path)
        print(f"Cleared context of {os.getcwd()}")
