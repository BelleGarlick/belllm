import belllm.chats


def parse_chat(args):
    # todo call api
    chat = belllm.chats.create_chat(" ".join(args))
    print(chat.messages[-1].content)

    while True:
        message = input("> ")
        if message == "/bye":
            break
        else:
            chat = belllm.chats.send_message(chat, message)
            print(chat.messages[-1].content)


def parse_chats(args):
    if len(args) < 1:
        chats = belllm.chats.list_chats()

        for chat in chats:
            print(chat[0])
        return

    command = args[0]
    if command == "resume":
        chat = belllm.chats.get_chat(args[1])
        if not chat:
            print("Chat not found.")
            return

        for message in chat.messages:
            print(message['content'])

        while True:
            message = input("> ")
            if message == "/bye":
                break
            else:
                chat = belllm.chats.send_message(chat, message)
                print(chat.messages[-1]['content'])

    elif command == "delete":
        if len(args) < 1:
            print("No chat id provided")
            return

        chat = belllm.chats.get_chat(args[1])
        if not chat:
            print("Chat not found.")
            return
        belllm.chats.delete_chat(chat)
        print("Chat deleted")

    else:
        print("Unknown command.")