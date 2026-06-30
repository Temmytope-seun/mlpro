# Student Performance Predictor

An end-to-end machine learning project that predicts a student's **math score** based on demographic information and their reading/writing scores. The project covers the full ML lifecycle — data ingestion, transformation, model training/selection, and deployment as a Flask web app.

## Overview

Given a student's:
- Gender
- Race/Ethnicity
- Parental level of education
- Lunch type (standard / free-reduced)
- Test preparation course status
- Reading score
- Writing score

...the model predicts their **math score** (0-100).

## Project Structure

```
studentPerformance/
├── app.py                          # Flask application entry point
├── artifacts/                      # Generated data splits, trained model & preprocessor
│   ├── data.csv
│   ├── train.csv
│   ├── test.csv
│   ├── model.pkl
│   └── preprocessor.pkl
├── notebook/
│   ├── data/stud.csv                       # Raw dataset
│   ├── 1 . EDA STUDENT PERFORMANCE.ipynb    # Exploratory data analysis
│   └── 2. MODEL TRAINING.ipynb              # Model experimentation
├── src/
│   ├── components/
│   │   ├── data_ingestion.py        # Reads raw data, splits into train/test
│   │   ├── data_transformation.py   # Builds preprocessing pipeline (imputation, encoding, scaling)
│   │   └── model_trainer.py         # Trains & tunes multiple regressors, picks the best
│   ├── pipelines/
│   │   ├── training_pipeline.py
│   │   └── predict_pipeline.py      # Loads saved model/preprocessor and serves predictions
│   ├── exception.py                 # Custom exception handling
│   ├── logger.py                    # Centralized logging
│   └── utils.py                     # Shared helpers (save/load objects, model evaluation)
├── templates/
│   ├── index.html                   # Landing page
│   └── home.html                    # Prediction form & result
├── requirements.txt
└── setup.py
```

## Pipeline

1. **Data Ingestion** (`src/components/data_ingestion.py`) — loads `notebook/data/stud.csv`, saves a raw copy, and performs an 80/20 train-test split into `artifacts/`.
2. **Data Transformation** (`src/components/data_transformation.py`) — builds a `ColumnTransformer`:
   - Numerical features (`reading_score`, `writing_score`): median imputation + standard scaling
   - Categorical features (`gender`, `race_ethnicity`, `parental_level_of_education`, `lunch`, `test_preparation_course`): most-frequent imputation + one-hot encoding + scaling
3. **Model Training** (`src/components/model_trainer.py`) — trains and grid-searches several regressors (Random Forest, Decision Tree, Gradient Boosting, Linear Regression, K-Neighbors, XGBoost, CatBoost, AdaBoost) and persists the best-performing model (by R² score) to `artifacts/model.pkl`.
4. **Prediction Pipeline** (`src/pipelines/predict_pipeline.py`) — loads the saved preprocessor and model to transform new input and return a prediction.

## Setup

```bash
# Clone the repo
git clone <repo-url>
cd studentPerformance

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Train the model

```bash
python -m src.components.data_ingestion
```

This runs ingestion → transformation → training, and saves `model.pkl` and `preprocessor.pkl` to `artifacts/`.

### Run the web app

```bash
python app.py
```

Then open `http://localhost:5000` in your browser, navigate to the prediction form, fill in the student's details, and submit to see the predicted math score.

## Tech Stack

- **Language:** Python
- **ML/Data:** scikit-learn, XGBoost, CatBoost, pandas, numpy
- **Web Framework:** Flask
- **Frontend:** HTML, Bootstrap 5

## Author

**Temmy** — temmytope60@gmail.com
