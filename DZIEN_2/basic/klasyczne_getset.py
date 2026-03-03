class Person:

    def __init__(self, name, age):
        self.name = name
        self._age = None #atrybut wewnętrzny
        self.set_age(age) #walidacja przez setter

    def get_age(self):
        return self._age

    def set_age(self, value):
        if value < 0:
            raise ValueError("Age cannot be negative")
        self._age = value

p = Person("Marcin",50)
print(p.get_age())
p.set_age(53)
print(p.get_age())
