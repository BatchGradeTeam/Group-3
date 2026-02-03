import os
import pandas as pd
import matplotlib.pyplot as plt

IN_CSV = "data/file_rootbeer.csv"
OUT_PNG = "data/scatterplot.png"
os.makedirs("data", exist_ok=True)

df = pd.read_csv(IN_CSV)
if df.empty:
    raise SystemExit("file_touches.csv is empty.")

# Ensure needed columns exist
needed = {"week_index", "file_path", "author"}
missing = needed - set(df.columns)
if missing:
    raise SystemExit(f"Missing columns in CSV: {missing}")

df["week_index"] = df["week_index"].astype(int)
df["file_path"] = df["file_path"].astype(str)
df["author"] = df["author"].astype(str)

# Encode categorical axes/colors
df["file_id"] = df["file_path"].astype("category").cat.codes
df["author_id"] = df["author"].astype("category").cat.codes

# Save mappings (useful for report / interpreting plot)
df[["author_id", "author"]].drop_duplicates().sort_values("author_id").to_csv("data/author_id_map.csv", index=False)
df[["file_id", "file_path"]].drop_duplicates().sort_values("file_id").to_csv("data/file_id_map.csv", index=False)

plt.figure(figsize=(12, 7))
sc = plt.scatter(
    df["week_index"],
    df["file_id"],
    c=df["author_id"],
    s=16,
    alpha=0.8
)

plt.title("File touches over time (colored by author)")
plt.xlabel("Week index (0 = earliest week)")
plt.ylabel("File (categorical id)")

cbar = plt.colorbar(sc)
cbar.set_label("Author (categorical id)")

plt.tight_layout()
plt.savefig(OUT_PNG, dpi=200)
plt.show()

print(f"Saved scatterplot -> {OUT_PNG}")
print("Mappings saved -> data/author_id_map.csv and data/file_id_map.csv")
