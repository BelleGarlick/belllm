from pathlib import Path

import webdataset as wds
from bellm.cli.dataset import DatasetDownloadCommand
from bellm.dataset.downloaders.allenai_c4 import download_c4
from bellm.dataset.downloaders.open_assistant_oasst2 import download_oasst


def download_foundation_model_datasets(root: Path):
    foundation_path = root / "foundation"

    foundation_path.mkdir(parents=True, exist_ok=True)

    with wds.ShardWriter(str(foundation_path / "training-%06d.tar"), maxcount=100000) as train_writer:
        with wds.ShardWriter(str(foundation_path / "validation-%06d.tar"), maxcount=100000) as validation_writer:
            download_c4(train_writer, validation_writer)


def download_instruction_model_datasets(root: Path):
    # psyche/glaiveai-reasoning-v1-20m
    # psyche/MultiSynt-MT-Reasoning
    # DataMuncher-Labs/UltraMath-Reasoning-Small
    # MaLA-LM/mala-code-reasoning
    # https://huggingface.co/datasets/ianncity/KIMI-K2.5-1000000x
    # https://huggingface.co/datasets/nohurry/Opus-4.6-Reasoning-3000x-filtered
    # https://huggingface.co/datasets/Modotte/CodeX-2M-Thinking
    # zake7749/Qwen3-Coder-Next-Open-Code-SFT
    # DCAgent/c1_gpt53_codex
    # ronantakizawa/github-codereview
    # Zigeng/DMax-LLaDA-2.0-Mini-Code-Trajectories
    instruction_path = root / "instruction"

    instruction_path.mkdir(parents=True, exist_ok=True)

    with wds.ShardWriter(str(instruction_path / "training-%06d.tar"), maxcount=100000) as train_writer:
        with wds.ShardWriter(str(instruction_path / "validation-%06d.tar"), maxcount=100000) as validation_writer:
            download_oasst(train_writer, validation_writer)


def download_dataset(download_config: DatasetDownloadCommand):
    download_foundation_model_datasets(Path(download_config.path))
    download_instruction_model_datasets(Path(download_config.path))
