from datetime import datetime
from typing import List
from pydantic import BaseModel


class Message(BaseModel):
    content: str
    tool_name: str | None = None
    role: str


ChatMessages = List[Message]


class Chat(BaseModel):

    chat_id: str

    created_at: datetime

    updated_at: datetime

    messages: ChatMessages
