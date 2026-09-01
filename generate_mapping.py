import json
import random
import openpyxl

FILES = [
    "/home/shrivardhan/A1/BD_A1/students/PESU_RR_BD_STUDENTS.xlsx",
    "/home/shrivardhan/A1/BD_A1/students/PESU_EC_BD_STUDENTS.xlsx",
]
NUM_DATASETS = 10
SEED = 20260901  # fixed - do not change once shared, or students' assignments shift

srns = []
for f in FILES:
    wb = openpyxl.load_workbook(f)
    ws = wb["Name-SRN"]
    for name, srn in ws.iter_rows(min_row=2, values_only=True):
        if srn:
            srns.append(srn.strip().upper())

assert len(srns) == len(set(srns)), "duplicate SRN across campuses!"

rng = random.Random(SEED)
shuffled = srns[:]
rng.shuffle(shuffled)

mapping = {srn: (i % NUM_DATASETS) + 1 for i, srn in enumerate(shuffled)}

from collections import Counter
counts = Counter(mapping.values())

with open("/home/shrivardhan/A1/BD_A1/dataset_website/mapping.json", "w") as fh:
    json.dump(mapping, fh, indent=0, sort_keys=True)

print("total students:", len(mapping))
print("per-dataset counts:", dict(sorted(counts.items())))
