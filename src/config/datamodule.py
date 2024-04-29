from hydra.core.config_store import ConfigStore
from torch.utils.data import DataLoader

from src.config import partial_builds
from src.data.dataset import MNISTDataSet

MNISTTrainDatasetConfig = partial_builds(
    MNISTDataSet,
    root="./data",
    train=True,
    transforms=None,
    download=True,
)

MNISTValidationDatasetConfig = partial_builds(
    MNISTDataSet,
    root="./data",
    train=True,
    transforms=None,
    download=True,
)

MNISTTestDatasetConfig = partial_builds(
    MNISTDataSet,
    root="./data",
    train=False,
    transforms=None,
    download=True,
)

MNISTTrainDataloaderConfig = partial_builds(
    DataLoader,
    batch_size=64,
    shuffle=True,
    num_workers=12,
    prefetch_factor=2,
    persistent_workers=True,
    pin_memory=True,
)

MNISTValidationDataloaderConfig = partial_builds(
    DataLoader,
    batch_size=64,
    num_workers=12,
    prefetch_factor=2,
    persistent_workers=True,
    pin_memory=True,
)

MNISTTestDataloaderConfig = partial_builds(
    DataLoader,
    batch_size=64,
    num_workers=12,
    prefetch_factor=2,
    persistent_workers=True,
    pin_memory=True,
)


def _register_configs():
    cs = ConfigStore.instance()

    cs.store(
        group="train_dataset",
        name="basic_train_dataset",
        node=MNISTTrainDatasetConfig,
    )
    cs.store(
        group="val_dataset",
        name="basic_val_dataset",
        node=MNISTValidationDatasetConfig,
    )
    cs.store(
        group="test_dataset",
        name="basic_test_dataset",
        node=MNISTTestDatasetConfig,
    )

    cs.store(
        group="train_loader",
        name="basic_train_loader",
        node=MNISTTrainDataloaderConfig,
    )
    cs.store(
        group="val_loader",
        name="basic_val_loader",
        node=MNISTValidationDataloaderConfig,
    )
    cs.store(
        group="test_loader",
        name="basic_test_loader",
        node=MNISTTestDataloaderConfig,
    )
