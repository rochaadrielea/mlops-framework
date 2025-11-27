import pandas as pd
from typing import Dict

from mlops_core.utils.config_loader import load_yaml
from mlops_core.data_access.snowflake_client import SnowflakeClient
from mlops_core.data_access.postgres_client import PostgresClient


def _build_clients() -> Dict[str, object]:
    return {
        "snowflake": SnowflakeClient(),
        "postgres": PostgresClient(),
    }


def load_dataset(dataset_name: str, datasets_cfg_path: str) -> pd.DataFrame:
    """
    Data scientist calls:

        df = load_dataset("iot_events", "config/datasets/datasets.example.yaml")

    The framework handles:
      - mapping logical name → DB/table
      - connecting via Snowflake/Postgres client
    """
    cfg = load_yaml(datasets_cfg_path)
    ds_meta = cfg["datasets"][dataset_name]

    clients = _build_clients()
    client = clients[ds_meta["connection"]]

    if ds_meta["connection"] == "snowflake":
        query = (
            f"SELECT * FROM "
            f"{ds_meta['database']}.{ds_meta['schema']}.{ds_meta['table']}"
        )
    elif ds_meta["connection"] == "postgres":
        query = f"SELECT * FROM {ds_meta['schema']}.{ds_meta['table']}"
    else:
        raise ValueError(f"Unsupported connection type: {ds_meta['connection']}")

    return client.fetch_df(query)
