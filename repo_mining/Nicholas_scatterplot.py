import matplotlib.pyplot as plt
import csv
from datetime import datetime
import os

repo_name = 'rootbeer' 
file_input = f'data/authorsFile_{repo_name}.csv'

if not os.path.exists(file_input):
    print(f"File {file_input} not found.")
    exit()

weeks_y = []
files_x = []
authors_c = []
file_names = []    
author_names = []  

contributor_stats = {}

with open(file_input, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    data = list(reader)

    if not data:
        print("CSV is empty.")
        exit()

    all_dates = [datetime.strptime(row['Date'], "%Y-%m-%dT%H:%M:%SZ") for row in data]
    start_date = min(all_dates)

    for i, row in enumerate(data):
        author = row['Author']
        date_obj = all_dates[i]

        if author not in contributor_stats:
            contributor_stats[author] = {'count': 0, 'last_commit': date_obj}
        
        contributor_stats[author]['count'] += 1
        if date_obj > contributor_stats[author]['last_commit']:
            contributor_stats[author]['last_commit'] = date_obj

        days_diff = (date_obj - start_date).days
        weeks_y.append(days_diff / 7) 

        fname = row['Filename']
        if fname not in file_names:
            file_names.append(fname)
        files_x.append(file_names.index(fname))

        if author not in author_names:
            author_names.append(author)
        authors_c.append(author_names.index(author))

print(f"\n{'Contributor':<25} | {'Commits':<8} | {'Last Commit Date'}")
print("-" * 60)
sorted_contributors = sorted(contributor_stats.items(), key=lambda x: x[1]['count'], reverse=True)

for name, stats in sorted_contributors:
    last_date_str = stats['last_commit'].strftime("%Y-%m-%d")
    print(f"{name:<25} | {stats['count']:<8} | {last_date_str}")
print("-" * 60 + "\n")

plt.figure(figsize=(12, 8)) 

for i, author in enumerate(author_names):
    mask = [auth_idx == i for auth_idx in authors_c]
    x_vals = [files_x[j] for j, val in enumerate(mask) if val]
    y_vals = [weeks_y[j] for j, val in enumerate(mask) if val]
    
    stats = contributor_stats[author]
    label_text = f"{author[:15]:<15} | {stats['count']:>3} commits | {stats['last_commit'].strftime('%Y-%m-%d')}"
    
    plt.scatter(x_vals, y_vals, s=40, label=label_text, edgecolors='none')

plt.xlabel('file')
plt.ylabel('weeks')
plt.title(f'Commit History: {repo_name}', loc='left', fontsize=14, pad=20)


plt.legend(
    title="Contributor | Commits | Last Date",
    bbox_to_anchor=(1.05, 1), 
    loc='upper left', 
    fontsize=9, 
    prop={'family': 'monospace'},
    frameon=True
)

plt.xlim(-1, max(files_x) + 1)
plt.ylim(-15, max(weeks_y) + 15)

plt.tight_layout()

plt.savefig(f'data/scatterplot_{repo_name}.png')
print(f"Plot saved as scatterplot_{repo_name}.png.")
plt.show()