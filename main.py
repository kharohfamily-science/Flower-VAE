import torch

from src.models.vae.vae import VAE
from src.logger.logger import Logger
from src.data.data_manager import DataManager
from src.trainer.trainer import Trainer
from src.visualization.visualizer import Visualizer
from src.config.config import (
    CHANNELS,
    LEARNING_RATE,
    LATENT_DIM,
    IMG_SIZE,
    KLD_WEIGHT,
    HIDDEN_DIMS,
    EPOCHS,
    DEVICE,
    NAME,
    GAMMA,
)

logger = Logger("try1").logger
logger.info("Logger instantiated")

data_manager = DataManager(verbose=True)
logger.info("Data manager instantiated")

vae = VAE(
    name=NAME,
    channels=CHANNELS,
    latent_dim=LATENT_DIM,
    img_size=IMG_SIZE,
    hidden_dims=HIDDEN_DIMS,
    logger=logger,
)
logger.info("VAE instantiated")

optimizer = torch.optim.Adam(vae.parameters(), lr=LEARNING_RATE)
scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer, gamma=GAMMA)

vae.set_loss_params(kld_weight=KLD_WEIGHT)
loss_fn = vae.vae_loss

trainer = Trainer(
    model=vae,
    optimizer=optimizer,
    loss_fn=loss_fn,
    logger=logger,
)
logger.info("Trainer instantiated")

visualizer = Visualizer(DEVICE)
logger.info("Visualizer instantiated")

trainer.train(
    train_dataloader=data_manager.train_dataloader,
    val_dataloader=data_manager.val_dataloader,
    num_epochs=EPOCHS,
    verbose=True,
    visualizer=visualizer,
)