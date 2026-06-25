import os
import pandas as pd
import matplotlib.pyplot as plt


def basic_eda(df):
    print("\n========== BASIC EDA ==========")

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nDataset shape:")
    print(df.shape)

    print("\nDataset info:")
    print(df.info())

    print("\nStatistical summary:")
    print(df.describe())

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nCategory count:")
    print(df["Category"].value_counts())

    print("\nRegion count:")
    print(df["Region"].value_counts())


def save_summary_reports(df):
    print("\n========== SAVING SUMMARY REPORTS ==========")

    os.makedirs("output/reports", exist_ok=True)

    category_sales = df.groupby("Category")["Sales"].sum().reset_index()
    category_sales.to_csv("output/reports/category_sales.csv", index=False)

    region_sales = df.groupby("Region")["Sales"].sum().reset_index()
    region_sales.to_csv("output/reports/region_sales.csv", index=False)

    segment_sales = df.groupby("Segment")["Sales"].sum().reset_index()
    segment_sales.to_csv("output/reports/segment_sales.csv", index=False)

    state_sales = df.groupby("State")["Sales"].sum().reset_index()
    state_sales.to_csv("output/reports/state_sales.csv", index=False)

    subcategory_sales = df.groupby("Sub-Category")["Sales"].sum().reset_index()
    subcategory_sales.to_csv("output/reports/subcategory_sales.csv", index=False)

    monthly_sales = df.groupby("Year_Month")["Sales"].sum().reset_index()
    monthly_sales.to_csv("output/reports/monthly_sales.csv", index=False)

    print("Summary reports saved successfully.")


def create_charts(df):
    print("\n========== CREATING CHARTS ==========")

    os.makedirs("output/charts", exist_ok=True)

    category_sales = df.groupby("Category")["Sales"].sum().sort_values()

    plt.figure(figsize=(8, 5))
    category_sales.plot(kind="bar")
    plt.title("Sales by Category")
    plt.xlabel("Category")
    plt.ylabel("Sales")
    plt.tight_layout()
    plt.savefig("output/charts/category_sales.png")
    plt.close()

    region_sales = df.groupby("Region")["Sales"].sum().sort_values()

    plt.figure(figsize=(8, 5))
    region_sales.plot(kind="bar")
    plt.title("Sales by Region")
    plt.xlabel("Region")
    plt.ylabel("Sales")
    plt.tight_layout()
    plt.savefig("output/charts/region_sales.png")
    plt.close()

    monthly_sales = df.groupby("Year_Month")["Sales"].sum()

    plt.figure(figsize=(12, 5))
    monthly_sales.plot(kind="line")
    plt.title("Monthly Sales Trend")
    plt.xlabel("Month")
    plt.ylabel("Sales")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("output/charts/monthly_sales_trend.png")
    plt.close()

    plt.figure(figsize=(8, 5))
    df["Sales"].plot(kind="hist", bins=30)
    plt.title("Sales Distribution")
    plt.xlabel("Sales")
    plt.tight_layout()
    plt.savefig("output/charts/sales_distribution.png")
    plt.close()

    print("Charts created successfully.")