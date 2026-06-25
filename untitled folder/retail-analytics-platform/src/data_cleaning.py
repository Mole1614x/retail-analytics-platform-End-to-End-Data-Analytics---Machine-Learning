import os
import pandas as pd


def load_data(file_path):
    df = pd.read_csv(file_path)

    # Remove extra spaces from column names
    df.columns = df.columns.str.strip()

    print("Data loaded successfully")
    print("Dataset Shape:", df.shape)
    print("Columns:", df.columns.tolist())

    return df


def clean_data(df):
    print("\nStarting data cleaning...")

    required_columns = [
        "Order Date",
        "Ship Date",
        "Ship Mode",
        "Segment",
        "City",
        "State",
        "Region",
        "Category",
        "Sub-Category",
        "Sales"
    ]

    missing_columns = []

    for col in required_columns:
        if col not in df.columns:
            missing_columns.append(col)

    if len(missing_columns) > 0:
        print("\nMissing columns:", missing_columns)
        print("Available columns:", df.columns.tolist())
        raise ValueError("Dataset does not match required Superstore format.")

    duplicate_count = df.duplicated().sum()
    print("Duplicate rows found:", duplicate_count)
    df = df.drop_duplicates()

    df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True, errors="coerce")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True, errors="coerce")

    df = df.dropna(subset=["Order Date", "Ship Date", "Sales"])

    df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
    df = df.dropna(subset=["Sales"])

    if "Postal Code" in df.columns:
        df["Postal Code"] = df["Postal Code"].fillna(0)

    df["Ship_Days"] = (df["Ship Date"] - df["Order Date"]).dt.days
    df = df[df["Ship_Days"] >= 0]

    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month
    df["Quarter"] = df["Order Date"].dt.quarter
    df["Order_Day"] = df["Order Date"].dt.day
    df["Year_Month"] = df["Order Date"].dt.to_period("M").astype(str)

    # Classification target
    df["High_Sales"] = (df["Sales"] > df["Sales"].median()).astype(int)

    print("Data cleaning completed successfully.")
    print("Final Shape:", df.shape)

    return df


def save_clean_data(df, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_csv(file_path, index=False)
    print("Cleaned data saved successfully:", file_path)