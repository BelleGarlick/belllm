# Datasets

Bellm uses a variety of datasets for training, ranging from large-scale web crawls for foundational pre-training to curated dialogue datasets for instruction tuning.

### Formats

Datasets are stored in the **WebDataset** format. This format consists of sharded `.tar` files, where each entry in the tarball represents a data sample. This allows for efficient streaming and shuffling of large datasets during training.

The specific keys within each sample vary depending on the dataset type:

- **Foundational Data (e.g., C4):**
    - `__key__`: Unique identifier for the sample.
    - `text`: The raw text content.
    - `dataset.source`: The source of the dataset (e.g., `allenai/c4`).
    - `dataset.name`: The specific configuration or language (e.g., `en`).

- **Instructional Data (e.g., OASST2):**
    - `__key__`: Unique identifier for the sample.
    - `json`: A list of message objects representing a conversation. Each message has a `message` (text) and a `role` (`user` or `assistant`).
    - `dataset.source`: The source of the dataset (e.g., `oasst`).
    - `dataset.name`: The specific configuration.

## Downloading the Datasets

Whilst you can create your own dataset, you can also download preselected ones. These are what are used for the current version of bellm.

To download the datasets, you use the `bellm` CLI. The download process pulls data from sources like Hugging Face and packages them into WebDataset shards.

### Download Command

To trigger the download, run: 
```shell
python -m bellm.cli dataset download --path <dataset_download_path>
```

This will download the datasets to the specified path. The directory structure will look like this:
- `<path>/foundation/`: Contains foundational training and validation shards.
- `<path>/instruction/`: Contains instructional training and validation shards.

Currently, it downloads:
1. **allenai/c4** (English): Used for foundational pre-training.
2. **OpenAssistant/oasst2**: Used for instruction tuning.


# TODO create tokenise cashing items
# todo also preprocess

## Future Work

- **Multi-modal data**: Support for non-text inputs.
- **More datasets**: Integration of additional benchmarks and diverse data sources.
- **Weighted sampling**: Ability to weight different datasets during the processing stage.
- **Data Filtering**: Automated removal of bias, toxic content, and low-quality data.
