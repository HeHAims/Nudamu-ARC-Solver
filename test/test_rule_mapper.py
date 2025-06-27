# rule_mapper.py

class RuleMapper:
    @staticmethod
    def map_pattern_to_formula(input_grid, output_grid):
        # Example basic mapping logic
        if (input_grid == output_grid).all():
            return "y = identity"

        if RuleMapper._is_diagonal(output_grid):
            return "y = diag"

        if RuleMapper._is_border(output_grid):
            return "y = border"

        if RuleMapper._is_checkerboard(output_grid):
            return "y = checkerboard"

        # Add more rules as needed
        return "y = unknown"

    @staticmethod
    def _is_diagonal(grid):
        n = min(grid.shape)
        for i in range(n):
            if grid[i, i] != 1:
                return False
        return True

    @staticmethod
    def _is_border(grid):
        top = (grid[0, :] == 1).all()
        bottom = (grid[-1, :] == 1).all()
        left = (grid[:, 0] == 1).all()
        right = (grid[:, -1] == 1).all()
        return top and bottom and left and right

    @staticmethod
    def _is_checkerboard(grid):
        pattern = (np.indices(grid.shape).sum(axis=0) % 2)
        return (grid == pattern).all()
