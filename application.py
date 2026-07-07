import os

import pandas as pd
from flask import Flask, request, render_template, flash, redirect, url_for
from sklearn.metrics import r2_score

from src.exception import CustomException
from src.logger import logging
from src.pipelines.predict_pipeline import CustomData, PredictPipeline
from src.utils import load_object

application = Flask(__name__)
app = application
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

MODEL_PATH = os.path.join("artifacts", "model.pkl")
PREPROCESSOR_PATH = os.path.join("artifacts", "preprocessor.pkl")
TEST_DATA_PATH = os.path.join("artifacts", "test.csv")

MODEL_FRIENDLY_NAMES = {
    "RandomForestRegressor": "Random Forest",
    "DecisionTreeRegressor": "Decision Tree",
    "GradientBoostingRegressor": "Gradient Boosting",
    "LinearRegression": "Linear Regression",
    "KNeighborsRegressor": "K-Neighbors Regressor",
    "XGBRegressor": "XGBoost",
    "CatBoostRegressor": "CatBoost",
    "AdaBoostRegressor": "AdaBoost",
}


def get_model_stats():
    """Best-effort lookup of which model is deployed and its held-out R2 score."""
    try:
        if not (os.path.exists(MODEL_PATH) and os.path.exists(PREPROCESSOR_PATH) and os.path.exists(TEST_DATA_PATH)):
            return None, None

        model = load_object(MODEL_PATH)
        preprocessor = load_object(PREPROCESSOR_PATH)
        test_df = pd.read_csv(TEST_DATA_PATH)

        X_test = test_df.drop(columns=["math_score"])
        y_test = test_df["math_score"]

        X_test_transformed = preprocessor.transform(X_test)
        predictions = model.predict(X_test_transformed)
        r2 = r2_score(y_test, predictions)

        model_name = MODEL_FRIENDLY_NAMES.get(type(model).__name__, type(model).__name__)
        return model_name, r2
    except Exception as e:
        logging.error(f"Could not compute model stats: {e}")
        return None, None


@app.route('/')
def index():
    best_model_name, model_r2 = get_model_stats()
    return render_template('index.html', best_model_name=best_model_name, model_r2=model_r2)


@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')

    form_data = request.form.to_dict()
    required_fields = [
        'gender', 'race_ethnicity', 'parental_level_of_education',
        'lunch', 'test_preparation_course', 'reading_score', 'writing_score'
    ]

    missing = [f for f in required_fields if not form_data.get(f)]
    if missing:
        flash("Please fill in all fields before submitting.", "error")
        return render_template('home.html', form_data=form_data)

    try:
        reading_score = float(form_data['reading_score'])
        writing_score = float(form_data['writing_score'])
    except ValueError:
        flash("Reading and writing scores must be numbers.", "error")
        return render_template('home.html', form_data=form_data)

    if not (0 <= reading_score <= 100) or not (0 <= writing_score <= 100):
        flash("Reading and writing scores must be between 0 and 100.", "error")
        return render_template('home.html', form_data=form_data)

    try:
        data = CustomData(
            gender=form_data['gender'],
            race_ethnicity=form_data['race_ethnicity'],
            parental_level_of_education=form_data['parental_level_of_education'],
            lunch=form_data['lunch'],
            test_preparation_course=form_data['test_preparation_course'],
            reading_score=reading_score,
            writing_score=writing_score,
        )
        pred_df = data.get_data_as_data_frame()

        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)

        predicted_score = round(float(results[0]), 1)
        predicted_score = max(0, min(100, predicted_score))

        return render_template('home.html', results=predicted_score, form_data=form_data)

    except CustomException as e:
        logging.error(str(e))
        flash("Something went wrong while generating the prediction. Please try again.", "error")
        return render_template('home.html', form_data=form_data)


@app.errorhandler(404)
def not_found(e):
    return render_template(
        'error.html', code=404, title="Page Not Found",
        message="The page you're looking for doesn't exist."
    ), 404


@app.errorhandler(500)
def server_error(e):
    return render_template(
        'error.html', code=500, title="Something Went Wrong",
        message="An unexpected error occurred on our end. Please try again."
    ), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0")
