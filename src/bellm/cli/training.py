from pydantic import Field

from bellm.cli.common.dataset import DatasetConfig
from bellm.cli.common.model import ModelConfig
from bellm.cli.common.training import TrainingConfig
from clpi import BaseClpIModel


class FoundationModelTrainingConfig(BaseClpIModel):

    name: str = Field(description="The run name of the experiment")

    model: ModelConfig = Field(description="The model config to train")

    dataset: DatasetConfig = Field(description="The dataset config to train on")

    training: TrainingConfig = Field(description="The training config")

    def run(self, *args, **kwargs):
        from bellm.training.foundational_model import train_foundational_model

        train_foundational_model(self)
