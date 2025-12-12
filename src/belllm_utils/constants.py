import os
from pathlib import Path

ROOT_DIR = r"~/Developer/Belllm/belllm/data"


def get_root_dir():
    return Path(os.path.expanduser(ROOT_DIR))
