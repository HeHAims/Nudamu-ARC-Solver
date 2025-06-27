import numpy as np

class CognitiveReasoner:
    def __init__(self):
        self.operations = {
            'complete_transform': self._apply_complete_transform,
            'identity': self._apply_identity,
            'border': self._apply_border,
            'center_dot': self._apply_center_dot
        }

    def reason_from_learned(self, learned_patterns, test_input):
        """Consistent reasoning with fallback handling"""
        if not learned_patterns:
            return self._default_output(test_input)

        # Flatten all patterns and select highest confidence
        all_patterns = []
        for pattern_set in learned_patterns:
            all_patterns.extend(pattern_set['patterns'])
        
        if not all_patterns:
            return self._default_output(test_input)

        best_pattern = max(all_patterns, key=lambda x: x['confidence'])

        # Apply the best matching operation
        operation = self.operations.get(best_pattern['type'], lambda x, _: x)
        try:
            output = operation(test_input, best_pattern)
            return {
                'output': output,
                'formula': best_pattern['type'],
                'score': best_pattern['confidence']
            }
        except Exception:
            return self._default_output(test_input)

    # Operation implementations
    def _apply_complete_transform(self, grid, pattern):
        return np.full_like(grid, pattern['value'])

    def _apply_identity(self, grid, _):
        return grid.copy()

    def _apply_border(self, grid, pattern):
        output = np.zeros_like(grid)
        output[0,:] = pattern['value']
        output[-1,:] = pattern['value']
        output[:,0] = pattern['value']
        output[:,-1] = pattern['value']
        return output

    def _apply_center_dot(self, grid, pattern):
        output = np.zeros_like(grid)
        center = (grid.shape[0]//2, grid.shape[1]//2)
        output[center] = pattern['value']
        return output

    def _default_output(self, test_input):
        return {
            'output': test_input.copy(),
            'formula': 'no_operation',
            'score': 0.001
        }