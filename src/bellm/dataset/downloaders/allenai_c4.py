from datasets import load_dataset
from tqdm import tqdm
import webdataset as wds


PATH = "allenai/c4"
NAME = "en"


def download_c4_english_train(
    writer: wds.ShardWriter,
    split: str,
    max_length: int
):
    # if not should_redownload(metadata_path, dataset_split_id):
    #     return

    dataset = load_dataset(
        PATH,
        NAME,
        split=split,
        streaming=True,
    )

    items = dataset.take(max_length)['text']

    for i, item in tqdm(enumerate(items), total=max_length):
        writer.write({
            "__key__": f"allenai_c4_en_{i}",
            "text": item,
            "dataset.source": "allenai/c4",
            "dataset.name": "en",
        })


def download_c4(train_writer, validation_writer):
    download_c4_english_train(
        train_writer,
        "train",
        10_000_000
    )
    download_c4_english_train(
        validation_writer,
        "validation",
        500_000
    )
