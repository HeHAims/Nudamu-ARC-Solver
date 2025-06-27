import numpy as np

class GridTransformer:
    @staticmethod
    def apply_rule(grid, rule):
        arr = np.array(grid)
        if rule == "y = diag":
            return np.full_like(arr, arr.diagonal()[0])
        elif rule == "y = anti_diag":
            n = arr.shape[0]
            anti_diag_vals = [arr[i, n - i - 1] for i in range(n)]
            return np.full_like(arr, anti_diag_vals[0])
        elif rule == "y = v + a":
            mid = arr.shape[1] // 2
            return np.tile(arr[:, [mid]], (1, arr.shape[1]))
        elif rule == "y = h + a":
            mid = arr.shape[0] // 2
            return np.tile(arr[[mid], :], (arr.shape[0], 1))
        elif rule == "y = border":
            transformed = arr.copy()
            transformed[1:-1, 1:-1] = 1 - transformed[1:-1, 1:-1]
            return transformed
        elif rule == "y = ones":
            return np.ones_like(arr)
        elif rule == "y = identity":
            return arr.copy()
        else:
            return arr.copy()
