class Fly:
    def ability(self):
        print("Can fly")

class Swim:
    def ability(self):
        print("Can swim")

class Duck(Fly, Swim):
    pass

d = Duck()
d.ability()

class Fly:
    def ability(self):
        print("Can fly")
class Swim:
    def ability(self):
        print("Can swim")
class Duck(Fly, Swim):
    pass
d = Duck()
d.ability()