#!/bin/bash

set -e

echo "Starting Retail Analytics Big Data Pipeline..."

echo "Step 1: Starting Docker containers..."
docker compose -f docker/docker-compose.yml up -d

echo "Step 2: Checking running containers..."
docker ps

echo "Step 3: Uploading dataset to HDFS..."

if [ ! -f "data/train.csv" ]; then
  echo "ERROR: data/train.csv not found"
  echo "Please make sure your dataset is placed at data/train.csv"
  exit 1
fi

docker cp data/train.csv retail-namenode:/tmp/train.csv

docker exec retail-namenode hdfs dfs -mkdir -p /retail_analytics/input
docker exec retail-namenode hdfs dfs -put -f /tmp/train.csv /retail_analytics/input/train.csv

echo "Step 4: Verifying HDFS input..."
docker exec retail-namenode hdfs dfs -ls /retail_analytics/input

echo "Step 5: Copying PySpark job to Spark master..."
docker cp spark/hdfs_retail_analysis.py retail-spark-master:/opt/spark/work-dir/hdfs_retail_analysis.py

echo "Step 6: Running PySpark job..."
docker exec retail-spark-master /opt/spark/bin/spark-submit \
  --master spark://spark-master:7077 \
  /opt/spark/work-dir/hdfs_retail_analysis.py

echo "Step 7: Checking HDFS output..."
docker exec retail-namenode hdfs dfs -ls /retail_analytics/output

echo "Step 8: Exporting HDFS reports to local output/hdfs_reports..."
mkdir -p output/hdfs_reports

for folder in category_summary kpi_summary monthly_sales region_summary segment_summary ship_mode_summary state_summary sub_category_summary top_cities top_products
do
  docker exec retail-namenode sh -c "hdfs dfs -cat /retail_analytics/output/$folder/part-*.csv" > output/hdfs_reports/$folder.csv
done

echo "Step 9: Local reports created:"
ls output/hdfs_reports

echo "Pipeline completed successfully."
echo "Reports are available in: output/hdfs_reports"
