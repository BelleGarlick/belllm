from typing import List

from belllm.context import get_system_message_for_global_context, set_system_message_for_global_context, clear_system_message_for_global_context


def parse_context(args: List[str]):
    if len(args) < 1:
        global_context = get_system_message_for_global_context()
        if not global_context:
            print("No context set.")
        else:
            print(global_context)
        return

    command = args[0]
    if command == "help":
        print("`belllm context`: Shows the global system message")
        print("`belllm context help`: Shows this help message")
        print("`belllm context set <message>`: Sets the context for the LLM system message")
        print("`belllm context clear`: Clears the context for the LLM system message")

    elif command == "set":
        if len(args) < 2:
            print("Please provide a message to set as the context.")
            return

        set_system_message_for_global_context(" ".join(args[1:]))
        print("Global context set.")

    elif command == "clear":
        clear_system_message_for_global_context()
        print("Global context cleared.")

    else:
        print("Unknown command.")
