def even_numbers(numbers):
    for number in numbers:
        if number % 2 == 0:
            yield number

data = range(1,21)

evens = even_numbers(data)

for e in evens:
    print(e)
