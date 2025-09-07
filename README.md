# End-to-End MLOPS Project: FX Price Forecasting with ZenML

This project demonstrates a complete, end-to-end Machine Learning Operations (MLOPS) workflow for a time-series forecasting problem. It uses a modern, Python-native stack centered around ZenML to orchestrate the entire lifecycle, from data ingestion and training to monitoring for data drift.  

The goal is to predict the daily closing price of the EUR/USD foreign exchange pair using historical data fetched from the Alpha Vantage API.

---

## 🌟 Core MLOPS Concepts Demonstrated

This project is a practical, hands-on implementation of the key stages in the MLOPS lifecycle:

- **Data Ingestion & Versioning:** Automatically fetching live data and versioning it as artifacts within a reproducible pipeline.  
- **Experiment Tracking:** Using MLflow to log model parameters, metrics (RMSE), and the model object itself.  
- **Model Versioning:** Leveraging ZenML's Model Control Plane to register and track models linked directly to the pipeline runs that produced them.  
- **Pipeline Orchestration:** Defining training and monitoring workflows as clean, Pythonic pipelines using ZenML.  
- **Data & Model Monitoring:** Automatically detecting dataset drift between training data and new data using Evidently AI.  
- **Integrated MLOPS Stack:** Managing all infrastructure components (orchestrator, artifact store, experiment tracker) as a single, switchable ZenML "Stack".  

---

## 🛠️ Tech Stack & Tools

This project uses an integrated stack managed by ZenML to ensure reproducibility and ease of use.

| MLOps Stage        | Tool Used        | Purpose                                                        |
|--------------------|-----------------|----------------------------------------------------------------|
| Framework          | ZenML           | The core framework that orchestrates, versions, and connects all other tools. |
| Data Ingestion     | requests, pandas| To fetch and handle data from the Alpha Vantage API.            |
| Preprocessing      | pandas, scikit-learn | For feature engineering (creating lagged features).      |
| Experiment Tracking| MLflow          | To log and compare model experiments and metrics.               |
| Model Training     | scikit-learn    | To train a simple LinearRegression model.                       |
| Data Monitoring    | Evidently AI    | To generate interactive data drift reports.                     |
| Environment        | Python 3.9+ & venv | For managing dependencies.                                   |

---

## 📁 Project Structure

```

mlops-fx/
├── .zen/                     # ZenML repository configuration
├── mlruns/                   # Local MLflow tracking data
├── venv/                     # Python virtual environment
├── .env                      # Stores the Alpha Vantage API key (git-ignored)
├── .gitignore
├── pipeline.py               # Defines the main training pipeline (fetch, preprocess, train)
├── run.py                    # Script to execute the training pipeline
├── monitoring\_pipeline.py     # Defines the data drift monitoring pipeline
├── run\_monitoring.py          # Script to execute the monitoring pipeline
├── evidently\_materializer.py  # Custom materializer to handle Evidently Report objects
└── README.md                  # This file

````

---

## 🚀 Getting Started

Follow these steps to set up and run the project on your local machine.

### 1. Prerequisites
- Python (3.9 - 3.12 recommended)  
- An account and a free API key from Alpha Vantage.  

---

### 2. Setup the Environment

First, clone the repository and navigate into the project directory.  

Create and activate a Python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
````

Install required packages:

```bash
pip install zenml scikit-learn pandas requests python-dotenv evidently mlflow -q
```

---

### 3. Initialize ZenML and Integrations

Set up the ZenML repository and install the necessary integrations:

```bash
zenml init
zenml integration install mlflow evidently -y
```

---

### 4. Configure Your API Key

Create a `.env` file in the project root to store your secret API key:

```bash
touch .env
echo "ALPHA_VANTAGE_API_KEY=YOUR_KEY_HERE" > .env
```

---

### 5. Configure the ZenML Stack with MLflow

We need to configure ZenML to use a running MLflow server for experiment tracking.

#### a. Start the MLflow Server

Open a new terminal, activate the virtual environment, and run:

```bash
source venv/bin/activate
mlflow ui
```

Leave this terminal running. This is your persistent MLflow server.

#### b. Configure the ZenML Stack

In another terminal, run:

```bash
# Create a copy of the default stack
zenml stack copy default mlflow_stack

# Register the MLflow tracker
zenml experiment-tracker register mlflow_tracker --flavor=mlflow \
--tracking_uri=http://127.0.0.1:5000 \
--tracking_username=admin --tracking_password=admin

# Add the new tracker to your stack
zenml stack update mlflow_stack -e mlflow_tracker

# Set your new stack as the active one
zenml stack set mlflow_stack
```

---

### 6. Start the ZenML Server

To view the dashboard and the results of your pipeline runs, start the ZenML server:

```bash
zenml up
```

This will open the ZenML Dashboard in your browser at:
[http://127.0.0.1:8237](http://127.0.0.1:8237)

---

## 📈 Running the Pipelines

You are now ready to run the MLOPS pipelines!

### Run the Training Pipeline

Execute the training script:

```bash
python run.py
```

**View results:**

* Go to the ZenML Dashboard → Pipelines → `fx_training_pipeline` → latest run.
* Inspect artifacts (DataFrames, model).
* Follow the MLflow link to explore experiment tracking.

---

### Run the Monitoring Pipeline

Execute the monitoring script:

```bash
python run_monitoring.py
```

**View report:**

* Go to the ZenML Dashboard → Pipelines → `fx_monitoring_pipeline` → latest run.
* Click on the `generate_drift_report` step → output artifact `drift_report`.
* Open the **Visualisation** tab to see the full interactive Evidently AI report.

---
