import unittest
import numpy as np
import os
import json
from core.pattern_detector import PatternDetector
from core.reasoning_engine import CognitiveReasoner
from nudamu_controller import NudamuController

class TestNudamuSolver(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.detector = PatternDetector()
        cls.reasoner = CognitiveReasoner()
        
        # Create test directory
        os.makedirs("test_data", exist_ok=True)
        
        # Define test cases
        cls.test_cases = [
            {
                "name": "diagonal_to_uniform",
                "input": [[1,0,0],[0,1,0],[0,0,1]],
                "output": [[1,1,1],[1,1,1],[1,1,1]],
                "expected_pattern": "complete_transform",
                "min_score": 0.95
            },
            {
                "name": "identity_transform",
                "input": [[0,1,0],[1,0,1],[0,1,0]],
                "output": [[0,1,0],[1,0,1],[0,1,0]],
                "expected_pattern": "identity",
                "min_score": 0.9
            },
            {
                "name": "rotation_90",
                "input": [[0,0,1],[0,1,0],[1,0,0]],
                "output": [[1,0,0],[0,1,0],[0,0,1]],
                "expected_pattern": "rotation",
                "min_score": 0.85
            }
        ]
        
        # Create test files
        with open("test_data/train.json", "w") as f:
            json.dump({
                f"test_task_{i}": [case] 
                for i, case in enumerate(cls.test_cases)
            }, f)
            
        with open("test_data/test.json", "w") as f:
            json.dump([{"input": case["input"]} for case in cls.test_cases], f)

    def test_pattern_detection(self):
        """Verify pattern detector identifies correct patterns"""
        for case in self.test_cases:
            with self.subTest(case=case["name"]):
                patterns = self.detector.detect_patterns(
                    np.array(case["input"]),
                    np.array(case["output"])
                )
                pattern_types = [p["type"] for p in patterns]
                self.assertIn(
                    case["expected_pattern"], pattern_types,
                    f"Failed on {case['name']}\n"
                    f"Expected: {case['expected_pattern']}\n"
                    f"Found: {pattern_types}"
                )

    def test_reasoning_execution(self):
        """Verify reasoning engine produces correct outputs"""
        for case in self.test_cases:
            with self.subTest(case=case["name"]):
                patterns = [{
                    "patterns": self.detector.detect_patterns(
                        np.array(case["input"]),
                        np.array(case["output"])
                    ),
                    "confidence": 0.9
                }]
                
                result = self.reasoner.reason_from_learned(
                    patterns,
                    np.array(case["input"])
                )
                
                self.assertTrue(
                    np.array_equal(result["output"], np.array(case["output"])),
                    f"Failed on {case['name']}\n"
                    f"Expected:\n{np.array(case['output'])}\n"
                    f"Got:\n{result['output']}"
                )

    def test_full_integration(self):
        """Test complete system from input to output"""
        controller = NudamuController()
        success = controller.run(
            train_path="test_data/train.json",
            test_path="test_data/test.json",
            submission_path="test_submission.json"
        )
        self.assertTrue(success)
        
        # Verify outputs
        with open("test_submission.json") as f:
            results = json.load(f)
            self.assertEqual(len(results), len(self.test_cases))
            
        # Verify scores
        with open("benchmark_results.json") as f:
            benchmarks = json.load(f)
            for bench, case in zip(benchmarks, self.test_cases):
                self.assertGreaterEqual(
                    bench["score"], case["min_score"],
                    f"Low score on {case['name']} "
                    f"(expected ≥{case['min_score']}, got {bench['score']})"
                )

    @classmethod
    def tearDownClass(cls):
        """Clean up test files"""
        for f in ["test_submission.json", "benchmark_results.json"]:
            if os.path.exists(f):
                os.remove(f)

if __name__ == "__main__":
    unittest.main(verbosity=2)