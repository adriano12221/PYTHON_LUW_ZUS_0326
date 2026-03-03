class Person:

    def __init__(self, name, age):
        self.name = name
        self._age = None #atrybut wewnętrzny
        self.age = age #użuycie property

    def get_age(self):
        return self._age

    def set_age(self, value):
        if value < 0:
            raise ValueError("Age cannot be negative")
        self._age = value

    age = property(get_age,set_age)

p = Person("Marcin",50)
print(p.age)
p.age = 53
print(p.age)
