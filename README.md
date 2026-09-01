# Dataset Download Website

Static site - no backend. A student types their SRN, the page hashes it
(`sha256(SALT + SRN)`) and downloads `d/<hash>.csv` as `trips.csv`.

There is no roster file served to the browser. `mapping.json` and the
raw `datasets/` folder are kept out of the deployed site, so a student
who opens dev tools cannot read the full SRN -> dataset assignment in one
place. This is not airtight: there are only 10 distinct dataset files, so
a determined student who collects several classmates' downloads can still
byte-compare them back to dataset numbers, and the SALT is visible in
`index.html`. For a real guarantee you need a server-side lookup.

## Layout

```
index.html          the page (HTML + CSS + JS, all in one file)
d/                   one <sha256(SALT+SRN)>.csv per student (deployed)
mapping.json         SRN -> dataset number, source of truth (NOT deployed)
datasets/            trips_1.csv .. trips_10.csv, the 10 fixed datasets (NOT deployed)
generate_mapping.py  regenerates mapping.json from the xlsx sheets (NOT deployed)
build_hashed.py      rebuilds d/ from mapping.json + datasets/
```

`mapping.json`, `datasets/`, and the generator scripts are listed in
`.gitignore` and are not pushed. Keep local backups of all three - they
are needed to rebuild `d/`.

## Rebuilding d/

Run this whenever `mapping.json` or a dataset file changes:

```
python build_hashed.py
```

It reads `mapping.json` + `datasets/`, wipes `d/`, and writes one file
per student. The SALT is defined at the top of both `build_hashed.py`
and `index.html` - if you change it, change it in both.

## Regenerating mapping.json

Only if the student list changes. Do NOT regenerate after sharing the
site - it reshuffles everyone's assigned dataset.

```
pip install openpyxl
python generate_mapping.py     # reads ../students/*.xlsx, writes mapping.json
python build_hashed.py         # then rebuild d/
```

Seed is fixed in the script, so re-running it unchanged reproduces the
exact same mapping.

## Hosting on GitHub Pages

The repo can stay private; the Pages site is served either way (private
Pages itself needs GitHub Enterprise, but a private repo with a public
Pages site is fine on the free plan).

1. Push `index.html` + `d/` to the `main` branch.
2. Repo -> Settings -> Pages -> Source -> "Deploy from a branch" ->
   Branch: `main`, folder: `/ (root)` -> Save.
3. Live at `https://<username>.github.io/<repo-name>/` in ~1-2 minutes.

To update: edit files, rebuild `d/` if needed, then

```
git add .
git commit -m "update"
git push
```

## Notes

- SRN lookup is case-insensitive and trims whitespace (input is
  uppercased before hashing, matching `build_hashed.py`).
- `d/` is ~39 MB (518 files). Well within GitHub Pages limits.
- `crypto.subtle` requires a secure context - works on `https://` and on
  `http://localhost`, not on a bare `file://` open.
- "SRN not found" means the SRN was not in the xlsx sheets when
  `mapping.json` was generated - check the source sheets.
