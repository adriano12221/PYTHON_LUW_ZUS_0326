from dataclasses import dataclass


@dataclass
class Car:
    brand: str
    model: str
    year: int
    price: float
    available: bool = True  # wartość domyślna

    def full_name(self) -> str:
        return f"{self.brand} {self.model} ({self.year})"

    @property
    def is_new(self) -> bool:
        return self.year >= 2023


# --- Demo ---
if __name__ == "__main__":
    car = Car("Toyota", "Corolla", 2024, 120000)

    print(car)               # automatyczne __repr__ z dataclass
    print(car.full_name())   # Toyota Corolla (2024)
    print(car.is_new)        # True
