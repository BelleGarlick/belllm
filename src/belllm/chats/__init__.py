from datetime import datetime
import uuid

import belllm.llm
from belllm.chats import database
from belllm.chats.models import Chat, Message


def create_chat(message: str):
    chat = Chat(
        chat_id=str(uuid.uuid4()),
        created_at=datetime.now(),
        updated_at=datetime.now(),
        messages=[Message(role="user", content=message)]
    )

    belllm.llm.chat(chat)

    database.put_chat(chat)

    return chat


def send_message(chat, message):
    chat.messages.append(Message(role="user", content=message))
    belllm.llm.chat(chat)
    database.put_chat(chat)
    return chat


def get_chat(chat_id: str) -> Chat | None:
    return database.get_chat(chat_id)


def list_chats():
    return database.list_chats()


def delete_chat(chat: Chat):
    database.delete_chat(chat.chat_id)
