import unittest
import numpy as np
from core.pattern_detector import PatternDetector

class TestPatternDetector(unittest.TestCase):
    def test_diagonal(self):
        grid = np.eye(3, dtype=int)
        patterns = PatternDetector.detect_patterns(grid)
        self.assertIn("diagonal", patterns)

    def test_vertical_stripe(self):
        grid = np.zeros((3,3), dtype=int)
        grid[:,1] = 1
        patterns = PatternDetector.detect_patterns(grid)
        self.assertIn("vertical_stripe", patterns)

    def test_border(self):
        grid = np.ones((3,3), dtype=int)
        grid[1,1] = 0
        patterns = PatternDetector.detect_patterns(grid)
        self.assertIn("border", patterns)

if __name__ == "__main__":
    unittest.main()
