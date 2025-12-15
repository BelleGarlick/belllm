import belllm
import belllm.plugins
from belllm.cli.chats import parse_chats, parse_chat
from belllm.cli.project import parse_project
from belllm.cli.context import parse_context
from belllm.cli.plugins import parse_plugins


def parse(args):
    plugins = belllm.plugins.get_cli_plugins()

    if len(args) < 1:
        commands = ["chat", "chats", "context", *list(plugins)]
        print(f"Usage: belllm <{"|".join(commands)}> [<args>...]")
        return

    command = args[0]

    if command == "chat":
        parse_chat(args[1:])

    elif command == "chats":
        parse_chats(args[1:])

    elif command == "context":
        parse_context(args[1:])

    elif command == "project":
        parse_project(args[1:])

    elif command == "plugins":
        parse_plugins(args[1:])

    elif command in plugins:
        plugins[command](args[1:])

    else:
        print("Unknown command: {}".format(command))

    # todo have internal api running
