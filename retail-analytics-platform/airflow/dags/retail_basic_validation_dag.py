from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    "owner": "airflow",
    "retries": 0,
}

with DAG(
    dag_id="retail_basic_validation_pipeline",
    default_args=default_args,
    description="Basic validation DAG for Retail Analytics Platform",
    start_date=datetime(2026, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["retail", "validation", "hdfs", "spark", "hive"],
) as dag:

    check_airflow_environment = BashOperator(
        task_id="check_airflow_environment",
        bash_command="""
        echo "Airflow basic validation started"
        echo "Current user: $(whoami)"
        echo "Current directory: $(pwd)"
        echo "Validation DAG is working"
        """,
    )

    check_spark_submit = BashOperator(
        task_id="check_spark_submit",
        bash_command="""
        echo "Checking spark-submit inside Airflow container..."
        if [ -x /home/airflow/.local/bin/spark-submit ]; then
            echo "spark-submit found at /home/airflow/.local/bin/spark-submit"
            /home/airflow/.local/bin/spark-submit --version
        elif command -v spark-submit >/dev/null 2>&1; then
            echo "spark-submit found in PATH"
            spark-submit --version
        else
            echo "spark-submit not found"
            exit 1
        fi
        """,
    )

    check_spark_master_connection = BashOperator(
        task_id="check_spark_master_connection",
        bash_command="""
        echo "Checking Spark master network connection..."
        python - <<'EOF'
import socket

host = "retail-spark-master"
port = 7077

s = socket.socket()
s.settimeout(10)

try:
    s.connect((host, port))
    print(f"Connected to Spark master: {host}:{port}")
finally:
    s.close()
EOF
        """,
    )

    check_hdfs_namenode_connection = BashOperator(
        task_id="check_hdfs_namenode_connection",
        bash_command="""
        echo "Checking HDFS NameNode network connection..."
        python - <<'EOF'
import socket

host = "retail-namenode"
port = 9000

s = socket.socket()
s.settimeout(10)

try:
    s.connect((host, port))
    print(f"Connected to HDFS NameNode: {host}:{port}")
finally:
    s.close()
EOF
        """,
    )

    check_hive_reports_note = BashOperator(
        task_id="check_hive_reports_note",
        bash_command="""
        echo "Hive reports were already verified on host machine:"
        echo "output/hive_reports/hive_category_sales.tsv"
        echo "output/hive_reports/hive_monthly_sales.tsv"
        echo "output/hive_reports/hive_region_sales.tsv"
        echo "output/hive_reports/hive_segment_sales.tsv"
        echo "output/hive_reports/hive_state_sales.tsv"
        echo "output/hive_reports/hive_sub_category_sales.tsv"
        echo "output/hive_reports/hive_top_10_products.tsv"
        echo "Basic Airflow validation completed"
        """,
    )

    (
        check_airflow_environment
        >> check_spark_submit
        >> check_spark_master_connection
        >> check_hdfs_namenode_connection
        >> check_hive_reports_note
    )
