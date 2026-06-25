from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    "owner": "anmol",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}


with DAG(
    dag_id="retail_hdfs_spark_pipeline",
    default_args=default_args,
    description="Retail analytics pipeline using HDFS, Spark, and PySpark",
    start_date=datetime(2026, 6, 25),
    schedule=None,
    catchup=False,
    tags=["retail", "hdfs", "spark", "pyspark"],
) as dag:

    check_pyspark_file = BashOperator(
        task_id="check_pyspark_file",
        bash_command="ls -l /opt/airflow/spark/hdfs_retail_analysis.py",
    )

    run_spark_job = BashOperator(
        task_id="run_spark_job",
        bash_command="""
        spark-submit \
          --master spark://retail-spark-master:7077 \
          --conf spark.driver.bindAddress=0.0.0.0 \
          --conf spark.driver.host=retail-airflow-scheduler \
          /opt/airflow/spark/hdfs_retail_analysis.py
        """,
    )

    check_spark_submit = BashOperator(
        task_id="check_spark_submit",
        bash_command="""
        spark-submit \
          --master spark://retail-spark-master:7077 \
          --conf spark.driver.bindAddress=0.0.0.0 \
          --conf spark.driver.host=retail-airflow-scheduler \
          --version
        """,
    )

    check_pyspark_file >> run_spark_job >> check_spark_submit
