import unittest
import numpy as np
import time
from core.reasoner import Reasoner

class TestReasoner(unittest.TestCase):
    def setUp(self):
        self.reasoner = Reasoner()

    def test_diagonal_plan(self):
        grid = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ])
        expected = np.ones((3, 3), dtype=int)
        train_output = expected.copy()
        result = self.reasoner.reason(grid, train_output, grid)
        self.assertTrue(np.array_equal(result["output"], expected.tolist()))
        self.assertIn("diag", result["formula"])

    def test_border_plan(self):
        grid = np.array([
            [1, 1, 1],
            [1, 0, 1],
            [1, 1, 1]
        ])
        inverted_inside = grid.copy()
        inverted_inside[1, 1] = 1
        train_output = inverted_inside
        result = self.reasoner.reason(grid, train_output, grid)
        self.assertTrue(np.array_equal(result["output"], train_output.tolist()))
        self.assertIn("border", result["formula"])

    def test_vertical_stripe_plan(self):
        grid = np.zeros((3, 3), dtype=int)
        grid[:, 1] = 1
        expected = np.tile(grid[:, [1]], (1, 3))
        train_output = expected.copy()
        result = self.reasoner.reason(grid, train_output, grid)
        self.assertTrue(np.array_equal(result["output"], expected.tolist()))
        self.assertIn("v + a", result["formula"])

    def test_uniform_plan(self):
        grid = np.ones((3, 3), dtype=int)
        train_output = grid.copy()
        result = self.reasoner.reason(grid, train_output, grid)
        self.assertTrue(np.array_equal(result["output"], train_output.tolist()))
        self.assertIn("ones", result["formula"])

    def test_identity_when_no_pattern(self):
        grid = np.array([
            [0, 1],
            [1, 0]
        ])
        train_output = grid.copy()
        result = self.reasoner.reason(grid, train_output, grid)
        self.assertTrue(np.array_equal(result["output"], train_output.tolist()))
        self.assertIn("identity", result["formula"])

    def test_invalid_grid_error(self):
        with self.assertRaises(ValueError):
            self.reasoner.reason("invalid", [[1]], [[1]])

    def test_speed_on_large_grid(self):
        grid = np.eye(50, dtype=int)
        train_output = np.ones((50, 50), dtype=int)
        start = time.time()
        result = self.reasoner.reason(grid, train_output, grid)
        duration = time.time() - start
        self.assertLess(duration, 1.0, "Reasoner is too slow on large grid")
        self.assertTrue(np.array_equal(result["output"], train_output.tolist()))

    def test_benchmark_multiple_tasks(self):
        tasks = [
            (np.eye(10, dtype=int), np.ones((10, 10), dtype=int)),
            (np.ones((10, 10), dtype=int), np.ones((10, 10), dtype=int)),
            (np.zeros((10, 10), dtype=int), np.zeros((10, 10), dtype=int))
        ]
        total_time = 0
        for grid, train_output in tasks:
            start = time.time()
            result = self.reasoner.reason(grid, train_output, grid)
            duration = time.time() - start
            total_time += duration
            self.assertTrue(np.array_equal(result["output"], train_output.tolist()))
        print(f"Benchmark: processed {len(tasks)} tasks in {total_time:.4f} seconds")

if __name__ == "__main__":
    unittest.main()
