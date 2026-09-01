# Dataset Download Website

Static site - no backend, no server to run or maintain. A student types
their SRN, the page looks it up in `mapping.json`, and downloads the
matching `datasets/trips_<N>.csv` as `trips.csv`.

## Layout

```
index.html      the page (HTML + CSS + JS, all in one file)
mapping.json    SRN -> dataset number (1-10), for all 518 students
datasets/       trips_1.csv .. trips_10.csv (the 10 fixed datasets)
```

## Regenerating mapping.json

Only needed if the student list changes. Do NOT regenerate after sharing
the site with students - it reshuffles everyone's assigned dataset.

```
pip install openpyxl   # if not already installed
python3 generate_mapping.py
```
(`generate_mapping.py` isn't in this folder by default - copy it back in
if you need to regenerate; it reads both xlsx files from `../students/`
and writes `mapping.json` here. Seed is fixed in the script, so re-running
it unchanged reproduces the exact same mapping.)

## Hosting on GitHub Pages (free, ~5 minutes)

1. Create a new GitHub repo (public - GitHub Pages' free tier requires
   public repos unless you're on GitHub Pro/Enterprise).
2. From this folder:
   ```
   git init
   git add .
   git commit -m "dataset download site"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<repo-name>.git
   git push -u origin main
   ```
3. On GitHub: repo -> Settings -> Pages -> Source -> "Deploy from a
   branch" -> Branch: `main`, folder: `/ (root)` -> Save.
4. Wait ~1-2 minutes. Your site is live at:
   `https://<your-username>.github.io/<repo-name>/`
5. Share that URL with students.

To update later (e.g. you swap a dataset file): edit the file, then
```
git add .
git commit -m "update"
git push
```
GitHub Pages redeploys automatically in under a minute.

## Alternative: Netlify Drop (no git needed)

Go to https://app.netlify.com/drop and drag this whole folder into the
browser window. It gives you a live URL immediately
(`https://random-name.netlify.app`). No account strictly required for a
one-off drop, though creating a free account lets you update it later
instead of getting a new random URL each time.

## Notes

- Total size is under 1MB (10 CSVs + one HTML file) - well within any free
  host's limits, loads instantly.
- `mapping.json` is plain text fetchable by anyone who opens dev tools -
  there's nothing sensitive in it (just SRN -> a number 1-10), so this is
  fine for a static site with no backend.
- SRN lookup is case-insensitive and trims whitespace (input is
  uppercased before the mapping lookup).
- If a student reports "SRN not found", it means their SRN isn't in
  either PESU_RR_BD_STUDENTS.xlsx or PESU_EC_BD_STUDENTS.xlsx at the time
  mapping.json was generated - check the source sheets, not this site.
