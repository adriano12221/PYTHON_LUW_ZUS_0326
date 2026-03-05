from dataclasses import dataclass

@dataclass
class Student:
    name: str
    age: int
    field: str

    #dataclass z automatu na postawie wypisania powyższych pól tworzy konstruktory: init, repr, eq

s1 = Student("John", 20, "Computer Science")
s2 = Student("Anna", 21, "Economy")

print(s1)
print(s2)
print(s1 is s2)

class Car:
    def __init__(self, name, color):
        self.name = name
        self.color = color

c1 = Car("Tesla", "Red")
c2 = Car("BMW", "Black")
print(c1)
print(c2)

print(c1 is c2)
