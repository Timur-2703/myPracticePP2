class Student:
    def __init__(self, name):
        self.name = name

    def show(self):
        print(self.name)

s = Student("Aida")
s.show()

class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def show(self):
        print(f"Name: {self.name}, Age: {self.age}")
s1 = Student("Aida", 20)
s2 = Student("Sanzhar", 22)
s1.show()
s2.show()
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def show(self):
        print(f"Name: {self.name}, Age: {self.age}")

s1 = Student("Aida", 20)
s2 = Student("Sanzhar", 22)
s1.show()
s2.show()
