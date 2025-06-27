import re

class FormulaTranslator:
    def __init__(self):
        self.grammatical_map = {
            'y': {'category': 'pronombre'},
            'm': {'category': ['sustantivo', 'verbo']},
            'x': {'category': ['preposición', 'adjetivo']},
            'b': {'category': ['adverbio', 'artículo']},
            '+': {'category': 'conjunción copulativa'},
            '-': {'category': 'conjunción adversativa'},
            '*': {'category': 'conjunción multiplicativa'},
            '/': {'category': 'conjunción divisiva'},
            '=': {'category': 'verbo copulativo'},
            '^': {'category': 'preposición de potencia'},
            'π': {'category': 'sustantivo abstracto'},
            'θ': {'category': 'sustantivo concreto'}
        }
        self.translation_rules = {
            'y': "el resultado",
            'm': "la magnitud que modifica",
            'x': "la variable fundamental",
            'b': "el término constante",
            '+': "sumado con",
            '-': "restado de",
            '*': "multiplicado por",
            '/': "dividido entre",
            '=': "equivale a",
            '^': "elevado a la potencia de",
            'π': "la constante circular",
            'θ': "el ángulo"
        }

    def parse_formula(self, formula):
        formula = re.sub(r'\s+', '', formula.lower())
        tokens = re.split(r'([a-z]+|[0-9.]+|[+\-*/^=()])', formula)
        tokens = [t for t in tokens if t]
        parsed = {'left': [], 'operator': '=', 'right': []}
        side = 'left'
        for token in tokens:
            if token == '=':
                side = 'right'
                parsed['operator'] = '='
            else:
                parsed[side].append(token)
        return parsed

    def translate_expression(self, tokens):
        return " ".join(self.translation_rules.get(t, t) for t in tokens)

    def translate_to_grammar(self, formula):
        parsed = self.parse_formula(formula)
        left = self.translate_expression(parsed['left'])
        right = self.translate_expression(parsed['right'])
        return f"{left} equivale a {right}"
