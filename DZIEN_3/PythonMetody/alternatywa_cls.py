class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @classmethod
    def from_string(cls,text):
        name,age=text.split(",")
        return cls(name,int(age))

pz = Person("Karol",60)
print(pz.name)
print(pz)

pp = Person.from_string("Jan,20")
print(pp)
