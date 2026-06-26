from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="retail_hdfs_spark_pipeline",
    description="Run Retail PySpark HDFS analysis using Docker Spark and Hadoop containers",
    start_date=datetime(2026, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["retail", "spark", "hdfs", "docker"],
) as dag:

    check_docker_containers = BashOperator(
        task_id="check_docker_containers",
        bash_command="""
        docker ps | grep -q retail-namenode &&
        docker ps | grep -q retail-spark-master
        """,
    )

    check_hdfs_input = BashOperator(
        task_id="check_hdfs_input",
        bash_command="""
        docker exec retail-namenode hdfs dfs -test -f /retail_analytics/input/train.csv
        """,
    )

    copy_spark_script = BashOperator(
        task_id="copy_spark_script",
        bash_command="""
        docker cp /project/spark/hdfs_retail_analysis.py retail-spark-master:/tmp/hdfs_retail_analysis.py
        """,
    )

    run_spark_job = BashOperator(
        task_id="run_spark_job",
        bash_command="""
        docker exec retail-spark-master /opt/spark/bin/spark-submit \
        --master spark://retail-spark-master:7077 \
        /tmp/hdfs_retail_analysis.py
        """,
    )

    verify_hdfs_output = BashOperator(
        task_id="verify_hdfs_output",
        bash_command="""
        docker exec retail-namenode hdfs dfs -ls /retail_analytics/output
        """,
    )

    check_docker_containers >> check_hdfs_input >> copy_spark_script >> run_spark_job >> verify_hdfs_output
