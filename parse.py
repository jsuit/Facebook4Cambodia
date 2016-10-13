__author__ = 'jsuit'
# -*- coding: utf-8 -*-
import facebook
import pprint
import requests
import numpy as np
import json
import sys
from string import printable
reload(sys)
sys.setdefaultencoding('utf-8')
import time
import os.path
import matplotlib.pyplot as plt

fileName = open('posts.txt','r')

post_list = json.load(fileName)

def loadPosts():
    posts= {}
    for p in post_list:
        page = json.loads(p)
        for post in page:
            posts[post['created_time']] = post
    return posts

def wordCounts(posts):
    pass
#p=loadPosts()

#pprint.pprint(loadPosts())

def FilterOutKhmer(posts,FilterOnkey = 'message', id_key = 'id',save=True):
    data ={}
    if type(posts) == str:
        if os.path.exists(posts):
            return json.load(posts)
    for page in posts:
            #print posts[page]
            if FilterOnkey not in posts[page]:
               continue
            s = posts[page][FilterOnkey]
            eng = []
            khmer =[]
            for char in s:
                if char in printable:
                        eng.append(char)
                else:
                    khmer.append(char)

            e = ''.join(eng)
            k =  ''.join(khmer).encode('utf-8')

            data[page] ={'eng': e, 'kh': k, 'id': posts[page][id_key]}
    if save:
        f = open('posts_language.txt','w')
        json.dump(data,f,ensure_ascii=False,indent=4,sort_keys=True)
        f.close()
    return data

#data = FilterOutKhmer(p)

def saveWordsToFile(data,stopWords,language= 'eng',fileName='wordCloud'):
    if type(data) == str:
        data = open(data,'r')
        data = json.load(data)
    fileName+=(time.strftime("%H:%M:%S"))
    fileName += '.txt'
    f = open(fileName,'a')
    final_s = []
    print len(data)
    for d in data:
        #print data[d][language]
        s = data[d][language].split()
        for w in s:
            w = w.lower()
            if w not in stopWords and ('http:' not in w or 'https:' not in w):
                if w[-1] == "," or w[-1] == '.' or w[-1] == ';' or w[-1] =='?' or w[-1] == '"' or w[-1] == '!':
                    final_s.append(w[:-1])
                elif w[-3:] == 'ing':
                    final_s.append(w[:-3])
                elif w[-2:] == 'ed' or w[-2:] == "'s":
                    final_s.append(w[:-2])
                elif w.lower() == 'cambodian':
                    final_s.append('cambodia')
                else:
                    final_s.append(w)
    words = ' '.join(final_s)
    #f.write(' '.join(final_s))
    #f.close()
    return words
stopWords = set(['a','an','the', 'by', 'and', 'be','all', 'http:','https:' 'here', 'also', 'goo.gl', 'do', 'like,' 'below','my', 'go', 'or', 'according', 'likely', 'now','more',
                 'he', 'she,', 'you', "you'll", "will", "till", 'about', 'above', 'before', 'after','your', "you're", 'whom', 'who', 'whoever','it','its', 'itself', "it's",
                 "i",'they','cant',"can't", "cannot", "not", "i'd","i'm",'more', 'most', 'then','if','his', 'her,' 'hers', 'here', 'here is', "here's", 'while', 'which',
                 'so', 'therefore','in','that','for','on','with','as','you','do', 'at', 'this', 'but','from','we','say', 'said', 'told', 'my', 'all', 'their', 'what',
                 'out', 'about', 'when', 'just', 'know','into', 'onto,' 'than', 'only','these', 'because', 'after', 'some', 'them', 'mine', 'yours', "what's",'where','have',
                 'get','across','much','how', "how's",'has','was','are','afterwards',"couldn't", 'could', 'spoke','wrote', 'written','indeed','nor','once', 'perhaps','since',
                 'due to', 'something', 'somewhere', 'some','them', 'themselves','those','thus', 'too','upon','were',"weren't",'whether','whose', 'yet', 'corp'])

#words = saveWordsToFile('posts_language.txt',stopWords)

def getDistribution(wordsStr):
    dist ={}
    words = wordsStr.split()
    for word in words:
        if word in dist:
            dist[word] +=1
        else:
            dist[word] = 1
    v = dist.values()
    print dist['cambodia']
    Z = sum(v)

    values = np.array(v,dtype=float)
    return values/ Z

def plotD(dist):
    dist = np.sort(dist)
    dist[:] = dist[::-1]

    plt.loglog(np.arange(0,dist.shape[0],1), dist)
    #plt.bar(np.arange(0,dist.shape[0],1), dist,width=1/1.5)
    plt.show()


#plotD(getDistribution(words))

def generateListOfPostIds(file):
    if type(file) == str:
        data = open(file,'r')
        data = json.load(data)
    list =[]

    for page in data:
        page = json.loads(page,parse_int=True,parse_float=True)
        for d in page:
            print d['id']
            list.append(d['id'])
    json.dump(list,open('ListOfIds.txt','w'), indent=4)


generateListOfPostIds('posts.txt')

