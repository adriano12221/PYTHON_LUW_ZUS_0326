#dekoratory w Pythonie
import time
from functools import wraps

#zadanie 1
def simple_logger(func):
    def wrapper():
        print("start funkcji")
        func()
        print("koniec funkcji")
    return wrapper

@simple_logger
def hello():
    print("Hello Python!")

def drugi():
    print("\nDrugi tekst!\n")

@simple_logger
def trzeci():
    print("Trzeci tekst!")

hello()
drugi()
trzeci()

#zadanie 2

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"Czas wykonania funkcji: {end - start:5f} sekund")
        return result
    return wrapper

@timer
def slow_function(n):
    time.sleep(n)
    return "Slow function completed"

print(slow_function(1))
print(slow_function(13))
