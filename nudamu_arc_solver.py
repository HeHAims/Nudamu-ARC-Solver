import json
import time
import numpy as np
from core.pattern_detector import PatternDetector
from core.rule_mapper import RuleMapper
from core.reasoning_engine import CognitiveReasoner
from data.dataset_loader import DatasetLoader
from data.submission_writer import SubmissionWriter
from utils.logger import Logger

class NudamuController:
    def __init__(self):
        self.detector = PatternDetector()
        self.mapper = RuleMapper()
        self.engine = CognitiveReasoner()
        self.logger = Logger.setup_logger()
        self.logger.info("NudamuController initialized")

    def run(self, train_path="data/train.json", test_path="data/test.json", submission_path="submission.json"):
        try:
            self.logger.info("Starting ARC task processing")

            # Load data
            train_data = DatasetLoader.load_json(train_path)
            test_data = DatasetLoader.load_json(test_path)

            # Process tasks
            results = self._process_all_tasks(train_data, test_data)

            # Save results
            SubmissionWriter.write_json(submission_path, results["submission"])
            with open("benchmark_results.json", "w") as f:
                json.dump(results["benchmark"], f, indent=2)

            self.logger.info(f"Successfully processed {len(results['submission'])} tasks")
            return True

        except Exception as e:
            self.logger.error(f"Error in controller run: {str(e)}")
            return False

    def _process_all_tasks(self, train_data, test_data):
        submission = []
        benchmark = []

        # Standardize data format
        test_data = self._ensure_dict_format(test_data)
        train_data = self._ensure_dict_format(train_data)

        for task_id, test_cases in test_data.items():
            try:
                if not test_cases:
                    continue

                result = self._process_single_task(
                    task_id,
                    train_data.get(task_id, []),
                    test_cases[0]["input"]
                )

                submission.append(result["submission"])
                benchmark.append(result["benchmark"])

            except Exception as e:
                self.logger.warning(f"Failed task {task_id}: {str(e)}")
                continue

        return {"submission": submission, "benchmark": benchmark}

    def _process_single_task(self, task_id, train_examples, test_input):
        start_time = time.time()

        # Learn patterns
        learned_patterns = []
        for example in train_examples:
            try:
                input_grid = np.array(example["input"])
                output_grid = np.array(example["output"])
                patterns = self.detector.detect_patterns(input_grid, output_grid)
                formula = self.mapper.map_patterns_to_formula(patterns)
                learned_patterns.append({
                    "patterns": patterns,
                    "formula": formula,
                    "confidence": len(patterns)/10
                })
            except Exception as e:
                self.logger.warning(f"Error learning from example in {task_id}: {str(e)}")
                continue

        # Apply reasoning
        result = self.engine.reason_from_learned(learned_patterns, np.array(test_input))
        duration = time.time() - start_time

        return {
            "submission": {
                "task_id": task_id,
                "output": result["output"].tolist() if isinstance(result["output"], np.ndarray) else result["output"],
                "formula": result.get("formula", ""),
                "interpretation": result.get("interpretation", ""),
                "duration": duration
            },
            "benchmark": {
                "task_id": task_id,
                "score": result.get("score", 0),
                "duration": duration
            }
        }

    def _ensure_dict_format(self, data):
        if isinstance(data, list):
            return {f"task_{i:03d}": [item] for i, item in enumerate(data)}
        return data

if __name__ == "__main__":
    import os
    print("Nudamu ARC Solver - Starting...")
    if not os.path.exists("data"):
        print("❌ Data directory 'data/' not found. Please make sure 'train.json' and 'test.json' are inside it.")
        exit(1)

    controller = NudamuController()
    controller.run("data/arc-agi_training_solutions.json", "data/arc-agi_training_challenges.json", "submission.json")
