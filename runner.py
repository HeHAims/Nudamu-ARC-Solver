import json
import time
from data.dataset_loader import DatasetLoader
from data.submission_writer import SubmissionWriter
from utils.logger import Logger

class NudamuRunner:
    def __init__(self, controller):
        self.controller = controller
        self.logger = Logger.setup_logger()

    def execute_pipeline(self, train_path, test_path, submission_path):
        """Orchestrate the full execution pipeline"""
        try:
            start_time = time.time()
            
            # Load data
            train_data = DatasetLoader.load_json(train_path)
            test_data = DatasetLoader.load_json(test_path)
            
            # Standardize data format
            test_data = self._standardize_data_format(test_data)
            train_data = self._standardize_data_format(train_data)
            
            # Process tasks
            results = self.controller.process_tasks(train_data, test_data)
            
            # Save outputs
            self._save_results(results, submission_path)
            
            self.logger.info(f"Pipeline completed in {time.time() - start_time:.2f}s")
            return True
            
        except Exception as e:
            self.logger.error(f"Pipeline failed: {str(e)}")
            return False

    def _standardize_data_format(self, data):
        """Ensure consistent data format"""
        if isinstance(data, list):
            return {f"task_{idx:03d}": [item] for idx, item in enumerate(data)}
        return data

    def _save_results(self, results, submission_path):
        """Save both submission and benchmark results"""
        SubmissionWriter.write_json(submission_path, results["submission"])
        with open("benchmark_results.json", "w", encoding="utf-8") as f:
            json.dump(results["benchmark"], f, indent=2)
        self.logger.info("Results saved successfully")