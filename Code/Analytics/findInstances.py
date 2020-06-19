from fuzzywuzzy import fuzz
import collections
import matplotlib.pyplot as plt
import numpy as np
import os
import json
import re
import pandas as pd

def plot(subList, c_data, c_size, thr , drug ):
    width = 0.9
    base = np.arange(6)
    #plt.bar(base , counter, width = barWidth, label= 'No of posts with isotonitazene')
    #plt.legend()
    labels = subList
    #d1 = [c_size[sub] for sub in subList]
    d2 = [c_data[sub] - 1 for sub in subList]

    #plt.bar(base, d1 , width=width, color='b', label='Total Number of posts')
    plt.bar([i+0.25*width for i in base], d2, width=0.5*width, color='b', alpha=0.5, label='No of posts with isotonitazene')

    plt.xticks(base, subList , rotation='vertical' )
    plt.xlabel('Subreddit')
    plt.ylabel('Number of Posts')
    for i , key in enumerate(subList):
        plt.text(x = base[i] , y = c_data[key] - 1+0.9,s = c_data[key] - 1, size = 6)
        #plt.text(x = base[i] , y = c_size[key]+0.9,s = c_size[key], size = 6)
    #plt.subplots_adjust(bottom= 0.2, top = 0.98)
    #plt.figure(figsize=(20,10))
    plt.title("Occurance of isotonitazene in subreddit posts between 2010 to 2020 with threshold" + str(thr))
    plt.legend()
    my_path = '../../Data/Scrapper-Data/'
    plt.savefig(os.path.join(my_path,  drug + ' with threshold ' + str(thr) + '.png') , bbox_inches='tight')
def write_to_csv(data , filename):
    data.to_csv('../../Data/Scrapper-Data/'+filename+'.csv' , sep='\t')

def comparitor(subList , drug):

    c_size = collections.Counter(subList)
    threshold = [85]


    for thr in threshold:
        data = collections.defaultdict(set)
        c_data = collections.Counter(subList)
        #x = 0
        for sub in subList:
            path = '../../Data/Scrapper-Data/' + sub + '/'
            print(path)
            c_size[sub] = len(os.listdir(path))
            for index, js in enumerate(os.listdir(path)):
                with open(os.path.join(path, js)) as json_file:
                    json_text = json.load(json_file)
                    try:
                        text = json_text['selftext']
                        text = re.sub("[^A-Za-z0-9%,.?!:() ]", "" , text)
                    except Exception as e:
                        #print(e)
                        #x += 1
                        continue
                    for sentence in text.split('.'):
                        for word in sentence.split(' '):
                            #print(word)
                            if (fuzz.ratio(drug.lower(),word.lower()) > thr):
                                #print(word)
                                word = re.sub("[^A-Za-z]", "" , word)
                                data[word].add(sub)
                                c_data[sub] += 1
        # print(x)
        print(c_data)
        print(c_size)
        plot(subList, c_data , c_size , thr)
        d = []
        for key in data.keys():
            d.append([key , len(data[key]) , data[key]])
        df = pd.DataFrame(d)

        df.columns = ['word' , 'No of instances' , 'subreddits']
        write_to_csv(df , 'isotonitazene - ' + str(thr) )


if __name__ == "__main__":
    drug = 'iso'
    subList = ['fentanyl' , 'HeroinHeroines' , 'ObscureDrugs' , 'opiates' , 'OpiatesRecovery' , 'quittingkratom']
    #subList = ['fentanyl']
    comparitor(subList , drug)
