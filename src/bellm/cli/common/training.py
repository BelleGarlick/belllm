from pydantic import BaseModel, Field


class TrainingConfig(BaseModel):

    epochs: int = Field(default=1000, description="The number of epochs to train for")

    batch_size: int = Field(default=10, description="The training batch size")

    use_random_initial_noise: bool = Field(default=False, description="Whether to use random initial noise. If false, a equal probability (max entropy) noise will be used.")
