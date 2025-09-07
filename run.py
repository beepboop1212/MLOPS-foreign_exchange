# run.py
from pipeline import fx_training_pipeline

if __name__ == "__main__":
    print("Starting pipeline run...")
    # This is the command that executes your entire MLOPS pipeline
    fx_training_pipeline()
    print("Pipeline run finished.")