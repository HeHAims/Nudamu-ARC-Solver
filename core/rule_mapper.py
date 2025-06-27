# core/rule_mapper.py (Complete Implementation)
class RuleMapper:
    def map_patterns_to_formula(self, patterns):
        """Converts detected patterns into executable rules"""
        rules = []
        priority_order = [
            'shape_change',
            'rotation',
            'flip',
            'color_mapping',
            'math_operation',
            'structural'
        ]
        
        # Sort patterns by priority
        sorted_patterns = sorted(patterns,
                               key=lambda x: priority_order.index(x['type']) 
                               if x['type'] in priority_order else len(priority_order))
        
        for pattern in sorted_patterns:
            if pattern['type'] == 'color_mapping':
                rules.append(self._create_color_mapping_rule(pattern))
            elif pattern['type'] == 'math_operation':
                rules.append(self._create_math_rule(pattern))
            elif pattern['type'] == 'rotation':
                rules.append(f"output = rotate(input, {pattern['degrees']})")
            elif pattern['type'] == 'flip':
                rules.append(f"output = flip(input, '{pattern['axis']}')")
            elif pattern['type'] == 'structural':
                rules.append(self._create_structural_rule(pattern))
            elif pattern['type'] == 'shape_change':
                rules.append(f"output = reshape(input, {pattern['to']})")
        
        return " AND ".join(rules) if rules else "NO_PATTERN"

    def _create_color_mapping_rule(self, pattern):
        """Generates color mapping rules"""
        mapping = pattern['map']
        conditions = []
        for src, dest in mapping.items():
            conditions.append(f"input=={src} -> {dest}")
        return f"MAP: {'; '.join(conditions)}"

    def _create_math_rule(self, pattern):
        """Generates math operation rules"""
        op = pattern['op']
        val = pattern['value']
        if op == 'add':
            return f"output = input + {val}"
        elif op == 'multiply':
            return f"output = input * {val}"
        return ""

    def _create_structural_rule(self, pattern):
        """Generates structural pattern rules"""
        if pattern['pattern'] == 'uniform':
            return f"FILL: all={pattern['value']}"
        elif pattern['pattern'] == 'border':
            return f"BORDER: val={pattern['value']}"
        return ""