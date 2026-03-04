class Engine:
    def __init__(self, horsepower: int):
        self.horsepower = horsepower

    def start(self) -> str:
        return f"Starting V{self.horsepower} engine"

class Car:
    def __init__(self, model: str, horsepower: int):
        self.model = model
        self.engine = Engine(horsepower)

    def start(self) -> str:
        return f"{self.model} started with {self.engine.start()}"

car = Car("BMW", 300)
print(car.start())
