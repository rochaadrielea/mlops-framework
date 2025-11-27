import os
import pandas as pd
import snowflake.connector
from .base_client import BaseDBClient


class SnowflakeClient(BaseDBClient):
    """
    Snowflake client for the framework.

    Secrets from env (or GitHub Secrets):
      - SNOWFLAKE_ACCOUNT
      - SNOWFLAKE_USER
      - SNOWFLAKE_PASSWORD

    Framework defaults (hard-coded):
      - role: ACCOUNTADMIN
      - database: IOTDATABASE
      - warehouse: COMPUTE_WH
      - schema: FRAMEWORK_PROD
    """

    def __init__(self):
        self.role = "ACCOUNTADMIN"
        self.database = "IOTDATABASE"
        self.warehouse = "COMPUTE_WH"
        self.schema = "FRAMEWORK_PROD"

    def _conn(self):
        account = os.getenv("SNOWFLAKE_ACCOUNT")
        user = os.getenv("SNOWFLAKE_USER")
        password = os.getenv("SNOWFLAKE_PASSWORD")

        if not all([account, user, password]):
            raise RuntimeError(
                "Missing Snowflake env vars. Expected SNOWFLAKE_ACCOUNT, "
                "SNOWFLAKE_USER, SNOWFLAKE_PASSWORD."
            )

        return snowflake.connector.connect(
            account=account,
            user=user,
            password=password,
            role=self.role,
            warehouse=self.warehouse,
            database=self.database,
            schema=self.schema,
        )

    def fetch_df(self, query: str) -> pd.DataFrame:
        with self._conn() as conn:
            return pd.read_sql(query, conn)

    def write_df(self, df: pd.DataFrame, table_name: str, if_exists: str = "append") -> None:
        """
        Template only. Implementation depends on company policy (e.g. write_pandas).
        """
        raise NotImplementedError("write_df is a template method for this framework.")
