import unittest
import os
import json
from data.dataset_loader import DatasetLoader

class TestDatasetLoader(unittest.TestCase):
    def setUp(self):
        # Create a temporary JSON file
        self.temp_file = "temp_test.json"
        with open(self.temp_file, "w", encoding="utf-8") as f:
            json.dump({"test": 123}, f)

    def tearDown(self):
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)

    def test_load_json(self):
        data = DatasetLoader.load_json(self.temp_file)
        self.assertEqual(data, {"test": 123})

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            DatasetLoader.load_json("nonexistent.json")

if __name__ == "__main__":
    unittest.main()
