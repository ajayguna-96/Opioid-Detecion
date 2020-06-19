import pandas as pd
import requests
import json
import csv
import time
import datetime
import os
import praw


def reddit_init():
    reddit = praw.Reddit(client_id="081KJhfxolnmRQ",
                     client_secret="4HcMIGNxK0LvHrbEXLESLVKtfAw",
                     password="r4AvZN9rdh8juHn",
                     user_agent="testscript by /u/Lucifer_1789",
                     username="Lucifer_1789")
    return reddit

def getPushshiftData(query, after, before, sub):
    print('Entered pushshift')

    itr = 0
    x = 0
    reddit = reddit_init()

    print('Entered looping')
    while True:
        objects = []
        url = 'https://api.pushshift.io/reddit/search/submission/?title='+str(query)+'&size=1000&after='+str(after)+'&before='+str(before)+'&subreddit='+str(sub)
        #print(url)
        print('Got url')
        r = requests.get(url)
        if len(r.text) == 0:
            break
        try:
            data = json.loads(r.text)
        except:
            break

        if len(data['data']) == 0:
            break
        print('Got data of length' , len(data['data']))
        for i,d in enumerate(data['data']):
            #print('Iterating' , i)
            d['comments'] = ''
            try:
                post = reddit.submission(url=d['url'])  # if you have the URL
                post.comments.replace_more(limit=None)
                for comment in post.comments.list():
                    d['comments'] = comment.body
            except:
                pass

            objects.append(d)
        print('Feteched comments')
        print(itr)
        after = objects[-1]['created_utc'] + 1
        itr = write_to_json(objects , itr , sub)
        print(after , 'batch ' + str(x) + ' done')
        x += 1
    return


def write_to_json(data , index , sub):
    newpath = '../../Data/Scrapper-Data/'+str(sub)
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    for item in (data):
        with open('../../Data/Scrapper-Data/'+str(sub)+'/post_'+str(index)+'.json', 'w') as json_file:
            json.dump(item, json_file)
            index += 1
    return index

if __name__ == "__main__":
    print('programming starting')
    #Subreddit to query
    #before and after dates
    before = "1590551838" #May 26 2020
    after = "1262329200"  #January 1 2010
    query = ""
    sub = ['Carfentanil']
    for reddit in sub:
        after = "1262329200"
        getPushshiftData(query, after, before, reddit)
