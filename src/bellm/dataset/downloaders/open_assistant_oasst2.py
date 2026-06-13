from pathlib import Path

from datasets import load_dataset
import webdataset as wds

PATH = "OpenAssistant/oasst2"


def oasst_adapter(data):
    items = [x for x in data]
    items_map = {x["message_id"]: {"children": [], "text": x['text'], "lang": x["lang"], "role": x["role"]} for x in items}

    heads = []

    for item in items:
        if item["parent_id"] is None:
            heads.append(items_map[item["message_id"]])
        else:
            item_chain = items_map[item["message_id"]]
            items_map[item["parent_id"]]["children"].append(item_chain)

    # Aim for english convos only
    heads = [x for x in heads if x["lang"] == "en"]

    # Traverse the tree forming the conversations
    conversations = []
    def traverse_head(items, conversation_chain):
        if len(items) == 0:
            conversations.append(conversation_chain)

        for item in items:
            traverse_head(
                item['children'],
                [*conversation_chain, {
                    "message": item["text"],
                    "role": {
                        "prompter": "user",
                        "assistant": "assistant"
                    }[item["role"]]
                }]
            )

    # Trigger breath first search
    traverse_head(heads, [])

    return conversations


def download_oasst_split(writer: wds.ShardWriter, split: str):
    # if not should_redownload(metadata_path, dataset_split_id):
    #     return

    dataset = load_dataset(
        PATH,
        split=split,
        streaming=True,
    )

    # Load all dataset items, needed to create the conversation tree
    items = list(dataset)
    items = oasst_adapter(items)

    for i, item in enumerate(items):
        writer.write({
            "__key__": f"oasst_{split}_{i}",
            "json": item,
            "dataset.source": "oasst",
            "dataset.name": "default",
        })


def download_oasst(train_writer, validation_writer):
    download_oasst_split(train_writer, "train")
    download_oasst_split(validation_writer, "validation")
