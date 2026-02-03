# Script that collects the authors and the dates when they touched each file in the list of files generated
import json
import requests
import csv

import os
from datetime import datetime

if not os.path.exists("data"):
 os.makedirs("data")

# GitHub Authentication function
def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lstTokens)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        pass
        print(e)
    return jsonData, ct

repo = 'scottyab/rootbeer'
file = repo.split('/')[1]
inputCSV = 'data/file_' + file + '.csv'
lstTokens = [""]

dictFiles = dict()
with open(inputCSV, mode='r', newline='') as f:
    reader = csv.reader(f)
    next(reader)  # Skip first line
    
    dictFiles = dict()
    
    for row in reader:
        filename = row[0]
        dictFiles[filename] = []
        

ipage = 1  # url page counter
ct = 0  # token counter

while True:
    spage = str(ipage)
    commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
    jsonCommits, ct = github_auth(commitsUrl, lstTokens, ct)

    # break out of the while loop if there are no more commits in the pages
    if len(jsonCommits) == 0:
        break
    # iterate through the list of commits in  spage
    for shaObject in jsonCommits:
        sha = shaObject['sha']
        # For each commit, use the GitHub commit API to extract the files touched by the commit
        shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
        shaDetails, ct = github_auth(shaUrl, lstTokens, ct)
        
        
        filesjson = shaDetails['files']
                            
        for filenameObj in filesjson:
            filename = filenameObj['filename']
            
            if filename in dictFiles:
                author = shaDetails['commit']['author']['name']
                date = shaDetails['commit']['author']['date']
             
                week = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ").isocalendar()[1] # Need this for second script

                dictFiles[filename].append([author, date, week])
    
    ipage += 1
 
with open('data/file_' + file + '_touches.csv', mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['filename', 'author', 'date', 'week'])
    
    for filename in dictFiles:
        touches = dictFiles[filename]
        for touch in touches:
            author = touch[0]
            date = touch[1]
            week = touch[2]
            writer.writerow([filename, author, date, week])