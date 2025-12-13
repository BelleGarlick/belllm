import json
import sqlite3

from belllm.chats.models import Chat
from belllm.utils import get_root_dir


def _get_connection():
    conn = sqlite3.connect(get_root_dir() / 'chats.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS chats
                      (
                          chat_id text PRIMARY KEY,
                          created_at text,
                          updated_at text,
                          chat text
                      )''')

    conn.commit()

    return conn


def put_chat(chat: Chat):
    data = json.loads(chat.model_dump_json())

    with _get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            'INSERT INTO chats VALUES (?, ?, ?, ?) ON CONFLICT DO UPDATE SET updated_at=excluded.updated_at, chat=excluded.chat', (
                chat.chat_id,
                chat.created_at,
                chat.updated_at,
                json.dumps(data['messages']),
            ))
        conn.commit()


def delete_chat(chat_id: str):
    with _get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            'DELETE FROM chats where chat_id=?', (chat_id,))
        conn.commit()


def get_chat(chat_id: str):
    with _get_connection() as conn:
        cursor = conn.cursor()

        res = cursor.execute(
            'SELECT chat_id, created_at, updated_at, chat FROM chats where chat_id = ?', (chat_id,))
        data = res.fetchone()

        if data:
            return Chat(
                chat_id=data[0],
                created_at=data[1],
                updated_at=data[2],
                messages=json.loads(data[3]),
            )


def list_chats():
    with _get_connection() as conn:
        cursor = conn.cursor()

        res = cursor.execute(
            'SELECT chat_id, created_at, updated_at FROM chats')
        return res.fetchall()
