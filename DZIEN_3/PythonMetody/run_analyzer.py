from abc import ABC, abstractmethod

class DataAnalyzer(ABC):

    @abstractmethod
    def process(self, data):
        pass

    @staticmethod
    def normalize(value, max_value):
        return value / max_value

    @classmethod
    def create_default(cls):
        return cls()

class RunAnalyzer(DataAnalyzer):

    def process(self, runs):
        max_distance = max(run["distance"] for run in runs)
        for run in runs:
            normalized = self.normalize(run["distance"], max_distance)
            yield {
                "distance": run["distance"],
                "time": run["time"],
                "normalized_distance": normalized
            }

runs = [
    {"distance": 5, "time": 23},
    {"distance": 5, "time": 28},
    {"distance": 12, "time": 67},
    {"distance": 10, "time": 51},
    {"distance": 5, "time": 21},
]

analyzer = RunAnalyzer.create_default()
for run in analyzer.process(runs):
    print(run)
