from belllm.cli.chats import parse_chats, parse_chat


def parse(args):
    if len(args) < 1:
        print("Usage: belllm <command> [<args>...]")
        return

    command = args[0]

    if command == "chat":
        parse_chat(args[1:])

    elif command == "chats":
        parse_chats(args[1:])

    else:
        print("Unknown command: {}".format(command))

    # todo have internal api running
