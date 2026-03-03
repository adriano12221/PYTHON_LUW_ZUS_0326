#generator z pamięcią stanu
def fibonacci(n):
    a,b = 0,1
    for _ in range(n):
        yield a
        a,b = b,a+b

for value in fibonacci(10):
    print(value)
