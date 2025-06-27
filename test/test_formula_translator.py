import unittest
from core.formula_translator import FormulaTranslator

class TestFormulaTranslator(unittest.TestCase):
    def setUp(self):
        self.translator = FormulaTranslator()

    def test_parse_and_translate_simple(self):
        formula = "y = mx + b"
        translation = self.translator.translate_to_grammar(formula)
        self.assertIn("el resultado", translation)
        self.assertIn("sumado con", translation)

    def test_parse_and_translate_power(self):
        formula = "a = π r ^ 2"
        translation = self.translator.translate_to_grammar(formula)
        self.assertIn("la constante circular", translation)
        self.assertIn("elevado a la potencia de", translation)

if __name__ == "__main__":
    unittest.main()
