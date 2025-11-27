import os
import mlflow


def init_mlflow() -> None:
    """
    Initialize MLflow tracking.

    Default: http://localhost:5000
    Optional override with MLFLOW_TRACKING_URI env var.
    """
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
    mlflow.set_tracking_uri(tracking_uri)


def set_experiment(experiment_name: str = "framework_connectivity_test") -> str:
    """
    Set experiment name, with optional override via env var MLFLOW_EXPERIMENT.
    """
    exp = os.getenv("MLFLOW_EXPERIMENT", experiment_name)
    mlflow.set_experiment(exp)
    return exp
