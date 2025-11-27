from typing import Callable, Dict, Any
import mlflow

from mlops_core.experiments.mlflow_utils import init_mlflow, set_experiment


def run_experiment(
    train_fn: Callable[[Dict[str, Any]], None],
    experiment_config: Dict[str, Any],
    mlflow_cfg_path: str,
) -> None:
    """
    Platform helper:

    - initializes MLflow from config/env
    - sets experiment
    - opens mlflow run
    - calls DS train(config)
    """

    init_mlflow(mlflow_cfg_path)
    experiment_name = set_experiment(mlflow_cfg_path)

    with mlflow.start_run(run_name=experiment_config.get("run_name")):
        mlflow.log_param("experiment_name", experiment_name)
        train_fn(experiment_config)
