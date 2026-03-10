class Animal:
    def speak(self):
        print("Animal speaks")

class Dog(Animal):
    pass

d = Dog()
d.speak()

class Animal:
    def speak(self):
        print("Animal speaks")
class Dog(Animal):
    def bark(self):
        print("Dog barks")
d = Dog()
d.speak()
d.bark()
