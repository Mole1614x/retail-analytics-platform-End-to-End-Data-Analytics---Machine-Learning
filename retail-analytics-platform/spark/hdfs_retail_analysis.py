from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, sum as spark_sum, avg, count, round,
    to_date, year, month, date_format, coalesce, desc
)

spark = SparkSession.builder \
    .appName("Retail HDFS PySpark Analysis") \
    .getOrCreate()

input_path = "hdfs://namenode:9000/retail_analytics/input/train.csv"
output_base = "hdfs://namenode:9000/retail_analytics/output"

print("Reading data from HDFS...")

df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv(input_path)

print("Schema:")
df.printSchema()

print("Sample data:")
df.show(5, truncate=False)

# Convert Sales column to double
df = df.withColumn("Sales", col("Sales").cast("double"))

# Clean Order Date
if "Order Date" in df.columns:
    df = df.withColumn(
        "Order_Date_Clean",
        coalesce(
            to_date(col("Order Date"), "dd/MM/yyyy"),
            to_date(col("Order Date"), "M/d/yyyy"),
            to_date(col("Order Date"), "MM/dd/yyyy"),
            to_date(col("Order Date"), "dd-MM-yyyy"),
            to_date(col("Order Date"), "yyyy-MM-dd")
        )
    )

    df = df.withColumn("Year", year(col("Order_Date_Clean")))
    df = df.withColumn("Month", month(col("Order_Date_Clean")))
    df = df.withColumn("Month_Name", date_format(col("Order_Date_Clean"), "MMMM"))

# 1. KPI Summary
kpi_summary = df.agg(
    round(spark_sum("Sales"), 2).alias("Total_Sales"),
    count("*").alias("Total_Orders"),
    round(avg("Sales"), 2).alias("Average_Sales")
)

kpi_summary.write.mode("overwrite").option("header", True).csv(f"{output_base}/kpi_summary")

# 2. Category Summary
if "Category" in df.columns:
    category_summary = df.groupBy("Category").agg(
        round(spark_sum("Sales"), 2).alias("Total_Sales"),
        count("*").alias("Orders")
    ).orderBy(desc("Total_Sales"))

    category_summary.write.mode("overwrite").option("header", True).csv(f"{output_base}/category_summary")

# 3. Region Summary
if "Region" in df.columns:
    region_summary = df.groupBy("Region").agg(
        round(spark_sum("Sales"), 2).alias("Total_Sales"),
        count("*").alias("Orders")
    ).orderBy(desc("Total_Sales"))

    region_summary.write.mode("overwrite").option("header", True).csv(f"{output_base}/region_summary")

# 4. Segment Summary
if "Segment" in df.columns:
    segment_summary = df.groupBy("Segment").agg(
        round(spark_sum("Sales"), 2).alias("Total_Sales"),
        count("*").alias("Orders")
    ).orderBy(desc("Total_Sales"))

    segment_summary.write.mode("overwrite").option("header", True).csv(f"{output_base}/segment_summary")

# 5. Sub-Category Summary
if "Sub-Category" in df.columns:
    sub_category_summary = df.groupBy("Sub-Category").agg(
        round(spark_sum("Sales"), 2).alias("Total_Sales"),
        count("*").alias("Orders")
    ).orderBy(desc("Total_Sales"))

    sub_category_summary.write.mode("overwrite").option("header", True).csv(f"{output_base}/sub_category_summary")

# 6. State Summary
if "State" in df.columns:
    state_summary = df.groupBy("State").agg(
        round(spark_sum("Sales"), 2).alias("Total_Sales"),
        count("*").alias("Orders")
    ).orderBy(desc("Total_Sales"))

    state_summary.write.mode("overwrite").option("header", True).csv(f"{output_base}/state_summary")

# 7. City Summary
if "City" in df.columns:
    city_summary = df.groupBy("City").agg(
        round(spark_sum("Sales"), 2).alias("Total_Sales"),
        count("*").alias("Orders")
    ).orderBy(desc("Total_Sales")).limit(20)

    city_summary.write.mode("overwrite").option("header", True).csv(f"{output_base}/top_cities")

# 8. Ship Mode Summary
if "Ship Mode" in df.columns:
    ship_mode_summary = df.groupBy("Ship Mode").agg(
        round(spark_sum("Sales"), 2).alias("Total_Sales"),
        count("*").alias("Orders")
    ).orderBy(desc("Total_Sales"))

    ship_mode_summary.write.mode("overwrite").option("header", True).csv(f"{output_base}/ship_mode_summary")

# 9. Monthly Sales
if "Order_Date_Clean" in df.columns:
    monthly_sales = df.groupBy("Year", "Month", "Month_Name").agg(
        round(spark_sum("Sales"), 2).alias("Total_Sales"),
        count("*").alias("Orders")
    ).orderBy("Year", "Month")

    monthly_sales.write.mode("overwrite").option("header", True).csv(f"{output_base}/monthly_sales")

# 10. Top Products
if "Product Name" in df.columns:
    top_products = df.groupBy("Product Name").agg(
        round(spark_sum("Sales"), 2).alias("Total_Sales"),
        count("*").alias("Orders")
    ).orderBy(desc("Total_Sales")).limit(10)

    top_products.write.mode("overwrite").option("header", True).csv(f"{output_base}/top_products")

print("PySpark analysis completed successfully.")
print(f"Reports saved to: {output_base}")

spark.stop()
