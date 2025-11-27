import pandas as pd
from typing import Optional
from mlops_core.data_access.snowflake_client import SnowflakeClient


class FeatureStoreClient:
    """
    Feature store backed by Snowflake.

    DS can specify fully qualified table names in their config:
        IOTDATABASE.FEATURES.FS_FRIDGE_FEATURES
    """

    def __init__(self):
        self.client = SnowflakeClient()

    def create_feature_table(self, fully_qualified_name: str, schema_definition: str) -> None:
        """
        Template for creating feature tables.

        Example:
          fully_qualified_name = "IOTDATABASE.FEATURES.FS_FRIDGE_FEATURES"
          schema_definition = "FRIDGE_ID STRING, FEATURE_1 FLOAT, TS TIMESTAMP"
        """
        # TODO: implement with CREATE TABLE
        raise NotImplementedError("create_feature_table is a template method.")

    def write_features(self, df: pd.DataFrame, fully_qualified_name: str) -> None:
        """
        Template for writing features.
        """
        # TODO: implement via client.write_df(...)
        raise NotImplementedError("write_features is a template method.")

    def read_features(self, fully_qualified_name: str, limit: Optional[int] = None) -> pd.DataFrame:
        query = f"SELECT * FROM {fully_qualified_name}"
        if limit is not None:
            query += f" LIMIT {limit}"
        return self.client.fetch_df(query)
