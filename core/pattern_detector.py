import numpy as np
from scipy.ndimage import label

class PatternDetector:
    def detect_patterns(self, input_grid, output_grid):
        """Consistent pattern detection with priority handling"""
        input_grid = np.array(input_grid)
        output_grid = np.array(output_grid)
        patterns = []

        # Priority 1: Complete transforms
        if self._detect_complete_transform(input_grid, output_grid, patterns):
            return patterns
            
        # Priority 2: Identity
        if self._detect_identity(input_grid, output_grid, patterns):
            return patterns
            
        # Priority 3: Common ARC patterns
        self._detect_common_arc_patterns(input_grid, output_grid, patterns)
        
        return patterns if patterns else [{'type': 'unknown', 'confidence': 0.1}]

    def _detect_complete_transform(self, input_grid, output_grid, patterns):
        if np.all(output_grid == output_grid[0,0]):
            patterns.append({
                'type': 'complete_transform',
                'value': int(output_grid[0,0]),
                'confidence': 0.95
            })
            return True
        return False

    def _detect_identity(self, input_grid, output_grid, patterns):
        if np.array_equal(input_grid, output_grid):
            patterns.append({
                'type': 'identity',
                'confidence': 1.0
            })
            return True
        return False

    def _detect_common_arc_patterns(self, input_grid, output_grid, patterns):
        # Border detection
        if (output_grid.shape[0] >= 3 and output_grid.shape[1] >= 3 and
            np.all(output_grid[0,:] == output_grid[0,0]) and
            np.all(output_grid[-1,:] == output_grid[0,0]) and
            np.all(output_grid[:,0] == output_grid[0,0]) and
            np.all(output_grid[:,-1] == output_grid[0,0])):
            
            patterns.append({
                'type': 'border',
                'value': int(output_grid[0,0]),
                'confidence': 0.9
            })

        # Center dot detection for 3x3 grids
        if (output_grid.shape == (3,3) and 
            output_grid[1,1] != 0 and 
            np.sum(output_grid) == output_grid[1,1]):
            
            patterns.append({
                'type': 'center_dot',
                'value': int(output_grid[1,1]),
                'confidence': 0.85
            })