import os

from dotenv import load_dotenv
from hydra.core.config_store import ConfigStore
from lightning.pytorch.loggers.wandb import WandbLogger

from src.config import full_builds

load_dotenv()

WandbLoggerConfig = full_builds(
    WandbLogger,
    entity=os.environ["WANDB_ENTITY"],
    project=os.environ["WANDB_PROJECT"],
    name=os.environ["WANDB_RUNNAME"],
)


def _register_configs():
    cs = ConfigStore.instance()
    cs.store(group="logger", name="wandb", node=WandbLoggerConfig)
