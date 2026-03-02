#programowanie funkcyjne
#ex1 - funkcja jako obiekt
#tryby silnika samochodu

def eco_mode(speed):
    return speed * 0.8

def sport_mode(speed):
    return speed * 1.2

mode = eco_mode

print(mode(100))
print(type(mode))

mode = sport_mode
print(mode(100))
print(type(mode))

#ex2 - funkcja jako argument
#system punktacji

def score_by_time(time):
    return max(0,500-time)

def score_by_consistancy(time):
    return 1000/(1+time)

def evaluate(time, scoring_strategy):
    return scoring_strategy(time)

print(evaluate(100, score_by_time))
print(evaluate(300, score_by_consistancy))

#ex3 - funkcja jako fabryka
#generator osobowości

def make_coach(multiplier):
    def coach(speed):
        return speed * multiplier
    return coach

strict_coach = make_coach(1.3)
calm_coach = make_coach(0.96)

print(strict_coach(10))
print(calm_coach(10))

#ex4 - kompozycja
#pipeline transformacji

def add_tax(x):
    return x * 1.23

def apply_discount(x):
    return x * 0.9

def compose(f, g):
    return lambda x: f(g(x))

final_price = compose(add_tax, apply_discount)

print(final_price(100))

#ex5 - funkcja jako warunek
#finteligentny filtr

def make_filter(threshold):
    def filter_func(value):
        return value > threshold
    return filter_func

high_filter = make_filter(100)
data = [50,120,80,200]
filtered_data = list(filter(high_filter, data))
print(filtered_data)
