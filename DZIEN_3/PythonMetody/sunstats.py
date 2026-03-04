class RunStatistics:

    @staticmethod
    def average_time(times):
        return sum(times) / len(times)

    @staticmethod
    def best_time(times):
        return min(times)

    @staticmethod
    def worst_time(times):
        return max(times)

    @staticmethod
    def training_report(times):
        return f"Average time: {RunStatistics.average_time(times)}s\n" \
               f"Best time: {RunStatistics.best_time(times)}s\n" \
               f"Worst time: {RunStatistics.worst_time(times)}s"

runs = [42,38,40,45,37]
report = RunStatistics.training_report(runs)
print(report)
