class RequireRunMeta(type):
    def __new__(cls, name, bases, attrs):
        if "run" not in attrs:
            raise TypeError("Class must have a run() method")
        return super().__new__(cls, name, bases, attrs)

class Worker(metaclass=RequireRunMeta):
    def run(self):
        print("Running worker")

w = Worker()
w.run()
