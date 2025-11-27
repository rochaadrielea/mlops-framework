from datetime import datetime, timedelta
import os

from airflow import DAG
from airflow.operators.python import PythonOperator
import mlflow


def training_core(**context):
    """Pretend to train a model and return a metric."""
    accuracy = 0.93
    print(f"[TRAIN] Finished training with accuracy={accuracy}")
    return {"accuracy": accuracy}


def log_to_mlflow(**context):
    """Log training metrics to MLflow."""
    print("[DEBUG][TRAIN] Entered log_to_mlflow")

    ti = context["ti"]
    metrics = ti.xcom_pull(task_ids="training_core_task") or {}
    accuracy = float(metrics.get("accuracy", 0.0))

    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://host.docker.internal:5000")
    experiment_name = os.getenv("MLFLOW_EXPERIMENT", "framework_training_airflow_v2")

    print(f"[DEBUG][TRAIN] tracking_uri    = {tracking_uri}")
    print(f"[DEBUG][TRAIN] experiment_name = {experiment_name}")
    print(f"[DEBUG][TRAIN] accuracy        = {accuracy}")

    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)

    with mlflow.start_run(run_name="training_pipeline_debug"):
        mlflow.log_param("pipeline", "training_pipeline")
        mlflow.log_metric("train_accuracy", accuracy)

    print("[DEBUG][TRAIN] Logged metrics to MLflow")


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="mlops_framework_training",
    default_args=default_args,
    description="Training DAG that logs to MLflow.",
    schedule_interval="*/1 * * * *",  # or None / whatever you want
    start_date=datetime(2025, 11, 27),
    catchup=False,
    tags=["mlflow", "mlops_framework", "training"],
) as dag:

    training_core_task = PythonOperator(
        task_id="training_core_task",
        python_callable=training_core,
    )

    log_to_mlflow_task = PythonOperator(
        task_id="log_to_mlflow_task",
        python_callable=log_to_mlflow,
    )

    training_core_task >> log_to_mlflow_task
