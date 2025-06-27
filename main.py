import argparse
import json
import time
import numpy as np

from core.reasoning_engine import ReasoningEngine
from data.dataset_loader import DatasetLoader
from data.submission_writer import SubmissionWriter
from utils.logger import Logger

def run_engine(train_path, test_path, submission_path, benchmark_path):
    logger = Logger()
    loader = DatasetLoader()
    engine = ReasoningEngine()

    train_data = loader.load_json(train_path)
    test_data = loader.load_json(test_path)

    submission = []
    benchmark = []

    learned_patterns = []
    for task_id, cases in train_data.items():
        for case in cases:
            learned_patterns.append({
                "input": case["input"],
                "output": case["output"]
            })

    for task_id, cases in test_data.items():
        for case in cases:
            test_input = np.array(case["input"])
            logger.info(f"Processing task: {task_id}")

            start_time = time.time()
            result = engine.reason_from_learned(learned_patterns, test_input)
            duration = time.time() - start_time

            logger.info(f"Task {task_id}: Formula {result['formula']} | Score {result['score']:.2f} | Time {duration:.4f}s")

            submission.append({
                "task_id": task_id,
                "output": result["output"]
            })
            benchmark.append({
                "task_id": task_id,
                "formula": result["formula"],
                "score": result["score"],
                "duration": duration
            })

    SubmissionWriter.write_json(submission_path, submission)
    logger.info(f"✅ Submission saved to {submission_path}")

    SubmissionWriter.write_json(benchmark_path, benchmark)
    logger.info(f"[INFO] Benchmark results saved to {benchmark_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", required=True, help="Path to training challenges JSON")
    parser.add_argument("--test", required=True, help="Path to test challenges JSON")
    parser.add_argument("--submission", default="submission.json", help="Path to save submission JSON")
    parser.add_argument("--benchmark", default="benchmark_results.json", help="Path to save benchmark results")
    args = parser.parse_args()

    run_engine(args.train, args.test, args.submission, args.benchmark)
