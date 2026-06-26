import joblib
import pandas as pd


def predict_sales(sample_order):
    model = joblib.load("output/models/best_sales_prediction_model.pkl")

    input_df = pd.DataFrame([sample_order])

    prediction = model.predict(input_df)

    return round(float(prediction[0]), 2)


def predict_high_sales(sample_order):
    model = joblib.load("output/models/best_high_sales_model.pkl")

    input_df = pd.DataFrame([sample_order])

    prediction = model.predict(input_df)

    if prediction[0] == 1:
        return "High Sales Order"
    else:
        return "Low Sales Order"