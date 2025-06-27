# Phase 2: Rule Induction and Application

```python
import numpy as np

class CognitiveReasoner:
    def __init__(self):
        self.long_term_memory = []  # Learned rules
        self.working_memory = []    # Current task state

    def solve(self, examples):
        """Induce simple rules based on input-output examples."""
        induced_rules = []
        for inp, out in examples:
            if isinstance(inp, str) and isinstance(out, str):
                # Detect basic math equivalence
                rule = {"pattern": inp, "action": out}
            elif isinstance(inp, np.ndarray) and isinstance(out, np.ndarray):
                if (inp == out).all():
                    rule = {"pattern": "identity", "action": "copy"}
                elif self._is_diagonal(out):
                    rule = {"pattern": "diagonal", "action": "fill_diag"}
                else:
                    rule = {"pattern": "unknown", "action": "none"}
            else:
                rule = {"pattern": "unknown_type", "action": "none"}
            induced_rules.append(rule)
            self.long_term_memory.append(rule)
        return induced_rules

    def execute(self, solution, input_data):
        """Apply the learned rule to input data."""
        for rule in solution:
            if rule["pattern"] == "identity" and isinstance(input_data, np.ndarray):
                return input_data.copy()
            elif rule["pattern"] == "diagonal" and isinstance(input_data, np.ndarray):
                return np.eye(*input_data.shape, dtype=int)
            elif rule["pattern"] == input_data:
                return rule["action"]
        return input_data

    def _is_diagonal(self, grid):
        n = min(grid.shape)
        for i in range(n):
            if grid[i, i] != 1:
                return False
        return True
```

### Phase 2 Goals:
- Implement basic rule induction from examples ✅
- Apply induced rules during execution ✅
- Lay groundwork for more advanced induction (Phase 3) ✅

👉 Ready for Phase 3? 🚀

