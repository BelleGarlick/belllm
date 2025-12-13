from fastapi import APIRouter, HTTPException

import belllm.chats

chats_router = APIRouter(prefix="/chats", tags=["chats"])

# todo enable streaming

@chats_router.get("")
def get_chats():
    chats = belllm.chats.list_chats()

    return {
        "chats": [
            x[0] for x in chats
        ]
    }




@chats_router.post("")
def new_chat(message: str):
    chat = belllm.chats.create_chat(message)

    return {
        "chat": chat
    }


@chats_router.get("/{chat_id}")
def get_chat(chat_id: str):
    chat = belllm.chats.get_chat(chat_id)

    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    return {
        "chat": chat
    }


@chats_router.post("/{chat_id}")
def send_message(chat_id: str, message: str):
    chat = belllm.chats.get_chat(chat_id)

    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    belllm.chats.send_message(chat, message)

    return {
        "chat": chat
    }



@chats_router.delete("/{chat_id}")
def delete_chat(chat_id: str):
    chat = belllm.chats.get_chat(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    belllm.chats.delete_chat(chat)

    return "ok"
