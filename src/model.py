import torch
import torch.nn.functional as F
from lightning import LightningModule
from torch import nn
from torch.optim import Optimizer
from torch.optim.lr_scheduler import LRScheduler
from torchmetrics import MeanMetric


class Model(LightningModule):
    def __init__(
        self,
        model: nn.Module,
        optimizer: Optimizer,
        loss: nn.Module,
        scheduler: LRScheduler,
    ):
        super().__init__()
        self.model = model
        self.loss = loss
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.example_input_array = torch.zeros(1, 1, 28, 28)
        self.val_loss = MeanMetric()
        self.test_loss = MeanMetric()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.model(x)

    def training_step(self, batch: torch.Tensor, batch_idx: int) -> torch.Tensor:
        x, y = batch
        pred = self.forward(x)
        loss = self.loss(pred, F.one_hot(y, num_classes=10).to(dtype=torch.float32))

        self.log(
            name="train_loss",
            value=round(loss.item(), 4),
            on_step=True,
            on_epoch=False,
            logger=True,
        )
        return loss

    def validation_step(self, batch: torch.Tensor, batch_idx: int) -> None:
        x, y = batch
        pred = self.forward(x)
        loss = self.loss(pred, F.one_hot(y, num_classes=10).to(dtype=torch.float32))

        self.val_loss(loss)

        self.log(
            name="val_loss",
            value=self.val_loss,
            on_step=False,
            on_epoch=True,
            logger=True,
        )

    def test_step(self, batch: torch.Tensor, batch_idx: int) -> None:
        x, y = batch
        pred = self.forward(x)
        loss = self.loss(pred, F.one_hot(y, num_classes=10).to(dtype=torch.float32))

        self.test_loss(loss)

        self.log(
            name="test_loss",
            value=self.test_loss,
            on_step=False,
            on_epoch=True,
            logger=True,
        )

    def configure_optimizers(self):
        optimizer = self.optimizer(params=self.parameters())
        scheduler = self.scheduler(
            optimizer=optimizer,
            total_steps=self.trainer.estimated_stepping_batches,
        )

        return {
            "optimizer": optimizer,
            "lr_scheduler": {
                "scheduler": scheduler,
                "interval": "step",
                "frequency": 1,
            },
        }

    def optimizer_zero_grad(
        self, epoch: int, batch_idx: int, optimizer: Optimizer
    ) -> None:
        optimizer.zero_grad(set_to_none=True)
