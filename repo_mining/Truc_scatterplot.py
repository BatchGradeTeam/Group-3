# Script generates a scatter plot of weeks vs file,
# with points distinctly shaded according to author

import os
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime

# Get file, author, & date info from CSV file
currentDirectory = os.getcwd()
df = pd.read_csv(currentDirectory+"/data/file_authors_dates.csv")

# Convert the file & author info into a Series of CategoricalDType
file = df['Filename'].astype('category')
author = df['Author'].astype('category')

# Convert the ISO 8601 dates into datetime objects
date = [datetime.fromisoformat(d).strftime("%Y-%m-%d") for d in df['Date']]

# Convert dates into correct weeks with the earliest date being the start of Week 0
startDate = datetime.fromisoformat(date[-1])
weekNum = [(datetime.fromisoformat(d)-startDate).days // 7 for d in date]

# Ensure that distinct file & author names map to integer values
fileNum = file.cat.codes
authorNum = author.cat.codes

# Plot the scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(fileNum, weekNum, c=authorNum, cmap='tab20', s=20)
plt.subplots_adjust(left=0.07, bottom=0.1, right=0.85, top=0.92, wspace=0, hspace=0)
plt.title('Source File Touches by Author in the scottyab/rootbeer Repo')
plt.xlabel('File')
plt.ylabel('Weeks')
cbar = plt.colorbar()
cbar.set_ticks(authorNum)
cbar.set_ticklabels(author)
plt.show()
