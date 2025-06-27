import numpy as np

class Validators:
    @staticmethod
    def validate_grid(grid):
        if not isinstance(grid, (list, np.ndarray)):
            raise ValueError("Grid must be a list or numpy array.")
        arr = np.array(grid)
        if arr.ndim != 2:
            raise ValueError("Grid must be 2D.")
        if arr.size == 0:
            raise ValueError("Grid cannot be empty.")
        return True

    @staticmethod
    def validate_formula(formula):
        if not isinstance(formula, str) or not formula.strip():
            raise ValueError("Formula must be a non-empty string.")
        return True
