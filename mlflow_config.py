import mlflow
import mlflow.pytorch
import os
from datetime import datetime


class MLflowConfig:
    """MLflow configuration and logging utilities"""
    
    def __init__(self, experiment_name="bone_age_estimation"):
        self.experiment_name = experiment_name
        self.tracking_uri = os.path.join(os.getcwd(), "mlruns")
        
        # Set tracking URI
        mlflow.set_tracking_uri(f"file:///{self.tracking_uri}")
        
        # Create or get experiment
        try:
            self.experiment_id = mlflow.create_experiment(experiment_name)
        except:
            self.experiment_id = mlflow.get_experiment_by_name(experiment_name).experiment_id
        
        mlflow.set_experiment(experiment_name)
        print(f"✓ MLflow initialized: {experiment_name}")
    
    def start_run(self, run_name=None):
        """Start a new MLflow run"""
        if run_name is None:
            run_name = f"prediction_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        return mlflow.start_run(run_name=run_name)
    
    def log_params(self, params: dict):
        """Log parameters to MLflow"""
        mlflow.log_params(params)
    
    def log_metrics(self, metrics: dict):
        """Log metrics to MLflow"""
        mlflow.log_metrics(metrics)
    
    def log_artifact(self, artifact_path: str):
        """Log artifact file to MLflow"""
        mlflow.log_artifact(artifact_path)
    
    def log_image(self, image_path: str, artifact_file: str = None):
        """Log image artifact to MLflow"""
        if artifact_file:
            mlflow.log_artifact(image_path, artifact_file)
        else:
            mlflow.log_artifact(image_path)
    
    def end_run(self):
        """End current MLflow run"""
        mlflow.end_run()
    
    def get_run_id(self):
        """Get current run ID"""
        return mlflow.active_run().info.run_id if mlflow.active_run() else None


# Global MLflow instance
mlflow_config = MLflowConfig()
