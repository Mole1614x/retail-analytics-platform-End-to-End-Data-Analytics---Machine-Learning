# Retail Analytics Platform — End-to-End Data Analytics & Big Data Project

## Project Overview

This project is an end-to-end Retail Analytics Platform built using Python, SQL, PySpark, Hadoop HDFS, Hive, Docker, and Apache Airflow.

The project performs data cleaning, exploratory data analysis, SQL reporting, machine learning model training, big data processing using Spark, distributed storage using HDFS, Hive-based 
analytics, and Airflow-based pipeline validation.

It is designed as a resume-ready Big Data Analytics project demonstrating both local data analytics and distributed data processing concepts.

---

## Technology Stack

* Python
* Pandas
* Matplotlib
* SQLite
* SQL
* scikit-learn
* PySpark
* Apache Spark
* Hadoop HDFS
* Apache Hive
* Apache Airflow
* Docker
* Docker Compose
* Git and GitHub

---

## Project Workflow

```text
Retail Dataset
     |
     v
Python + Pandas Cleaning
     |
     v
EDA + Charts
     |
     v
SQLite Reports
     |
     v
Machine Learning Models
     |
     v
PySpark Processing
     |
     v
HDFS Storage
     |
     v
Hive SQL Reports
     |
     v
Airflow Validation DAG
```

---

## Folder Structure

```text
retail-analytics-platform/
├── airflow/
│   └── dags/
│       ├── retail_hdfs_spark_dag.py
│       └── retail_basic_validation_dag.py
├── data/
├── database/
├── docker/
├── output/
│   ├── charts/
│   ├── hdfs_reports/
│   ├── hive_reports/
│   ├── models/
│   ├── reports/
│   └── spark_reports/
├── scripts/
├── spark/
├── src/
├── main.py
├── requirements.txt
├── README.md
└── project_structure.txt
```

---

## Completed Modules

### 1. Data Cleaning with Python and Pandas

The dataset was cleaned using Python and Pandas.

Main tasks included:

* Loaded retail sales dataset
* Handled missing values
* Converted date columns
* Created new time-based columns
* Prepared cleaned data for analytics and reporting

---

### 2. Exploratory Data Analysis

EDA was performed using Pandas and Matplotlib.

Generated analysis included:

* Sales by category
* Sales by region
* Sales by segment
* Monthly sales trend
* Product-level analysis
* State and city-level analysis

Charts were saved inside:

```text
output/charts/
```

---

### 3. SQLite Reporting

Cleaned data was loaded into a SQLite database.

SQLite reports were generated for:

* Category sales
* Region sales
* Segment sales
* State sales
* Monthly sales
* Top products

Reports were saved inside:

```text
output/reports/
```

---

### 4. Machine Learning

Machine learning models were trained using scikit-learn.

Models included:

* Linear Regression
* Decision Tree
* Random Forest
* Logistic Regression
* KNN
* Naive Bayes
* SVC

Saved models are available inside:

```text
output/models/
```

---

### 5. PySpark Analytics

PySpark was used for big data style processing.

Generated Spark reports included:

* Category summary
* Region summary
* Segment summary
* Monthly sales
* State summary
* Sub-category summary
* Top products
* Top cities

Spark reports were saved inside:

```text
output/spark_reports/
```

---

### 6. Dockerized Hadoop and Spark

The big data environment was created using Docker and Docker Compose.

Running services included:

* Hadoop NameNode
* Hadoop DataNode
* Spark Master
* Spark Worker
* Airflow Webserver
* Airflow Scheduler
* Airflow Postgres

Main containers used:

```text
retail-namenode
retail-datanode
retail-spark-master
retail-spark-worker
retail-airflow-webserver
retail-airflow-scheduler
retail-airflow-postgres
```

---

### 7. HDFS Storage

Dataset and output reports were stored in HDFS.

Important HDFS paths:

```text
/retail_analytics/input
/retail_analytics/output
```

HDFS output folders included:

