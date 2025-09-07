# pipeline.py
import pandas as pd
import numpy as np
import requests
import os
from dotenv import load_dotenv
from io import StringIO

# We ONLY need Annotated now. The complex imports are gone.
from typing_extensions import Annotated
from zenml import step, pipeline

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# The return type hint is now much cleaner. We just name the output.
# The installed integrations will automatically create visualizations.
@step
def fetch_data() -> Annotated[pd.DataFrame, "raw_data"]:
    """Fetches data from Alpha Vantage and returns a DataFrame."""
    print("Fetching data...")
    load_dotenv()
    API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
    if not API_KEY:
        raise ValueError("ALPHA_VANTAGE_API_KEY not found in .env file.")
    
    URL = f"https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=USD&to_symbol=INR&outputsize=full&apikey={API_KEY}&datatype=csv"
    
    response = requests.get(URL)
    response.raise_for_status()
    
    df = pd.read_csv(StringIO(response.text))
    print(f"Data fetched successfully with {len(df)} rows.")
    return df

@step
def preprocess_data(df: pd.DataFrame) -> Annotated[pd.DataFrame, "processed_data"]:
    """Creates lagged features for the model."""
    print("Preprocessing data...")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp').reset_index(drop=True)
    df.rename(columns={'close': 'y'}, inplace=True)
    for i in range(1, 6):
        df[f'lag_{i}'] = df['y'].shift(i)
    df.dropna(inplace=True)
    print("Preprocessing complete.")
    return df

@step
def train_model(df: pd.DataFrame) -> Annotated[LinearRegression, "trained_model"]:
    """Trains a linear regression model and logs metrics to MLflow."""
    print("Training model...")
    import mlflow
    mlflow.autolog(log_models=True, log_input_examples=False, silent=True)
    
    features = [col for col in df.columns if 'lag_' in col]
    X = df[features]
    y = df['y']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    lr = LinearRegression()
    lr.fit(X_train, y_train)
    
    preds = lr.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    print(f"Model trained with RMSE: {rmse}")
    mlflow.log_metric("rmse", rmse)
    
    return lr

@pipeline(enable_cache=False)
def fx_training_pipeline():
    """The main training pipeline that connects all the steps."""
    raw_data = fetch_data()
    processed_data = preprocess_data(raw_data)
    train_model(processed_data)