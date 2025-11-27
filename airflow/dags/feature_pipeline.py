from datetime import datetime, timedelta
import os

from airflow import DAG
from airflow.operators.python import PythonOperator
import mlflow


def compute_features(**context):
    rows_processed = 200
    print(f"[FEATURES] Processed {rows_processed} rows (placeholder).")
    return {"rows_processed": rows_processed}


def log_to_mlflow(**context):
    """Log feature metrics to MLflow."""
    print("[DEBUG][FEATURE] Entered log_to_mlflow")

    ti = context["ti"]
    metrics = ti.xcom_pull(task_ids="compute_features_task") or {}
    rows_processed = float(metrics.get("rows_processed", 0.0))

    # ✅ Use the MLflow container name as default
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://felfel-mlflow:5000")
    experiment_name = os.getenv("MLFLOW_EXPERIMENT", "framework_training_airflow_v2")

    print(f"[DEBUG][FEATURE] tracking_uri    = {tracking_uri}")
    print(f"[DEBUG][FEATURE] experiment_name = {experiment_name}")
    print(f"[DEBUG][FEATURE] rows_processed  = {rows_processed}")

    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)

    with mlflow.start_run(run_name="feature_pipeline_debug"):
        mlflow.log_param("pipeline", "feature_pipeline")
        mlflow.log_metric("rows_processed", rows_processed)

    print("[DEBUG][FEATURE] Logged metrics to MLflow") 


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="mlops_feature_pipeline",
    default_args=default_args,
    description="Feature generation DAG that logs to MLflow.",
    schedule_interval="*/5 * * * *",
    start_date=datetime(2025, 11, 27),
    catchup=False,
    tags=["mlops_framework", "features", "mlflow"],
) as dag:

    compute_features_task = PythonOperator(
        task_id="compute_features_task",
        python_callable=compute_features,
    )

    log_to_mlflow_task = PythonOperator(
        task_id="log_to_mlflow_task",
        python_callable=log_to_mlflow,
    )

    compute_features_task >> log_to_mlflow_task
