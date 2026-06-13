from pydantic import Field

from clpi import BaseClpIModel


class DatasetDownloadCommand(BaseClpIModel):

    path: str = Field(description="The file path to download the dataset")

    def run(self, *args, **kwargs):
        from bellm.dataset.downloader import download_dataset

        print(self.path)

        download_dataset(self)
