# Retail Analytics Platform — Big Data Pipeline

An end-to-end retail analytics project using **Docker, HDFS, Apache Spark, PySpark, Python, SQLite, and Pandas**.
The project processes retail sales data, stores it in HDFS, runs distributed analytics using Spark, and generates business-ready CSV reports.

## Project Objective

The objective of this project is to build a scalable retail analytics pipeline that can:

* Store raw retail sales data in HDFS
* Process large-scale data using PySpark
* Generate KPI and business summary reports
* Export final analytics reports locally
* Run the complete pipeline using a shell script
* Later orchestrate the pipeline using Apache Airflow

## Tech Stack

* Python
* Pandas
* SQLite
* PySpark
* Apache Spark
* Hadoop HDFS
* Docker
* Shell Scripting
* Apache Airflow — planned as final orchestration layer

## Project Architecture

```text
Local Dataset
    ↓
Docker Containers
    ↓
HDFS NameNode + DataNode
    ↓
Apache Spark Master + Worker
    ↓
PySpark Analytics Job
    ↓
Reports stored in HDFS
    ↓
Reports exported to local output folder
```

## Docker Services

The project runs the following services using Docker Compose:

```text
retail-namenode
retail-datanode
retail-spark-master
retail-spark-worker
```

Service UIs:

```text
NameNode UI: http://localhost:9871
DataNode UI: http://localhost:9864
Spark Master UI: http://localhost:8080
Spark Worker UI: http://localhost:8081
```

## Project Structure

```text
retail-analytics-platform/
│
├── data/
│   └── train.csv
│
├── docker/
│   └── docker-compose.yml
│
├── spark/
│   └── hdfs_retail_analysis.py
│
├── scripts/
│   └── run_pipeline.sh
│
├── output/
│   └── hdfs_reports/
│
├── src/
├── database/
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Generated Reports

The PySpark pipeline generates the following reports:

```text
category_summary.csv
kpi_summary.csv
monthly_sales.csv
region_summary.csv
segment_summary.csv
ship_mode_summary.csv
state_summary.csv
sub_category_summary.csv
top_cities.csv
top_products.csv
```

## Business Reports Created

The project generates insights for:

* Total sales
* Total orders
* Average sales
* Sales by category
* Sales by region
* Sales by customer segment
* Sales by state
* Sales by city
* Sales by ship mode
* Monthly sales trend
* Top-selling products
* Sub-category performance

## How to Run the Project

### 1. Start Docker Pipeline

From the project root:

```bash
./scripts/run_pipeline.sh
```

This command will:

```text
Start Docker containers
Upload dataset to HDFS
Run PySpark job on Spark cluster
Generate reports in HDFS
Export reports to local output folder
```

### 2. Check Docker Containers

```bash
docker ps
```

Expected containers:

```text
retail-namenode
retail-datanode
retail-spark-master
retail-spark-worker
```

### 3. Check HDFS Input

```bash
docker exec -it retail-namenode hdfs dfs -ls /retail_analytics/input
```

### 4. Check HDFS Output

```bash
docker exec -it retail-namenode hdfs dfs -ls /retail_analytics/output
```

### 5. Check Local Reports

```bash
ls output/hdfs_reports
```

### 6. View KPI Report

```bash
cat output/hdfs_reports/kpi_summary.csv
```

## Manual Spark Submit Command

The PySpark job can also be run manually:

```bash
docker cp spark/hdfs_retail_analysis.py retail-spark-master:/opt/spark/work-dir/hdfs_retail_analysis.py

docker exec -it retail-spark-master /opt/spark/bin/spark-submit \
  --master spark://spark-master:7077 \
  /opt/spark/work-dir/hdfs_retail_analysis.py
```

## Key Features

* End-to-end big data pipeline
* HDFS-based distributed storage
* Spark-based distributed processing
* Dockerized environment
* Automated shell pipeline
* Local CSV report export
* GitHub-ready project structure
* Airflow orchestration planned as final step

## Current Status

Completed:

```text
Docker setup
HDFS setup
Spark setup
Dataset upload to HDFS
PySpark analytics job
HDFS report generation
Local report export
One-command pipeline script
```

Pending:

```text
Apache Airflow DAG orchestration
Final Airflow pipeline test
```

## Resume Description

Built an end-to-end retail analytics big data pipeline using Docker, HDFS, Apache Spark, and PySpark. The project ingests retail sales data into HDFS, processes it using Spark, generates business 
KPI reports, and exports final analytics outputs for dashboarding and reporting.

## Author

Anmol Gangwar

