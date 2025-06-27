import json

class SubmissionWriter:
    @staticmethod
    def write_json(path, data):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
