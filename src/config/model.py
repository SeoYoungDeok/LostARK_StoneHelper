from hydra.core.config_store import ConfigStore

from src.config import full_builds
from src.models.resnet import ResNet

ResNetConfig = full_builds(
    ResNet, in_channels=1, start_channels=64, class_num=10, blocks=[2, 2, 2, 2]
)


def _register_configs():
    cs = ConfigStore.instance()

    cs.store(
        group="architecture",
        name="resnet",
        node=ResNetConfig,
    )
