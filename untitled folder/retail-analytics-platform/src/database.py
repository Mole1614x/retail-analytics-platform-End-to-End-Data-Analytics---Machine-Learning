import os
import sqlite3
import pandas as pd


DB_PATH = "database/retail.db"
TABLE_NAME = "retail_sales"


def clean_column_names(df):
    """
    Convert column names into SQL-friendly format.
    Example:
    Order Date -> order_date
    Customer Name -> customer_name
    Sub-Category -> sub_category
    """

    df = df.copy()

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    return df


def create_connection(db_path=DB_PATH):
    """
    Create SQLite database connection.
    """

    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    return conn


def save_to_sqlite(df, db_path=DB_PATH, table_name=TABLE_NAME):
    """
    Save cleaned dataframe into SQLite database.
    """

    print("\nSaving cleaned data into SQLite database...")

    df_db = clean_column_names(df)

    conn = create_connection(db_path)

    df_db.to_sql(
        table_name,
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    print("Data saved successfully in:", db_path)
    print("Table name:", table_name)

    return df_db


def run_query(query, db_path=DB_PATH):
    """
    Run SQL query and return result as dataframe.
    """

    conn = create_connection(db_path)
    result = pd.read_sql_query(query, conn)
    conn.close()

    return result


def get_table_columns(table_name=TABLE_NAME, db_path=DB_PATH):
    """
    Get column names from SQLite table.
    """

    conn = create_connection(db_path)

    query = "PRAGMA table_info({})".format(table_name)
    columns_df = pd.read_sql_query(query, conn)

    conn.close()

    return columns_df["name"].tolist()


def save_report(df, report_name):
    """
    Save SQL report into output/reports folder.
    """

    os.makedirs("output/reports", exist_ok=True)

    file_path = "output/reports/sql_{}.csv".format(report_name)
    df.to_csv(file_path, index=False)

    print("SQL report saved:", file_path)


def generate_sql_reports():
    """
    Generate business reports using SQL queries.
    """

    print("\nGenerating SQL reports...")

    columns = get_table_columns()

    # 1. Category-wise sales and profit
    if "category" in columns and "sales" in columns and "profit" in columns:
        query = """
        SELECT 
            category,
            ROUND(SUM(sales), 2) AS total_sales,
            ROUND(SUM(profit), 2) AS total_profit
        FROM retail_sales
        GROUP BY category
        ORDER BY total_sales DESC
        """

        category_report = run_query(query)
        print("\nCategory-wise Sales Report:")
        print(category_report)
        save_report(category_report, "category_sales")

    elif "category" in columns and "sales" in columns:
        query = """
        SELECT 
            category,
            ROUND(SUM(sales), 2) AS total_sales
        FROM retail_sales
        GROUP BY category
        ORDER BY total_sales DESC
        """

        category_report = run_query(query)
        print("\nCategory-wise Sales Report:")
        print(category_report)
        save_report(category_report, "category_sales")

    # 2. Region-wise profit
    if "region" in columns and "profit" in columns:
        query = """
        SELECT 
            region,
            ROUND(SUM(profit), 2) AS total_profit
        FROM retail_sales
        GROUP BY region
        ORDER BY total_profit DESC
        """

        region_report = run_query(query)
        print("\nRegion-wise Profit Report:")
        print(region_report)
        save_report(region_report, "region_profit")

    # 3. Monthly sales trend
    if "order_date" in columns and "sales" in columns:
        query = """
        SELECT 
            STRFTIME('%Y-%m', order_date) AS order_month,
            ROUND(SUM(sales), 2) AS monthly_sales
        FROM retail_sales
        GROUP BY order_month
        ORDER BY order_month
        """

        monthly_report = run_query(query)
        print("\nMonthly Sales Trend:")
        print(monthly_report.head())
        save_report(monthly_report, "monthly_sales_trend")

    # 4. Top 10 products by sales
    if "product_name" in columns and "sales" in columns:
        query = """
        SELECT 
            product_name,
            ROUND(SUM(sales), 2) AS total_sales
        FROM retail_sales
        GROUP BY product_name
        ORDER BY total_sales DESC
        LIMIT 10
        """

        product_report = run_query(query)
        print("\nTop 10 Products by Sales:")
        print(product_report)
        save_report(product_report, "top_10_products")

    # 5. State-wise sales
    if "state" in columns and "sales" in columns:
        query = """
        SELECT 
            state,
            ROUND(SUM(sales), 2) AS total_sales
        FROM retail_sales
        GROUP BY state
        ORDER BY total_sales DESC
        """

        state_report = run_query(query)
        print("\nState-wise Sales Report:")
        print(state_report.head())
        save_report(state_report, "state_sales")

    # 6. Segment-wise sales
    if "segment" in columns and "sales" in columns:
        query = """
        SELECT 
            segment,
            ROUND(SUM(sales), 2) AS total_sales
        FROM retail_sales
        GROUP BY segment
        ORDER BY total_sales DESC
        """

        segment_report = run_query(query)
        print("\nSegment-wise Sales Report:")
        print(segment_report)
        save_report(segment_report, "segment_sales")

    print("\nAll SQL reports generated successfully.")