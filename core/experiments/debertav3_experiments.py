from core.base_models.debertav3_models import DebertaV3ForClassificationV1
from core.dataloaders.focus.lighting.debertav3_lighting_dataloaders import (
    DebertaV3FoCusLightningDataModuleV1,
    DebertaV3FoCusLightningDataModuleV2,
    DebertaV3FoCusLightningDataModuleV3,
)
from core.hyperparameters.debertav3_hyperparameters import DebertaV3HyperparametersV1
from core.hyperparameters.lighting_hyperparameters import LightingHyperparametersV1
from core.lighting_models.debertav3_lighting import DebertaV3LightningModelV1
from core.loggers.wandb_logger import WandbLoggerV2
from core.utils import ExperimentArgumentParserV1, TrainArgumentsV1

from pytorch_lightning import Trainer
from pytorch_lightning import seed_everything
from pytorch_lightning.callbacks import ModelCheckpoint

from transformers import DebertaV2Config, DebertaV2Tokenizer  # type: ignore


def experiment_1():
    """
    бинарная классифицикация
    для этого я использую последний вопрос пользователя и кандидатов
    из knowledge_candidates. где предложению которое использовалось в
    ответе соответсвует 1, а остальным 0. для группировки по диалогам пришлось испльзовать
    уникальные id чтобы потом посчитать accuracy сравнимую с результатами модели bart.
    """
    parser = ExperimentArgumentParserV1()
    args: TrainArgumentsV1 = parser.args

    max_epochs = 1
    if args.debug_status == 1:
        max_epochs = 1

    lighting_hyperparameters = LightingHyperparametersV1(
        precision=16,
        max_epochs=max_epochs,
    ).__dict__

    hyperparameters = DebertaV3HyperparametersV1(
        lighting_hyperparameters=lighting_hyperparameters,
        train_batch_size=16,
        valid_batch_size=16,
    )
    seed_everything(hyperparameters.seed)

    tokenizer = DebertaV2Tokenizer.from_pretrained(
        hyperparameters.model_name,
    )
    is_debug = args.debug_status

    data_module = DebertaV3FoCusLightningDataModuleV1(
        train_path_dataset="./datasets/FoCus/train_focus.json",
        valid_path_dataset="./datasets/FoCus/valid_focus.json",
        hyperparameters=hyperparameters,
        tokenizer=tokenizer,  # type: ignore
        debug_status=is_debug,
    )
    base_model = DebertaV3ForClassificationV1(
        config=DebertaV2Config.from_pretrained(
            hyperparameters.model_name,
        ),  # type: ignore
    )
    model = DebertaV3LightningModelV1(
        hyperparameters=hyperparameters,
        tokenizer=tokenizer,  # type: ignore
        base_model=base_model,
    )

    wandb_logger = WandbLoggerV2(
        hyperparameters=hyperparameters,
    )

    checkpoint_callback = ModelCheckpoint(
        save_top_k=1,
        monitor="valid_loss",
        mode="min",
        filename=f"{hyperparameters.model_name}" + "-{epoch:02d}-{valid_loss:.2f}",
    )

    accelerator = "gpu"
    if args.debug_status == 1:
        accelerator = "cpu"

    # ckpt_path = ""  # noqa: E501

    trainer = Trainer(
        accelerator=accelerator,
        logger=wandb_logger.logger,
        callbacks=[checkpoint_callback],
        **lighting_hyperparameters,
    )

    trainer.fit(
        model,
        datamodule=data_module,
        # ckpt_path=ckpt_path,
    )


def experiment_2():
    """
    похоже на experiment_1, теперь количество положительных примеров
    равно количеству отрицательных примеров.
    """
    parser = ExperimentArgumentParserV1()
    args: TrainArgumentsV1 = parser.args

    max_epochs = 1
    if args.debug_status == 1:
        max_epochs = 1

    lighting_hyperparameters = LightingHyperparametersV1(
        precision=16,
        max_epochs=max_epochs,
    ).__dict__

    hyperparameters = DebertaV3HyperparametersV1(
        lighting_hyperparameters=lighting_hyperparameters,
        train_batch_size=16,
        valid_batch_size=16,
    )
    seed_everything(hyperparameters.seed)

    tokenizer = DebertaV2Tokenizer.from_pretrained(
        hyperparameters.model_name,
    )
    is_debug = args.debug_status

    data_module = DebertaV3FoCusLightningDataModuleV2(
        train_path_dataset="./datasets/FoCus/train_focus.json",
        valid_path_dataset="./datasets/FoCus/valid_focus.json",
        hyperparameters=hyperparameters,
        tokenizer=tokenizer,  # type: ignore
        debug_status=is_debug,
    )
    base_model = DebertaV3ForClassificationV1(
        config=DebertaV2Config.from_pretrained(
            hyperparameters.model_name,
        ),  # type: ignore
    )
    model = DebertaV3LightningModelV1(
        hyperparameters=hyperparameters,
        tokenizer=tokenizer,  # type: ignore
        base_model=base_model,
    )

    wandb_logger = WandbLoggerV2(
        hyperparameters=hyperparameters,
    )

    checkpoint_callback = ModelCheckpoint(
        save_top_k=1,
        monitor="valid_loss",
        mode="min",
        filename=f"{hyperparameters.model_name}" + "-{epoch:02d}-{valid_loss:.2f}",
    )

    accelerator = "gpu"
    if args.debug_status == 1:
        accelerator = "cpu"

    # ckpt_path = ""  # noqa: E501

    trainer = Trainer(
        accelerator=accelerator,
        logger=wandb_logger.logger,
        callbacks=[checkpoint_callback],
        **lighting_hyperparameters,
    )

    trainer.fit(
        model,
        datamodule=data_module,
        # ckpt_path=ckpt_path,
    )


