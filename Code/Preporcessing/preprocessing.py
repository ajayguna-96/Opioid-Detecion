import os
import pandas as pd
import json
from pandas.io.json import json_normalize
import re


def to_csv(sub):
    streetName = [sub , 'fent' , 'fet' , 'Apache', 'China Girl', 'China White', 'Dance Fever', 'Friend', 'Goodfellas', 'Jackpot', 'Murder 8', 'Tango & Cash']
    streetName = set(streetName)
    path = '../../Data/Scrapper-Data/' + sub + '/'
    data = pd.DataFrame()
    columns = ['author_fullname' , 'id' , 'created_utc', 'subreddit' , 'title', 'selftext','num_comments' , 'comments' ,'upvote_ratio' , 'score' , 'full_link' , 'does_contain']
    for index, js in enumerate(os.listdir(path)):
        json_file = open(os.path.join(path, js))
        jsonObj = json.loads(json_file.read())
        #print(jsonObj['selftext'])
        try:
            text = jsonObj['selftext']
            text = re.sub("[^A-Za-z0-9%,.?!:() ]", "" , text)
            jsonObj['selftext'] = text
            title = jsonObj['title']
            title = re.sub("[^A-Za-z0-9%,.?!:() ]", "" , title)
            jsonObj['title'] = title
            comment = jsonObj['comments']
            comment = re.sub("[^A-Za-z0-9%,.?!:() ]", "" , comment)
            jsonObj['comments'] = comment
            flag = True
            for word in jsonObj['selftext'].split(' '):
                for name in streetName:
                    if name.lower() in word.lower():
                        #print(word)
                        flag = False
                        jsonObj['does_contain'] = True
                        break
                if not flag:
                    break

            if flag:
                jsonObj['does_contain'] = False

        except Exception as e:
            print(e)
            jsonObj['does_contain'] = False
        df = json_normalize(jsonObj)
        #print(df)

        data = data.append(df , sort = False)
    data = data[columns]
    data['judgement'] = ''
    data.to_csv('../../Data/Scrapper-Data/'+sub+'.csv' , sep='\t')

if __name__ == "__main__":
    to_csv('fentanyl')
