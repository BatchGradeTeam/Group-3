# Script that generates a scatterplot (using matplotlib) of weeks vs file variables where the points are shaded according to author variable
import json
import requests
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import os
from datetime import datetime

if not os.path.exists("data"):
 os.makedirs("data")
 
repo = 'scottyab/rootbeer'
file = repo.split('/')[1]
inputCSV = 'data/file_' + file + '_touches.csv'

with open(inputCSV, mode='r', newline='') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header line
    
    data = []
    for row in reader:
        data.append(row)
        
# Preprocess data
fileNames = np.array(data)[:,0]
authors = np.array(data)[:,1]
weeksStr = np.array(data)[:, 3]
weeks = weeksStr.astype(int)

uniqueFiles, fileNumbers = np.unique(fileNames, return_inverse=True) # Convert file names to numbers
uniqueAuthors, authorNumbers = np.unique(authors, return_inverse=True) # Convert authors to numbers for colors

# Create scatterplot
plt.xticks(np.arange(0, len(uniqueFiles), 2))
plt.scatter(fileNumbers, weeks, c=authorNumbers, cmap='tab20')

# Add legend for authors
for i, author in enumerate(uniqueAuthors):
    plt.scatter([], [], color=plt.cm.tab20(i), label=author)

plt.legend(title="Author", bbox_to_anchor=(1, 1))

plt.ylabel('Weeks')
plt.xlabel('File')

plt.savefig('data/scatterplot_' + file, bbox_inches='tight')