def experiment_3():
    """
    похоже на experiment_1, теперь количество положительных примеров
    равно количеству отрицательных примеров.
    увеличил количество эпох
    """
    parser = ExperimentArgumentParserV1()
    args: TrainArgumentsV1 = parser.args
    is_debug = args.debug_status

    max_epochs = 3
    if args.debug_status == 1:
        max_epochs = 1

    lighting_hyperparameters = LightingHyperparametersV1(
        precision=16,
        max_epochs=max_epochs,
    ).__dict__

    hyperparameters = DebertaV3HyperparametersV1(
        lighting_hyperparameters=lighting_hyperparameters,
        train_batch_size=16,
        valid_batch_size=16,
    )
    seed_everything(hyperparameters.seed)

    tokenizer = DebertaV2Tokenizer.from_pretrained(
        hyperparameters.model_name,
    )

    data_module = DebertaV3FoCusLightningDataModuleV2(
        train_path_dataset="./datasets/FoCus/train_focus.json",
        valid_path_dataset="./datasets/FoCus/valid_focus.json",
        hyperparameters=hyperparameters,
        tokenizer=tokenizer,  # type: ignore
        debug_status=is_debug,
    )
    base_model = DebertaV3ForClassificationV1(
        config=DebertaV2Config.from_pretrained(
            hyperparameters.model_name,
        ),  # type: ignore
    )
    model = DebertaV3LightningModelV1(
        hyperparameters=hyperparameters,
        tokenizer=tokenizer,  # type: ignore
        base_model=base_model,
    )

    wandb_logger = WandbLoggerV2(
        hyperparameters=hyperparameters,
    )

    checkpoint_callback = ModelCheckpoint(
        save_top_k=1,
        monitor="valid_loss",
        mode="min",
        filename=f"{hyperparameters.model_name}" + "-{epoch:02d}-{valid_loss:.2f}",
    )

    accelerator = "gpu"
    if args.debug_status == 1:
        accelerator = "cpu"

    ckpt_path = "/home/dimweb/Desktop/deeppavlov/my_focus/focus_knowledge_classification/1is9z2lu/checkpoints/microsoft/deberta-v3-base-epoch=00-valid_loss=0.53.ckpt"  # noqa: E501

    trainer = Trainer(
        accelerator=accelerator,
        logger=wandb_logger.logger,
        callbacks=[checkpoint_callback],
        **lighting_hyperparameters,
    )

    trainer.fit(
        model,
        datamodule=data_module,
        ckpt_path=ckpt_path,
    )


def experiment_4():
    """
    похоже на experiment_3, количество положительных примеров
    равно количеству отрицательных примеров.
    добавил в текст используемые части персоны(если такие использовались)
    для генерации ответа
    """
    parser = ExperimentArgumentParserV1()
    args: TrainArgumentsV1 = parser.args
    is_debug = args.debug_status

    max_epochs = 2
    if args.debug_status == 1:
        max_epochs = 1

    lighting_hyperparameters = LightingHyperparametersV1(
        precision=16,
        max_epochs=max_epochs,
    ).__dict__

    hyperparameters = DebertaV3HyperparametersV1(
        lighting_hyperparameters=lighting_hyperparameters,
        train_batch_size=16,
        valid_batch_size=16,
    )
    seed_everything(hyperparameters.seed)

    tokenizer = DebertaV2Tokenizer.from_pretrained(
        hyperparameters.model_name,
    )

    data_module = DebertaV3FoCusLightningDataModuleV3(
        train_path_dataset="./datasets/FoCus/train_focus.json",
        valid_path_dataset="./datasets/FoCus/valid_focus.json",
        hyperparameters=hyperparameters,
        tokenizer=tokenizer,  # type: ignore
        debug_status=is_debug,
    )
    base_model = DebertaV3ForClassificationV1(
        config=DebertaV2Config.from_pretrained(
            hyperparameters.model_name,
        ),  # type: ignore
    )
    model = DebertaV3LightningModelV1(
        hyperparameters=hyperparameters,
        tokenizer=tokenizer,  # type: ignore
        base_model=base_model,
    )

    wandb_logger = WandbLoggerV2(
        hyperparameters=hyperparameters,
    )

    checkpoint_callback = ModelCheckpoint(
        save_top_k=1,
        monitor="valid_loss",
        mode="min",
        filename=f"{hyperparameters.model_name}" + "-{epoch:02d}-{valid_loss:.2f}",
    )

    accelerator = "gpu"
    if args.debug_status == 1:
        accelerator = "cpu"

    # ckpt_path = "/home/dimweb/Desktop/deeppavlov/my_focus/focus_knowledge_classification/1is9z2lu/checkpoints/microsoft/deberta-v3-base-epoch=00-valid_loss=0.53.ckpt"  # noqa: E501

    trainer = Trainer(
        accelerator=accelerator,
        logger=wandb_logger.logger,
        callbacks=[checkpoint_callback],
        **lighting_hyperparameters,
    )

    trainer.fit(
        model,
        datamodule=data_module,
        # ckpt_path=ckpt_path,
    )
