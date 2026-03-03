class DataSet:

    def __init__(self, data):
        self._data = data
        self._mean_cache = None

    @property
    def mean(self):
        if self._mean_cache is None:
            print("Liczmy średnią!")
            self._mean_cache = sum(self._data) / len(self._data)
        return self._mean_cache

d = DataSet([1, 2, 3, 4, 5, 75,899,3,24,63,235,78,32,64,69,112])
print(d.mean)
print(d.mean)
