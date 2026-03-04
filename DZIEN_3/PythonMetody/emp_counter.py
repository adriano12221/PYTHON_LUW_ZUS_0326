class Employee:

    count = 0

    def __init__(self,name):
        self.name = name
        Employee.count += 1

    @classmethod
    def how_many(cls):
        return cls.count


e1 = Employee("Karol")
e2 = Employee("Anna")
e3 = Employee("Ola")
e4 = Employee("Piotr")

print(Employee.how_many())
