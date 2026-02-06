class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name, university):
        super().__init__(name)
        self.university = university

s = Student("Timur", "KBTU")
print(s.name, s.university)


class Person:
    def __init__(self, name):
        self.name = name
class Student(Person):
    def __init__(self, name, university):
        super().__init__(name)
        self.university = university
s1 = Student("Aida", "KIMEP")
s2 = Student("Sanzhar", "Nazarbayev University")
print(s1.name, s1.university)
print(s2.name, s2.university)