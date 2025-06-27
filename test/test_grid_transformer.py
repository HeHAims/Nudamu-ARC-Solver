import numpy as np

class GridTransformer:
    @staticmethod
    def apply_rule(input_array, formula):
        shape = input_array.shape
        
        if formula == "y = ones":
            return np.ones(shape, dtype=int)
        
        elif formula == "y = identity":
            return input_array.copy()
        
        elif formula == "y = diag":
            return np.eye(*shape, dtype=int)
        
        elif formula == "y = anti_diag":
            n, m = shape
            output = np.zeros(shape, dtype=int)
            for i in range(n):
                output[i, m - 1 - i] = 1
            return output
        
        elif formula == "y = border":
            n, m = shape
            output = np.ones(shape, dtype=int)
            output[1:n-1, 1:m-1] = 0
            return output
        
        # Default fallback: return input unchanged
        else:
            return input_array.copy()
