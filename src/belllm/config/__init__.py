import json
import os

from belllm.utils import get_root_dir
from belllm.utils.exceptions import MissingConfigException


CONFIG = None


def get_config():
    global CONFIG
    if CONFIG:
        return CONFIG

    config_file = get_root_dir() / "belllm.json"

    if not os.path.exists(config_file):
        raise MissingConfigException("Missing config file. Please run `belllm configure` first.")

    with open(config_file) as f:
        CONFIG = json.load(f)

    return CONFIG


def get(key: str, default=None):
    branch = get_config()

    key_tokens = key.split(".")
    for token in key_tokens:
        if token not in branch:
            if default is not None:
                return default
            else:
                raise MissingConfigException(f"{key} is not configured. Please run `belllm configure` first.")
        branch = branch[token]

    return branch
