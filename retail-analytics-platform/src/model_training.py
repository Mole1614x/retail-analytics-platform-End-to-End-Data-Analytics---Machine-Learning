import os
import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    accuracy_score,
    confusion_matrix,
    classification_report
)


def make_one_hot_encoder():
    try:
        return OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:
        return OneHotEncoder(handle_unknown="ignore", sparse=False)


def get_features(df):
    features = [
        "Ship Mode",
        "Segment",
        "Region",
        "State",
        "City",
        "Category",
        "Sub-Category",
        "Year",
        "Month",
        "Quarter",
        "Order_Day",
        "Ship_Days"
    ]

    return df[features]


def get_preprocessor(x):
    numeric_features = x.select_dtypes(include=["int64", "float64"]).columns
    categorical_features = x.select_dtypes(include=["object"]).columns

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_features),
            ("cat", make_one_hot_encoder(), categorical_features)
        ]
    )

    return preprocessor


def train_regression_model(df):
    print("\n=========== Regression: Sales Prediction =============")

    x = get_features(df)
    y = df["Sales"]

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42
    )

    models = {
        "Linear Regression": LinearRegression(),
        "Decision Tree Regressor": DecisionTreeRegressor(random_state=42),
        "Random Forest Regressor": RandomForestRegressor(
            n_estimators=100,
            random_state=42
        )
    }

    results = []

    best_model = None
    best_score = -999999

    for name, model in models.items():
        pipeline = Pipeline([
            ("preprocessor", get_preprocessor(x_train)),
            ("model", model)
        ])

        pipeline.fit(x_train, y_train)

        y_pred = pipeline.predict(x_test)

        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)

        results.append([name, mae, mse, rmse, r2])

        print("\nModel:", name)
        print("MAE:", mae)
        print("MSE:", mse)
        print("RMSE:", rmse)
        print("R2 Score:", r2)

        if r2 > best_score:
            best_score = r2
            best_model = pipeline

    results_df = pd.DataFrame(
        results,
        columns=["Model", "MAE", "MSE", "RMSE", "R2 Score"]
    )

    os.makedirs("output/reports", exist_ok=True)
    results_df.to_csv("output/reports/regression_results.csv", index=False)

    os.makedirs("output/models", exist_ok=True)
    joblib.dump(best_model, "output/models/best_sales_prediction_model.pkl")

    print("\nBest sales prediction model saved successfully.")


def train_classification_model(df):
    print("\n=========== Classification: High Sales Prediction ===========")

    x = get_features(df)
    y = df["High_Sales"]

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42, stratify=y
    )

    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "Random Forest": RandomForestClassifier(random_state=42),
        "KNN": KNeighborsClassifier(n_neighbors=5),
        "Naive Bayes": GaussianNB(),
        "SVM": SVC(kernel="linear")
    }

    results = []

    best_model = None
    best_accuracy = 0

    for name, model in models.items():
        pipeline = Pipeline([
            ("preprocessor", get_preprocessor(x_train)),
            ("model", model)
        ])

        pipeline.fit(x_train, y_train)

        y_pred = pipeline.predict(x_test)

        accuracy = accuracy_score(y_test, y_pred)

        results.append([name, accuracy])

        print("\nModel:", name)
        print("Accuracy:", accuracy)
        print("Confusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        print("Classification Report:")
        print(classification_report(y_test, y_pred, zero_division=0))

        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_model = pipeline

    results_df = pd.DataFrame(
        results,
        columns=["Model", "Accuracy"]
    )

    os.makedirs("output/reports", exist_ok=True)
    results_df.to_csv("output/reports/classification_results.csv", index=False)

    os.makedirs("output/models", exist_ok=True)
    joblib.dump(best_model, "output/models/best_high_sales_model.pkl")

    print("\nBest high sales classification model saved successfully.")


def tune_random_forest_classifier(df):
    print("\n========== Hyperparameter Tuning ==========")

    x = get_features(df)
    y = df["High_Sales"]

    pipeline = Pipeline([
        ("preprocessor", get_preprocessor(x)),
        ("model", RandomForestClassifier(random_state=42))
    ])

    param_grid = {
        "model__n_estimators": [50, 100],
        "model__max_depth": [5, 10, None],
        "model__min_samples_split": [2, 5]
    }

    grid_search = GridSearchCV(
        pipeline,
        param_grid,
        cv=3,
        scoring="accuracy",
        n_jobs=-1
    )

    grid_search.fit(x, y)

    print("Best Parameters:", grid_search.best_params_)
    print("Best Accuracy:", grid_search.best_score_)

    os.makedirs("output/models", exist_ok=True)

    joblib.dump(
        grid_search.best_estimator_,
        "output/models/tuned_random_forest_classifier.pkl"
    )

    print("Tuned model saved successfully.")