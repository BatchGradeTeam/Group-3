import os
import time
import requests
import pandas as pd

# ----------------------------
# CONFIG
# ----------------------------
REPO = os.environ.get("REPO_FULL", "scottyab/rootbeer").strip()  # "owner/repo"
TOKEN = os.environ.get("GITHUB_TOKEN", "").strip()

# Define "source files" for the lab (mention these in your writeup)
SOURCE_EXTS = {
    ".py", ".java", ".c", ".cpp", ".h", ".hpp",
    ".js", ".ts", ".tsx", ".jsx",
    ".go", ".rb", ".rs", ".cs",
    ".php", ".swift", ".kt"
}

OUT_CSV = "data/file_rootbeer.csv"
WEEK_BUCKET = "W-MON"  # or "W-SUN"

os.makedirs("data", exist_ok=True)

if not TOKEN:
    raise SystemExit("Missing GITHUB_TOKEN. Set it in your environment (do not hardcode).")

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "repo-mining-lab"
}

# ----------------------------
# 1) Repo metadata -> default branch
# ----------------------------
repo_meta = requests.get(f"https://api.github.com/repos/{REPO}", headers=headers, timeout=30)
if repo_meta.status_code != 200:
    raise SystemExit(f"Repo metadata error {repo_meta.status_code}: {repo_meta.text[:400]}")

default_branch = repo_meta.json()["default_branch"]

# ----------------------------
# 2) Branch -> tree SHA
# ----------------------------
branch_meta = requests.get(f"https://api.github.com/repos/{REPO}/branches/{default_branch}", headers=headers, timeout=30)
if branch_meta.status_code != 200:
    raise SystemExit(f"Branch metadata error {branch_meta.status_code}: {branch_meta.text[:400]}")

tree_sha = branch_meta.json()["commit"]["commit"]["tree"]["sha"]

# ----------------------------
# 3) Tree listing -> source file paths
# ----------------------------
tree_resp = requests.get(
    f"https://api.github.com/repos/{REPO}/git/trees/{tree_sha}",
    headers=headers,
    params={"recursive": "1"},
    timeout=30
)
if tree_resp.status_code != 200:
    raise SystemExit(f"Tree error {tree_resp.status_code}: {tree_resp.text[:400]}")

paths = []
for item in tree_resp.json().get("tree", []):
    if item.get("type") == "blob":
        p = item.get("path", "")
        if p:
            pl = p.lower()
            if any(pl.endswith(ext) for ext in SOURCE_EXTS):
                paths.append(p)

paths = sorted(set(paths))
if not paths:
    raise SystemExit("No source files found. Adjust SOURCE_EXTS for your repo.")

print(f"Found {len(paths)} source files.")

# ----------------------------
# 4) For each file, list commits that touched it (event log rows)
# ----------------------------
rows = []
for i, file_path in enumerate(paths, start=1):
    print(f"[{i}/{len(paths)}] {file_path}")

    page = 1
    while True:
        r = requests.get(
            f"https://api.github.com/repos/{REPO}/commits",
            headers=headers,
            params={"path": file_path, "per_page": 100, "page": page},
            timeout=30
        )

        if r.status_code != 200:
            print(f"  API error {r.status_code} for {file_path}: {r.text[:200]}")
            break

        commits = r.json()
        if not isinstance(commits, list) or len(commits) == 0:
            break

        for c in commits:
            author = None
            if c.get("author") and c["author"].get("login"):
                author = c["author"]["login"]
            else:
                author = (c.get("commit", {}).get("author", {}) or {}).get("name", "unknown")

            date_utc = (c.get("commit", {}).get("author", {}) or {}).get("date", None)

            rows.append({
                "file_path": file_path,
                "commit_sha": c.get("sha"),
                "author": author,
                "date_utc": date_utc,
                "commit_html_url": c.get("html_url"),
            })

        if len(commits) < 100:
            break

        page += 1
        time.sleep(0.15)

touches = pd.DataFrame(rows)
if touches.empty:
    raise SystemExit("No touches collected. Check token access to repo and rate limits.")

# Parse dates and derive week buckets/index
touches["date_utc"] = pd.to_datetime(touches["date_utc"], utc=True, errors="coerce")
touches = touches.dropna(subset=["date_utc"]).copy()

touches["week_start"] = touches["date_utc"].dt.to_period(WEEK_BUCKET).dt.start_time
min_week = touches["week_start"].min()
touches["week_index"] = ((touches["week_start"] - min_week).dt.days // 7).astype(int)

touches.to_csv(OUT_CSV, index=False)
print(f"Saved {len(touches)} rows -> {OUT_CSV}")