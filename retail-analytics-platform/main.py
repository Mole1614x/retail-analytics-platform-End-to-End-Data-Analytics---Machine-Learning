from src.data_cleaning import load_data, clean_data, save_clean_data
from src.eda import basic_eda, save_summary_reports, create_charts
from src.model_training import (
    train_regression_model,
    train_classification_model,
    tune_random_forest_classifier
)
from src.prediction import predict_high_sales, predict_sales
from src.database import save_to_sqlite, generate_sql_reports


def main():
    print("\n======================================")
    print("RETAIL ANALYTICS PLATFORM")
    print("======================================")

    input_file = "data/train.csv"
    cleaned_file = "output/reports/cleaned_superstore.csv"

    df = load_data(input_file)

    df = clean_data(df)

    save_clean_data(df, cleaned_file)

    #
    
    df_db = save_to_sqlite(df)
    generate_sql_reports()

    basic_eda(df)

    save_summary_reports(df)

    create_charts(df)

    train_regression_model(df)

    train_classification_model(df)

    tune_random_forest_classifier(df)

    sample_order = {
        "Ship Mode": "Second Class",
        "Segment": "Consumer",
        "Region": "South",
        "State": "Kentucky",
        "City": "Henderson",
        "Category": "Furniture",
        "Sub-Category": "Bookcases",
        "Year": 2017,
        "Month": 11,
        "Quarter": 4,
        "Order_Day": 8,
        "Ship_Days": 3
    }

    predicted_class = predict_high_sales(sample_order)
    predicted_sales = predict_sales(sample_order)

    print("\n========== SAMPLE PREDICTION ==========")
    print("Predicted Class:", predicted_class)
    print("Predicted Sales:", predicted_sales)

    print("\nProject executed successfully.")


if __name__ == "__main__":
    main()