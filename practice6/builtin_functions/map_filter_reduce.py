from functools import reduce

print("=" * 50)
print("MAP()")
print("=" * 50)

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

squares = list(map(lambda x: x ** 2, numbers))
print(f"Original : {numbers}")
print(f"Squares  : {squares}")

str_nums = ["10", "20", "30", "40", "50"]
int_nums  = list(map(int, str_nums))
print(f"\nStrings  : {str_nums}")
print(f"Integers : {int_nums}")

celsius    = [0, 20, 37, 100]
fahrenheit = list(map(lambda c: round(c * 9/5 + 32, 1), celsius))
print(f"\nCelsius   : {celsius}")
print(f"Fahrenheit: {fahrenheit}")

a = [1, 2, 3, 4]
b = [10, 20, 30, 40]
sums = list(map(lambda x, y: x + y, a, b))
print(f"\na         : {a}")
print(f"b         : {b}")
print(f"a + b     : {sums}")

print("\n" + "=" * 50)
print("FILTER()")
print("=" * 50)

numbers = list(range(1, 21))

evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"All 1–20 : {numbers}")
print(f"Evens    : {evens}")

mixed    = [-3, -1, 0, 2, 5, -7, 8, 10]
positives = list(filter(lambda x: x > 0, mixed))
print(f"\nMixed    : {mixed}")
print(f"Positives: {positives}")

words = ["hi", "Python", "is", "great", "fun", "programming"]
long_words = list(filter(lambda w: len(w) > 3, words))
print(f"\nWords    : {words}")
print(f"len > 3  : {long_words}")

data   = [0, 1, "", "hello", None, 42, False, True, [], [1]]
truthy = list(filter(None, data))
print(f"\nRaw data : {data}")
print(f"Truthy   : {truthy}")

print("\n" + "=" * 50)
print("REDUCE()  (from functools)")
print("=" * 50)

nums = [1, 2, 3, 4, 5]

total = reduce(lambda acc, x: acc + x, nums)
print(f"Numbers  : {nums}")
print(f"Sum      : {total}")

product = reduce(lambda acc, x: acc * x, nums)
print(f"Product  : {product}")

values = [3, 1, 4, 1, 5, 9, 2, 6]
maximum = reduce(lambda a, b: a if a > b else b, values)
print(f"\nValues   : {values}")
print(f"Max      : {maximum}")

words = ["Python", "is", "awesome"]
sentence = reduce(lambda a, b: a + " " + b, words)
print(f"\nWords    : {words}")
print(f"Joined   : '{sentence}'")

nums   = [1, 2, 3, 4, 5]
result = reduce(lambda acc, x: acc + x, nums, 100)   # starts at 100
print(f"\nnums={nums}, initial=100 → sum={result}")


print("\n" + "=" * 50)
print("CHAINING  map + filter + reduce")
print("=" * 50)

data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

result = reduce(
    lambda acc, x: acc + x,          
    map(lambda x: x ** 2,            
        filter(lambda x: x % 2 == 0, data))  
)
print(f"Data             : {data}")
print(f"Evens            : {list(filter(lambda x: x % 2 == 0, data))}")
print(f"Squared evens    : {list(map(lambda x: x**2, filter(lambda x: x%2==0, data)))}")
print(f"Sum of sq evens  : {result}")

print("\n" + "=" * 50)
print("len / sum / min / max / sorted")
print("=" * 50)

scores = [88, 72, 95, 60, 83, 91, 77]
print(f"Scores  : {scores}")
print(f"Count   : {len(scores)}")
print(f"Sum     : {sum(scores)}")
print(f"Min     : {min(scores)}")
print(f"Max     : {max(scores)}")
print(f"Average : {sum(scores)/len(scores):.2f}")
print(f"Sorted ↑: {sorted(scores)}")
print(f"Sorted ↓: {sorted(scores, reverse=True)}")

words = ["banana", "fig", "apple", "cherry", "date"]
by_len = sorted(words, key=len)
print(f"\nWords by length: {by_len}")

nums = [2, 4, 6, 8]
print(f"\nall even in {nums}: {all(x % 2 == 0 for x in nums)}")
print(f"any > 5 in  {nums}: {any(x > 5 for x in nums)}")