from datetime import datetime, timedelta
import os

from airflow import DAG
from airflow.operators.python import PythonOperator
import mlflow


def compute_monitoring_metrics(**context):
    """Fake monitoring metrics for demo."""
    metrics = {
        "latency_ms": 120,
        "error_rate": 0.01,
    }
    print(f"[MONITOR] Metrics: {metrics}")
    return metrics


def log_to_mlflow(**context):
    """Log monitoring metrics to MLflow."""
    print("[DEBUG][MONITOR] Entered log_to_mlflow")

    ti = context["ti"]
    metrics = ti.xcom_pull(task_ids="compute_monitoring_metrics") or {}
    latency_ms = float(metrics.get("latency_ms", 0.0))
    error_rate = float(metrics.get("error_rate", 0.0))

    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://host.docker.internal:5000")
    experiment_name = os.getenv("MLFLOW_EXPERIMENT", "framework_training_airflow_v2")

    print(f"[DEBUG][MONITOR] tracking_uri    = {tracking_uri}")
    print(f"[DEBUG][MONITOR] experiment_name = {experiment_name}")
    print(f"[DEBUG][MONITOR] latency_ms      = {latency_ms}")
    print(f"[DEBUG][MONITOR] error_rate      = {error_rate}")

    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)

    with mlflow.start_run(run_name="monitoring_pipeline_debug"):
        mlflow.log_param("pipeline", "monitoring_pipeline")
        mlflow.log_metric("latency_ms", latency_ms)
        mlflow.log_metric("error_rate", error_rate)

    print("[DEBUG][MONITOR] Logged monitoring metrics to MLflow")


def trigger_alerts(**context):
    ti = context["ti"]
    metrics = ti.xcom_pull(task_ids="compute_monitoring_metrics") or {}
    error_rate = float(metrics.get("error_rate", 0.0))

    if error_rate > 0.05:
        print(f"[ALERT] High error rate detected: {error_rate}")
    else:
        print(f"[ALERT] All good, error_rate={error_rate}")


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="mlops_monitoring_pipeline",
    default_args=default_args,
    description="Monitoring DAG that logs metrics to MLflow and can trigger alerts.",
    schedule_interval="*/10 * * * *",
    start_date=datetime(2025, 11, 27),
    catchup=False,
    tags=["mlops_framework", "mlops", "monitoring"],
) as dag:

    compute_monitoring_metrics_task = PythonOperator(
        task_id="compute_monitoring_metrics",
        python_callable=compute_monitoring_metrics,
    )

    log_to_mlflow_task = PythonOperator(
        task_id="log_to_mlflow",
        python_callable=log_to_mlflow,
    )

    trigger_alerts_task = PythonOperator(
        task_id="trigger_alerts",
        python_callable=trigger_alerts,
    )

    compute_monitoring_metrics_task >> log_to_mlflow_task >> trigger_alerts_task
