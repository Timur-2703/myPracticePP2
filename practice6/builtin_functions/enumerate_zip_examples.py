print("=" * 50)
print("ENUMERATE()")
print("=" * 50)

fruits = ["apple", "banana", "cherry", "date", "elderberry"]

print("Basic enumerate (start=0):")
for index, fruit in enumerate(fruits):
    print(f"  {index}: {fruit}")

print("\nCustom start (start=1):")
for i, fruit in enumerate(fruits, start=1):
    print(f"  {i}. {fruit}")

print("\nMenu:")
for i, item in enumerate(["New Game", "Load Game", "Settings", "Quit"], 1):
    print(f"  [{i}] {item}")

print("\nItems with 'a' in name (with their index):")
for i, fruit in enumerate(fruits):
    if "a" in fruit:
        print(f"  Index {i}: {fruit}")

indexed = list(enumerate(fruits))
print(f"\nlist(enumerate(fruits)) = {indexed}")

print("\n" + "=" * 50)
print("ZIP()")
print("=" * 50)

names  = ["Alice", "Bob", "Carol", "Dave"]
scores = [92,      85,    78,      90]
grades = ["A",     "B",   "C+",    "A-"]

print("Names + Scores:")
for name, score in zip(names, scores):
    print(f"  {name}: {score}")

print("\nNames + Scores + Grades:")
for name, score, grade in zip(names, scores, grades):
    print(f"  {name:6} | {score:3} | {grade}")

short = [1, 2, 3]
long_ = ["a", "b", "c", "d", "e"]
print(f"\nzip({short}, {long_}):", list(zip(short, long_)))

from itertools import zip_longest
padded = list(zip_longest(short, long_, fillvalue="?"))
print(f"zip_longest:          {padded}")

zipped = list(zip(names, scores))
names_back, scores_back = zip(*zipped)
print(f"\nOriginal zipped : {zipped}")
print(f"Unzipped names  : {list(names_back)}")
print(f"Unzipped scores : {list(scores_back)}")

student_dict = dict(zip(names, scores))
print(f"\ndict(zip(names, scores)):\n  {student_dict}")

print("\nenumerate + zip:")
for i, (name, score) in enumerate(zip(names, scores), 1):
    print(f"  {i}. {name} scored {score}")

print("\n" + "=" * 50)
print("TYPE CHECKING")
print("=" * 50)

values = [42, 3.14, "hello", True, [1, 2], {"a": 1}, (1, 2), None]

print(f"{'Value':<15} {'type()':<15} {'isinstance check'}")
print("-" * 55)
for v in values:
    t = type(v).__name__
    is_num = isinstance(v, (int, float)) and not isinstance(v, bool)
    print(f"  {str(v):<13} {t:<15} is_numeric={is_num}")

x = True
print(f"\nbool is subclass of int: isinstance(True, int) = {isinstance(x, int)}")
print(f"type(True) == int  → {type(x) == int}   # False – prefer isinstance")

print("\n" + "=" * 50)
print("TYPE CONVERSION")
print("=" * 50)

print("int() conversions:")
print(f"  int('42')    = {int('42')}")
print(f"  int(3.99)    = {int(3.99)}   # truncates (not rounds)")
print(f"  int(True)    = {int(True)}")
print(f"  int('0b101', 2) = {int('0b101', 2)}  # binary string")

print("\nfloat() conversions:")
print(f"  float('3.14') = {float('3.14')}")
print(f"  float(7)      = {float(7)}")
print(f"  float('inf')  = {float('inf')}")

print("\nstr() conversions:")
print(f"  str(100)   = '{str(100)}'")
print(f"  str(3.14)  = '{str(3.14)}'")
print(f"  str(True)  = '{str(True)}'")
print(f"  str([1,2]) = '{str([1, 2])}'")

print("\nbool() conversions (falsy values):")
falsy = [0, 0.0, "", [], {}, (), None, False]
for v in falsy:
    print(f"  bool({repr(v):<10}) = {bool(v)}")

print("\nCollection conversions:")
t  = (1, 2, 3)
s  = {4, 5, 6}
l  = [7, 8, 9]
print(f"  list((1,2,3))  = {list(t)}")
print(f"  tuple([7,8,9]) = {tuple(l)}")
print(f"  set([1,1,2,3]) = {set([1,1,2,3])}")
print(f"  list('hello')  = {list('hello')}")

print("\n" + "=" * 50)
print("OTHER USEFUL BUILT-INS")
print("=" * 50)

print(f"abs(-7)        = {abs(-7)}")
print(f"round(3.7)     = {round(3.7)}")
print(f"round(3.14159, 2) = {round(3.14159, 2)}")
print(f"pow(2, 10)     = {pow(2, 10)}")
print(f"divmod(17, 5)  = {divmod(17, 5)}  # (quotient, remainder)")

print(f"\nlist(range(5))       = {list(range(5))}")
print(f"list(range(2, 10, 2))= {list(range(2, 10, 2))}")

nums = [5, 1, 4, 2, 3]
print(f"\nnums             = {nums}")
print(f"sorted()         = {sorted(nums)}")
print(f"list(reversed()) = {list(reversed(nums))}")

x = "hello"
print(f"\nid('hello')   = {id(x)}")
print(f"hash('hello') = {hash(x)}")