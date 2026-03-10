import os

print("=== Current Working Directory ===")
cwd = os.getcwd()
print(f"  os.getcwd() → {cwd}\n")

DIR = "my_project"
os.makedirs(DIR, exist_ok=True)
print(f"✅ Created directory: '{DIR}'")

nested = os.path.join(DIR, "src", "utils")
os.makedirs(nested, exist_ok=True)
print(f"✅ Created nested directories: '{nested}'")

data_dir = os.path.join(DIR, "data", "raw")
os.makedirs(data_dir, exist_ok=True)
print(f"✅ Created nested directories: '{data_dir}'")

logs_dir = os.path.join(DIR, "logs")
os.makedirs(logs_dir, exist_ok=True)
print(f"✅ Created nested directories: '{logs_dir}'")

files_to_create = [
    os.path.join(DIR, "README.md"),
    os.path.join(DIR, "src", "main.py"),
    os.path.join(DIR, "src", "utils", "helper.py"),
    os.path.join(DIR, "data", "raw", "data.csv"),
    os.path.join(DIR, "data", "raw", "notes.txt"),
    os.path.join(DIR, "logs", "app.log"),
]

for fpath in files_to_create:
    with open(fpath, "w") as f:
        f.write(f"# {os.path.basename(fpath)}\n")

print(f"\n✅ Created {len(files_to_create)} sample files inside '{DIR}/'.\n")

print(f"=== os.listdir('{DIR}') ===")
for item in sorted(os.listdir(DIR)):
    full = os.path.join(DIR, item)
    kind = "DIR " if os.path.isdir(full) else "FILE"
    print(f"  [{kind}] {item}")
print()

print(f"=== os.walk('{DIR}') – full tree ===")
for root, dirs, files in os.walk(DIR):
    level = root.replace(DIR, "").count(os.sep)
    indent = "  " * level
    print(f"{indent}📁 {os.path.basename(root)}/")
    sub_indent = "  " * (level + 1)
    for file in files:
        print(f"{sub_indent}📄 {file}")
print()

print("=== Find all .py files ===")
for root, dirs, files in os.walk(DIR):
    for file in files:
        if file.endswith(".py"):
            print(f"  {os.path.join(root, file)}")
print()

print("=== Find all .txt and .csv files ===")
for root, dirs, files in os.walk(DIR):
    for file in files:
        if file.endswith((".txt", ".csv")):
            print(f"  {os.path.join(root, file)}")
print()

sample = os.path.join(DIR, "data", "raw", "data.csv")
print("=== os.path checks ===")
print(f"  exists  : {os.path.exists(sample)}")
print(f"  isfile  : {os.path.isfile(sample)}")
print(f"  isdir   : {os.path.isdir(os.path.join(DIR, 'data'))}")
print(f"  size    : {os.path.getsize(sample)} bytes")
print()

print("=== os.chdir() demo ===")
print(f"  Before chdir: {os.getcwd()}")
os.chdir(DIR)
print(f"  After  chdir: {os.getcwd()}")
os.chdir("..")                          
print(f"  After  cd ..: {os.getcwd()}")
print()

import shutil
shutil.rmtree(DIR)
print(f"🗑  Removed '{DIR}/' and all contents. Done.")