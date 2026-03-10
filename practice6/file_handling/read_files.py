import os

DEMO_FILE = "demo.txt"

with open(DEMO_FILE, "w") as f:
    f.write("First line\n")
    f.write("Second line\n")
    f.write("Third line\n")
    f.write("Fourth line\n")
    f.write("Fifth line\n")

print("=== read() ===")
with open(DEMO_FILE, "r") as f:
    content = f.read()
print(content)

print("=== read(12) – first 12 characters ===")
with open(DEMO_FILE, "r") as f:
    print(repr(f.read(12)))
print()

print("=== readline() ===")
with open(DEMO_FILE, "r") as f:
    print("Line 1:", repr(f.readline()))
    print("Line 2:", repr(f.readline()))
print()

print("=== readlines() ===")
with open(DEMO_FILE, "r") as f:
    lines = f.readlines()
print(lines)
print(f"Total lines: {len(lines)}")
print()

print("=== Iterating line by line ===")
with open(DEMO_FILE, "r") as f:
    for i, line in enumerate(f, start=1):
        print(f"  [{i}] {line.rstrip()}")
print()

print("=== tell() and seek() ===")
with open(DEMO_FILE, "r") as f:
    f.read(5)
    print(f"Position after read(5): {f.tell()}")
    f.seek(0)                          # go back to the start
    print(f"Position after seek(0): {f.tell()}")
    print("First char again:", repr(f.read(1)))
print()

print("=== Safe read with os.path.exists() ===")
for fname in (DEMO_FILE, "missing.txt"):
    if os.path.exists(fname):
        with open(fname, "r") as f:
            first = f.readline().rstrip()
        print(f"  '{fname}' found. First line: '{first}'")
    else:
        print(f"  '{fname}' does not exist – skipping.")

os.remove(DEMO_FILE)
print("\n✅ Demo file removed. Done.")