import os
import shutil

SOURCE = "source.txt"
with open(SOURCE, "w") as f:
    f.write("This is the original source file.\n")
    f.write("It contains important data.\n")
print(f"✅ Created '{SOURCE}'.")

COPY = "source_copy.txt"
shutil.copy(SOURCE, COPY)
print(f"✅ Copied '{SOURCE}' → '{COPY}' using shutil.copy().")

COPY2 = "source_copy2.txt"
shutil.copy2(SOURCE, COPY2)
print(f"✅ Copied '{SOURCE}' → '{COPY2}' using shutil.copy2() (metadata preserved).")

BACKUP_DIR = "backup"
os.makedirs(BACKUP_DIR, exist_ok=True)
BACKUP_PATH = os.path.join(BACKUP_DIR, "source_backup.txt")
shutil.copy2(SOURCE, BACKUP_PATH)
print(f"✅ Backup saved to '{BACKUP_PATH}'.")

MOVED = "moved_source.txt"
shutil.move(COPY, MOVED)
print(f"✅ Moved (renamed) '{COPY}' → '{MOVED}'.")

print("\n📂 Current files:")
for fname in (SOURCE, COPY2, MOVED, BACKUP_PATH):
    status = "✔ exists" if os.path.exists(fname) else "✘ missing"
    print(f"  {fname}: {status}")

print("\n🗑  Deleting files safely …")
for fname in (COPY2, MOVED):
    if os.path.exists(fname):
        os.remove(fname)
        print(f"  Deleted '{fname}'.")
    else:
        print(f"  '{fname}' not found – skipping.")

if os.path.exists(BACKUP_DIR):
    shutil.rmtree(BACKUP_DIR)
    print(f"  Removed directory '{BACKUP_DIR}/' and all its contents.")

try:
    os.remove(SOURCE)
    print(f"  Deleted '{SOURCE}'.")
except FileNotFoundError:
    print(f"  '{SOURCE}' was already gone.")

print("\n✅ All done. Workspace cleaned up.")

example_path = "/home/user/documents/report.txt"
print("\n=== os.path utilities ===")
print(f"  Path        : {example_path}")
print(f"  dirname     : {os.path.dirname(example_path)}")
print(f"  basename    : {os.path.basename(example_path)}")
print(f"  splitext    : {os.path.splitext(example_path)}")
print(f"  isabs       : {os.path.isabs(example_path)}")
print(f"  join example: {os.path.join('/home/user', 'docs', 'file.txt')}")