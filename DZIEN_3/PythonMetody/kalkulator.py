class Calculator:

    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def substract(a, b):
        return a - b

    @staticmethod
    def multiply(a, b):
        return a * b

    @staticmethod
    def divide(a, b):
        if b==0:
            raise ValueError("Cannot divide by zero")
        return a / b

print(Calculator.add(1, 2))
print(Calculator.substract(10, 5))
print(Calculator.multiply(2, 3))
print(Calculator.divide(10, 2))
