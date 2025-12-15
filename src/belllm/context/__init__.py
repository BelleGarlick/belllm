import os
from pathlib import Path

from belllm.utils import get_root_dir

CONTEXT_FILE = "context.txt"


# todo do global context
def get_system_message_from_current_context():
    current_path = Path(os.getcwd())

    contexts = []
    for path in [current_path, *current_path.parents]:
        if (path / CONTEXT_FILE).exists():
            with open(path / CONTEXT_FILE, "r") as f:
                contexts.append(f"{str(path)}: {f.read()}")

    contexts.reverse()

    return contexts


def get_system_message_for_global_context():
    fill_path = get_root_dir() / CONTEXT_FILE

    if fill_path.exists():
        with open(fill_path, "r") as f:
            return f.read()

    return None


def set_system_message_for_global_context(message: str):
    fill_path = get_root_dir() / CONTEXT_FILE
    fill_path.parent.mkdir(parents=True, exist_ok=True)

    with open(fill_path, "w+") as f:
        f.write(message)


def clear_system_message_for_global_context():
    fill_path = get_root_dir() / CONTEXT_FILE
    if fill_path.exists():
        os.remove(fill_path)


# todo sort this
def _initialise():
    contexts = get_system_message_from_current_context()

    return "\n".join(contexts)
