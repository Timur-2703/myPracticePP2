class Car:
    wheels = 4  # class variable

    def __init__(self, brand):
        self.brand = brand  # instance variable

c1 = Car("BMW")
c2 = Car("Audi")

print(c1.wheels, c2.wheels)
print(c1.brand, c2.brand)

class Car:
    wheels = 4  # class variable

    def __init__(self, brand):
        self.brand = brand  # instance variable
c1 = Car("BMW")
c2 = Car("Audi")
print(c1.wheels, c2.wheels)
print(c1.brand, c2.brand)