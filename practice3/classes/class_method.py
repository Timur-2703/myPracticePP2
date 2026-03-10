class Counter:
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1

c = Counter()
c.increment()
c.increment()
print(c.value)

class Counter:
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1
    def decrement(self):
        self.value -= 1
c1 = Counter()
c2 = Counter()
c1.increment()
c1.increment()  
print(c1.value)    