# scripts/framework_smoke_test.py

"""
Smoke test for the MLOps framework:
- Connects to Snowflake using env vars
- Runs a tiny query
- Logs a metric + params to MLflow
"""

from mlops_core.data_access.snowflake_client import SnowflakeClient
from mlops_core.experiments.mlflow_utils import init_mlflow, set_experiment
import mlflow


def main() -> None:
    # 1) Init MLflow (default http://localhost:5000)
    init_mlflow()
    experiment_name = set_experiment("framework_connectivity_test")

    client = SnowflakeClient()

    # 2) Simple query just to prove connectivity
    df = client.fetch_df("SELECT CURRENT_DATABASE() AS DB, CURRENT_SCHEMA() AS SCHEMA")

    current_db = df["DB"].iloc[0]
    current_schema = df["SCHEMA"].iloc[0]

    with mlflow.start_run(run_name="framework_smoke_test"):
        # Log which DB/schema we actually connected to
        mlflow.log_param("snowflake_database", current_db)
        mlflow.log_param("snowflake_schema", current_schema)

        # Dummy metric just to see something numeric
        mlflow.log_metric("connectivity_ok", 1.0)


if __name__ == "__main__":
    main()
