import os
from pathlib import Path

from belllm.utils.constants import ROOT_DIR


def get_root_dir():
    return Path(os.path.expanduser(ROOT_DIR))
