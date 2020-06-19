import os
import json
import matplotlib.pyplot as plt
import numpy as np
import collections
import pandas as pd
import json
from pandas.io.json import json_normalize


def plot(counter , sub):
    barWidth = 0.9
    base = np.arange(11)
    plt.bar(base , counter, width = barWidth, label= 'Posts per year')
    plt.legend()
    labels = [str(i) for i in range(2010 , 2021)]
    plt.xticks(base , labels , rotation=90)
    plt.xlabel('Years')
    plt.ylabel('Number of Posts')
    for i in range(len(counter)):
        plt.text(x = base[i] , y = counter[i]+0.9,s = counter[i], size = 6)
    #plt.subplots_adjust(bottom= 0.2, top = 0.98)
    #plt.figure(figsize=(20,10))
    plt.title("r/"+sub+" posts between 2010 to 2020 \n Total Number of posts = "+ str(sum(counter)))
    my_path = '../../Data/Scrapper-Data/'
    plt.savefig(os.path.join(my_path, sub + '.png') , bbox_inches='tight')

def print_growth(sub):
    path = '../../Data/Scrapper-Data/' + sub + '/'
    print(path)
    counter = [0 for i in range(11)]

    c = collections.Counter()
    for index, js in enumerate(os.listdir(path)):
        #print(js)
        with open(os.path.join(path, js)) as json_file:
            json_text = json.load(json_file)
            c[index] = 1
            time = json_text['created_utc']
            if 1262329200 <= time < 1293840000:
                counter[0] += 1
            elif 1293840000 <= time < 1325376000:
                counter[1] += 1
            elif 1325376000 <= time < 1356998400:
                counter[2] += 1
            elif 1356998400 <= time < 1388534400:
                counter[3] += 1
            elif 1388534400 <= time < 1420070400:
                counter[4] += 1
            elif 1420070400 <= time < 1451606400:
                counter[5] += 1
            elif 1451606400 <= time < 1483228800:
                counter[6] += 1
            elif 1483228800 <= time < 1514764800:
                counter[7] += 1
            elif 1514764800 <= time < 1546300800:
                counter[8] += 1
            elif 1546300800 <= time < 1577836800:
                counter[9] += 1
            else:
                counter[10] += 1
    plot(counter , sub)

#print_growth('fentanyl')
#print_growth('OpiatesRecovery')
