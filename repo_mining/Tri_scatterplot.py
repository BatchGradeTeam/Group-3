import csv
from collections import defaultdict
import matplotlib.pyplot as plt

# =========================
# CONFIGURATION
# =========================

# Input produced by the Tri_authorsFileTouches.py
INPUT_CSV = "data/file_touches.csv"

# Output the scatterplot
OUTPUT_PNG = "data/scatterplot.png"


# =========================
# MAIN LOGIC
# =========================

def main():
    # -------------------------
    # 1) Read data from CSV
    # -------------------------
    # We will store:
    # - a list of files (to assign each file a numeric file index)
    # - points grouped by author so each author can have a distinct color
    rows = []
    file_names = []
    seen_files = set()

    with open(INPUT_CSV, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            filename = row["Filename"]
            author = row["Author"]
            week = int(row["Week"])

            rows.append((filename, author, week))

            # Keep a stable list of unique file names (in first-seen order)
            if filename not in seen_files:
                seen_files.add(filename)
                file_names.append(filename)

    # -------------------------
    # 2) Map each file to an index
    # -------------------------
    # Scatter plot needs numeric x-values.
    # Map each file name to an integer
    file_to_index = {}
    for i, fname in enumerate(file_names):
        file_to_index[fname] = i

    # -------------------------
    # 3) Group points by author
    # -------------------------
    # Plot each author separately (distinct color per author).
    author_points = defaultdict(list)
    for filename, author, week in rows:
        x = file_to_index[filename]  # file index
        y = week                     # weeks since project start
        author_points[author].append((x, y))

    # -------------------------
    # 4) Plot
    # -------------------------
    # Create a color map with as many distinct colors as authors
    authors = list(author_points.keys())
    cmap = plt.get_cmap("tab20", len(authors))  # tab20 supports many distinct colors

    # One scatter call per author
    plt.figure()
    for i, author in enumerate(authors):
        points = author_points[author]
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        plt.scatter(xs, ys, color=cmap(i), label=author, s=12)


    # Axis labels
    plt.xlabel("File")
    plt.ylabel("Weeks")
    plt.title("Authors Activities over time")

    plt.legend(
        loc="upper right",
        fontsize=6,
        markerscale=0.6,
        handlelength=0.8,
        handletextpad=0.3,
        labelspacing=0.2,
        borderpad=0.3,
        frameon=True
    )

    # Tight layout to reduce overlapping labels
    plt.tight_layout()

    # -------------------------
    # 5) Save plot to file
    # -------------------------
    plt.savefig(OUTPUT_PNG)
    print(f"Saved plot to {OUTPUT_PNG}")


# Entry point
if __name__ == "__main__":
    main()
