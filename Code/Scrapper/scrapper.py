import pandas as pd
import requests
import json
import csv
import time
import datetime

def getPushshiftData(query, after, before, sub):
    url = 'https://api.pushshift.io/reddit/search/submission/?title='+str(query)+'&size=1000&after='+str(after)+'&before='+str(before)+'&subreddit='+str(sub)
    print(url)
    r = requests.get(url)
    data = json.loads(r.text)
    return data['data']

def write_to_json(data):
    for i , item in enumerate(data):
        with open('../../Data/Scrapper-Data/entry_'+str(i+1)+'.json', 'w') as json_file:
            json.dump(item, json_file)

if __name__ == "__main__":
    
    #Subreddit to query
    sub='LifeLessonLearnedLate'
    #before and after dates
    before = "1590551838" #May 26 2020
    after = "1262329200"  #January 1 2010
    query = ""
    subCount = 0
    subStats = {}

    data = getPushshiftData(query, after, before, sub)
    write_to_json(data)