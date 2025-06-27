# Phase 3: Program Synthesis and Meta-Reasoning

```python
import numpy as np

class CognitiveReasoner:
    def __init__(self):
        self.long_term_memory = []  # Persistent learned rules
        self.working_memory = []    # Current reasoning state

    def solve(self, examples):
        """Induce rules and synthesize programs."""
        induced_rules = self.induce_rules(examples)
        candidate_programs = self.synthesize_programs(induced_rules)
        best_program = self.select_best(candidate_programs, examples)
        return best_program

    def induce_rules(self, examples):
        rules = []
        for inp, out in examples:
            if isinstance(inp, str) and isinstance(out, str):
                rules.append({"pattern": inp, "action": out})
            elif isinstance(inp, np.ndarray) and isinstance(out, np.ndarray):
                if (inp == out).all():
                    rules.append({"pattern": "identity", "action": "copy"})
                elif self._is_diagonal(out):
                    rules.append({"pattern": "diagonal", "action": "fill_diag"})
                else:
                    rules.append({"pattern": "unknown", "action": "none"})
        self.long_term_memory.extend(rules)
        return rules

    def synthesize_programs(self, rules, depth=2):
        if depth == 1:
            return [[r] for r in rules]
        programs = []
        for r in rules:
            for sub in self.synthesize_programs(rules, depth - 1):
                programs.append([r] + sub)
        return programs

    def select_best(self, programs, examples):
        best = None
        best_score = -1
        for prog in programs:
            score = self.evaluate_program(prog, examples)
            if score > best_score:
                best_score = score
                best = prog
        return best

    def evaluate_program(self, program, examples):
        score = 0
        for inp, out in examples:
            predicted = self.execute(program, inp)
            if isinstance(predicted, np.ndarray) and (predicted == out).all():
                score += 1
            elif predicted == out:
                score += 1
        return score / len(examples)

    def execute(self, program, input_data):
        data = input_data
        for rule in program:
            if rule["pattern"] == "identity" and isinstance(data, np.ndarray):
                data = data.copy()
            elif rule["pattern"] == "diagonal" and isinstance(data, np.ndarray):
                data = np.eye(*data.shape, dtype=int)
            elif rule["pattern"] == data:
                data = rule["action"]
        return data

    def _is_diagonal(self, grid):
        n = min(grid.shape)
        return all(grid[i, i] == 1 for i in range(n))
```

### Phase 3 Goals:
- Combine rules into multi-step programs ✅
- Implement meta-reasoning to select best program ✅
- Prepare for adaptive feedback and dynamic learning (Phase 4) ✅

🚀 Onward to Phase 4!

