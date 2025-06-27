import json
import os

class DatasetLoader:
    @staticmethod
    def load_json(path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def load_arc_dataset(train_path, test_path):
        train_data = DatasetLoader.load_json(train_path)
        test_data = DatasetLoader.load_json(test_path)
        return train_data, test_data
