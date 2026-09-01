import hashlib, json, pathlib, shutil, sys

ROOT = pathlib.Path(r"C:\Desktop\bdta\A1\website")
SALT = "bdta-a1-2026-"  # ships in index.html too; friction only, not a secret

mapping = json.loads((ROOT / "mapping.json").read_text())
out = ROOT / "d"
if out.exists():
    shutil.rmtree(out)
out.mkdir()

count = 0
for srn, num in mapping.items():
    key = srn.strip().upper()
    h = hashlib.sha256((SALT + key).encode()).hexdigest()
    src = ROOT / "datasets" / f"trips_{num}.csv"
    shutil.copyfile(src, out / f"{h}.csv")
    count += 1

print(f"wrote {count} files to {out}")
# sanity: sample hash for the first SRN so we can curl-test it
first = next(iter(mapping))
print("sample", first, "->", hashlib.sha256((SALT + first.upper().strip()).encode()).hexdigest())
