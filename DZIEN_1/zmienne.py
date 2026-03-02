a = 5
print(a)
print(type(a))

b = a

print(type(b),b)
print(id(a),id(b))

c = 5

print(id(a),id(b),id(c))

a = 10
print(a,id(a))

a = "hej"

print(a,id(a))