```text
category_summary
kpi_summary
monthly_sales
region_summary
segment_summary
ship_mode_summary
state_summary
sub_category_summary
top_cities
top_products
```

---

### 8. Hive Analytics

Hive was used for SQL-style big data analytics.

Hive reports were generated and stored inside:

```text
output/hive_reports/
```

Hive reports include:

```text
hive_category_sales.tsv
hive_monthly_sales.tsv
hive_region_sales.tsv
hive_segment_sales.tsv
hive_state_sales.tsv
hive_sub_category_sales.tsv
hive_top_10_products.tsv
```

---

### 9. Apache Airflow

Apache Airflow was used for pipeline validation and orchestration checks.

A basic Airflow DAG was created:

```text
retail_basic_validation_pipeline
```

The DAG successfully validated:

* Airflow environment
* Spark submit availability
* Spark master connectivity
* HDFS NameNode connectivity
* Hive report completion status

Final Airflow DAG status:

```text
retail_basic_validation_pipeline | success
```

The advanced Spark execution DAG was paused after testing:

```text
retail_hdfs_spark_pipeline
```

---

## Docker Commands

Start Hadoop, Spark, and Airflow services:

```bash
docker compose -f docker-compose.yml -f docker-compose.airflow.yml up -d --build
```

Check running containers:

```bash
docker ps
```

Stop containers:

```bash
docker compose -f docker-compose.yml -f docker-compose.airflow.yml down
```

---

## HDFS Commands

Check HDFS root:

```bash
docker exec -it retail-namenode hdfs dfs -ls /
```

Check retail analytics folder:

```bash
docker exec -it retail-namenode hdfs dfs -ls /retail_analytics
```

Check HDFS output reports:

```bash
docker exec -it retail-namenode hdfs dfs -ls /retail_analytics/output
```

---

## Airflow Commands

List DAGs:

```bash
docker exec -it retail-airflow-webserver airflow dags list
```

Trigger basic validation DAG:

```bash
docker exec -it retail-airflow-webserver airflow dags trigger retail_basic_validation_pipeline
```

Check DAG run status:

```bash
docker exec -it retail-airflow-webserver airflow dags list-runs -d retail_basic_validation_pipeline
```

Open Airflow UI:

```text
http://localhost:8085
```

---

## Final Outputs

Final reports are available in:

```text
output/reports/
output/spark_reports/
output/hdfs_reports/
output/hive_reports/
```

Final Hive reports:

```text
output/hive_reports/hive_category_sales.tsv
output/hive_reports/hive_monthly_sales.tsv
output/hive_reports/hive_region_sales.tsv
output/hive_reports/hive_segment_sales.tsv
output/hive_reports/hive_state_sales.tsv
output/hive_reports/hive_sub_category_sales.tsv
output/hive_reports/hive_top_10_products.tsv
```

---

## Resume Points

* Built an end-to-end Retail Analytics Platform using Python, SQL, PySpark, Hive, HDFS, Docker, and Airflow.
* Designed data cleaning, EDA, reporting, and machine learning workflows using Pandas, SQLite, Matplotlib, and scikit-learn.
* Implemented big data processing using PySpark and stored distributed outputs in Hadoop HDFS.
* Created Hive-based analytical reports for category, region, state, segment, monthly sales, and top products.
* Containerized Hadoop, Spark, and Airflow services using Docker Compose.
* Created and executed an Airflow validation DAG to verify pipeline components and service connectivity.

---

## Project Status

```text
Python + Pandas        Completed
EDA + Charts           Completed
SQLite Reports         Completed
Machine Learning       Completed
PySpark Reports        Completed
Docker Setup           Completed
Hadoop HDFS            Completed
Spark                  Completed
Hive Reports           Completed
Airflow Validation     Completed
GitHub Documentation   Completed
```

---

## Author

**Anmol Gangwar**

GitHub: [Mole1614x](https://github.com/Mole1614x)
LinkedIn: [anmolgangwar](https://www.linkedin.com/in/anmolgangwar/)

