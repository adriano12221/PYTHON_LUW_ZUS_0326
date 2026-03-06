def morph(x):
    if x == 7:
        morph.__code__ = (lambda y: y*y + 1).__code__
    return x + 1

print(morph(2))   # 3
print(morph(7))   # 8  -> tu następuje mutacja
print(morph(2))   # 5  -> nowa architektura funkcji
print(morph(3))   # 10

def organism(x):

    if not hasattr(organism, "stage"):
        organism.stage = 0

    if x == 7 and organism.stage == 0:
        organism.__code__ = (lambda y: y*y).__code__
        organism.stage = 1

    elif x == 9 and organism.stage == 1:
        organism.__code__ = (lambda y: y**3 + 1).__code__
        organism.stage = 2

    return x + 1

print(organism(2))
print(organism(7))
print(organism(3))
print(organism(9))
print(organism(2))
