class RunAnalyzer:

    @staticmethod
    def pace(distance, time):
        return time/distance

    @staticmethod
    def average_pace(runs):
        paces = []

        for run in runs:
            p = RunAnalyzer.pace(run["distance"], run["time"])
            paces.append(p)
        return sum(paces)/len(paces)

    @staticmethod
    def longest_run(runs):
        return max(runs, key=lambda r: r["time"])

    @staticmethod
    def training_summary(runs):
        total_distance = sum(run["distance"] for run in runs)
        avg_pace = RunAnalyzer.average_pace(runs)
        longest = RunAnalyzer.longest_run(runs)
        return f"Total distance: {total_distance} km\n" \
               f"Average pace: {avg_pace:.2f} min/km\n" \
               f"Longest run: {longest['distance']} km in {longest['time']} s"


runs = [
    {"distance": 5, "time": 23},
    {"distance": 5, "time": 28},
    {"distance": 12, "time": 67},
    {"distance": 10, "time": 51},
    {"distance": 5, "time": 21},
    {"distance": 21, "time": 112},
    {"distance": 45, "time": 305},
    {"distance": 10, "time": 26},
]

report = RunAnalyzer.training_summary(runs)
print(report)
