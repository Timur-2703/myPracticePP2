with open("sample.txt", "w") as f:
    f.write("Hello, World!\n")
    f.write("This is a sample file.\n")
    f.write("Python file handling is easy.\n")

print("✅ File 'sample.txt' created and written.")

lines = [
    "Line 1: Apple\n",
    "Line 2: Banana\n",
    "Line 3: Cherry\n",
]

with open("fruits.txt", "w") as f:
    f.writelines(lines)

print("✅ File 'fruits.txt' created with writelines().")

with open("sample.txt", "a") as f:
    f.write("This line was appended.\n")
    f.write("So was this one!\n")

print("✅ Appended two lines to 'sample.txt'.")

print("\n📄 Contents of 'sample.txt' after appending:")
with open("sample.txt", "r") as f:
    print(f.read())

import os

filename = "new_file.txt"
if os.path.exists(filename):
    os.remove(filename)          

with open(filename, "x") as f:  
    f.write("Created exclusively with mode 'x'.\n")

print(f"✅ '{filename}' created with mode 'x'.")

students = [
    ("Alice", 90),
    ("Bob",   85),
    ("Carol", 92),
]

with open("students.txt", "w") as f:
    f.write("Name,Score\n")
    for name, score in students:
        f.write(f"{name},{score}\n")

print("✅ 'students.txt' written with structured data.")
print("\n📄 Contents of 'students.txt':")
with open("students.txt", "r") as f:
    print(f.read())