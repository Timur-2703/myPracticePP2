import os
import shutil

WORKSPACE = "workspace"
INBOX     = os.path.join(WORKSPACE, "inbox")
ARCHIVE   = os.path.join(WORKSPACE, "archive")
BACKUP    = os.path.join(WORKSPACE, "backup")

for d in (INBOX, ARCHIVE, BACKUP):
    os.makedirs(d, exist_ok=True)

sample_files = {
    "report_2024.txt":  "Annual report content.\n",
    "photo.jpg":        "fake jpg data\n",
    "data.csv":         "id,name,score\n1,Alice,90\n",
    "notes.txt":        "Meeting notes go here.\n",
    "script.py":        "print('hello')\n",
}

for fname, content in sample_files.items():
    with open(os.path.join(INBOX, fname), "w") as f:
        f.write(content)

print("✅ Workspace created. Inbox contents:")
for f in sorted(os.listdir(INBOX)):
    print(f"   {f}")
print()

# ── 1. Move a single file ─────────────────────────────────────────────────────
src  = os.path.join(INBOX, "report_2024.txt")
dest = os.path.join(ARCHIVE, "report_2024.txt")
shutil.move(src, dest)
print(f"📦 Moved  : {src} → {dest}")

src  = os.path.join(INBOX, "data.csv")
dest = os.path.join(BACKUP, "data_backup.csv")
shutil.copy2(src, dest)
print(f"📋 Copied : {src} → {dest}")

print("\n📂 Moving all .txt files to archive …")
for fname in os.listdir(INBOX):
    if fname.endswith(".txt"):
        src  = os.path.join(INBOX, fname)
        dest = os.path.join(ARCHIVE, fname)
        shutil.move(src, dest)
        print(f"   Moved: {fname}")

ARCHIVE_COPY = ARCHIVE + "_copy"
if os.path.exists(ARCHIVE_COPY):
    shutil.rmtree(ARCHIVE_COPY)
shutil.copytree(ARCHIVE, ARCHIVE_COPY)
print(f"\n🗂  Copied entire directory: '{ARCHIVE}' → '{ARCHIVE_COPY}'")

old_name = os.path.join(INBOX, "photo.jpg")
new_name = os.path.join(INBOX, "photo_renamed.jpg")
os.rename(old_name, new_name)
print(f"\n✏️  Renamed: photo.jpg → photo_renamed.jpg")

print("\n🗃  Organising remaining inbox files by extension …")
for fname in os.listdir(INBOX):
    fpath = os.path.join(INBOX, fname)
    if os.path.isfile(fpath):
        ext       = os.path.splitext(fname)[1].lstrip(".") or "no_ext"
        ext_dir   = os.path.join(INBOX, ext)
        os.makedirs(ext_dir, exist_ok=True)
        shutil.move(fpath, os.path.join(ext_dir, fname))
        print(f"   {fname}  →  {ext}/")

print("\n📁 Final workspace tree:")
for root, dirs, files in os.walk(WORKSPACE):
    level  = root.replace(WORKSPACE, "").count(os.sep)
    indent = "  " * level
    print(f"{indent}📁 {os.path.basename(root)}/")
    for f in files:
        print(f"{'  ' * (level + 1)}📄 {f}")

shutil.rmtree(WORKSPACE)
print(f"\n🗑  Cleaned up '{WORKSPACE}/'. Done.")