from typing import Dict, Any

import mlflow
# import pandas as pd  # when needed

from mlops_core.data_access.dataset_loader import load_dataset
from mlops_core.feature_store.feature_store_client import FeatureStoreClient


def train(config: Dict[str, Any]) -> None:
    """
    This is where the Data Scientist writes their ML logic.

    Typical steps (you put comments / TODOs, not full code):
    1) df_raw = load_dataset(config["data"]["input_dataset"],
                             config["data"]["datasets_config"])
    2) df_features = ...  # cleaning + feature engineering
    3) fs = FeatureStoreClient()
       fs.write_features(df_features, config["data"]["feature_store_table"])
    4) model = ...  # train model
    5) mlflow.log_params(config["params"])
       mlflow.log_metric("some_metric", value)
       mlflow.<framework>.log_model(model, "model")

    The framework takes care of:
    - DB connections (Snowflake/Postgres)
    - MLflow initialization (URI + experiment)
    You only focus on ML code.
    """
    raise NotImplementedError("Implement your training logic here.")
