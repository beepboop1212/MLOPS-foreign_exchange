# monitoring_pipeline.py
import pandas as pd

from zenml import step, pipeline
from zenml.client import Client

from typing_extensions import Annotated
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

# 1. Import our new custom materializer
from evidently_materializer import EvidentlyReportMaterializer

@step
def get_reference_data() -> Annotated[pd.DataFrame, "reference_data"]:
    """Fetches the reference data from a previous training run."""
    print("Fetching reference data...")
    client = Client()
    training_pipeline = client.get_pipeline("fx_training_pipeline")
    last_run = training_pipeline.last_successful_run
    
    reference_data = last_run.steps["preprocess_data"].outputs["processed_data"][0].load()
    
    print("Reference data fetched successfully.")
    return reference_data

@step
def get_current_data(reference_data: pd.DataFrame) -> Annotated[pd.DataFrame, "current_data"]:
    """Simulates fetching new, 'current' data."""
    print("Fetching current data (simulation)...")
    current_data = reference_data.tail(100)
    print("Current data fetched successfully.")
    return current_data

# 2. THIS IS THE FINAL, CORRECT STEP DEFINITION
# We tell the step to use our custom class for its output.
@step(output_materializers=EvidentlyReportMaterializer)
def generate_drift_report(
    reference_data: pd.DataFrame, current_data: pd.DataFrame
) -> Report:
    """
    Generates an Evidently AI data drift report using a custom materializer.
    """
    print("Generating data drift report...")
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=reference_data, current_data=current_data)
    print("Drift report generated.")
    return report

@pipeline(enable_cache=False)
def fx_monitoring_pipeline():
    """The main monitoring pipeline that connects all the steps."""
    reference_data = get_reference_data()
    current_data = get_current_data(reference_data)
    generate_drift_report(reference_data, current_data)