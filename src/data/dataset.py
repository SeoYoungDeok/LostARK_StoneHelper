from typing import Any

import numpy as np
import torch
from torchvision.datasets import MNIST


class MNISTDataSet(MNIST):
    def __init__(
        self,
        root: str = "./data",
        train: bool = True,
        transforms: Any = None,
        download: bool = True,
    ):
        super().__init__(
            root=root, train=train, transform=transforms, download=download
        )

    def __getitem__(self, index):
        img, target = self.data[index], int(self.targets[index])

        if self.transform:
            img = self.transform(image=np.array(img) / 255)["image"]

        return img.to(dtype=torch.float32), target
