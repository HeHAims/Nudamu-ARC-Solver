# Nudamu ARC Solver

A clean, modular Python project for solving ARC (Abstraction and Reasoning Corpus) tasks using pattern detection, rule mapping, grid transformation, and symbolic formula translation.

---

## 📦 **Project Structure**

```
nudamu_arc_solver/
├── core/
│   ├── pattern_detector.py
│   ├── rule_mapper.py
│   ├── grid_transformer.py
│   └── formula_translator.py
├── data/
│   ├── dataset_loader.py
│   ├── submission_writer.py
│   └── secure_file_utils.py
├── utils/
│   ├── validators.py
│   └── logger.py
├── tests/
│   ├── test_pattern_detector.py
│   ├── test_rule_mapper.py
│   ├── test_grid_transformer.py
│   ├── test_formula_translator.py
│   └── test_dataset_loader.py
├── main.py
└── README.md
```

---

## 🚀 **Usage**

Run the main script:

```
python main.py
```

It will load ARC datasets, detect patterns, apply rules, translate formulas, and output a submission JSON.

---

## ✅ **Tests**

Run unit tests with:

```
python -m unittest discover tests
```

---

## 🧠 **Modules Overview**

- `pattern_detector.py`: Identifies grid patterns.
- `rule_mapper.py`: Maps patterns to symbolic rules.
- `grid_transformer.py`: Applies rules to grids.
- `formula_translator.py`: Parses and translates formulas.
- `dataset_loader.py`: Loads ARC JSON data.
- `submission_writer.py`: Outputs results JSON.
- `validators.py`: Validates inputs.
- `logger.py`: Handles logging.

---

## ✨ **Notes**

- Replace `train.json` / `test.json` paths in `main.py` with your actual dataset files.
- Extend pattern detection or rule mapping by editing the core modules.
- Contributions welcome (if you can handle the brilliance).

