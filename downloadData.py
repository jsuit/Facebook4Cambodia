# -*- coding: utf-8 -*-
import facebook
import pprint
import requests
import json
import sys
import Globals
reload(sys)
sys.setdefaultencoding('utf8')
import gettext
import string
import collections
import os.path
import matplotlib.ticker as ticker
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from time import strptime
import numpy as np
class GraphAPI():

    access_token = Globals.access_token
    user = Globals.user
    def __init__(self, version='2.7'):
       self.version=version
       self.graph = facebook.GraphAPI(GraphAPI.access_token, version=version)
       self.profile = self.graph.get_object(GraphAPI.user)
       self.ListOfIds = open('ListOfIds.txt','r') #postIds

    def downloadPosts(self):
        posts = self.graph.get_connections(self.profile['id'], 'posts')
        return posts



    def getCommentsForPost(self,postId):

        comments = self.graph.get_connections(id=postId, connection_name='comments')
        print comments
        data = {}
        data[postId] = []
        while True:
            try:
                s = json.dumps(comments['data'],ensure_ascii=False,indent=4)
                if len(s) > 2:
                    data[postId].append(s.decode('utf-8'))
                comments = requests.get(comments['paging']['next']).json()
            except KeyError:
               return data[postId]

    def getAllComments(self):
        ids = json.load(self.ListOfIds)
        data={}
        print len(ids)
        for i,id in enumerate(ids):
            print i
            data[id] = self.getCommentsForPost(id)
        return data

    def saveToFile(self,fileName,data):
         json.dump(data,open(fileName,'a'),ensure_ascii=False,indent=4)

    def countComments(self, comments_file):
        comments=json.load(open(comments_file,'r'))
        s = 0
        for id in comments:
            cmtList = comments[id]
            for i in cmtList:
                cmts = json.loads(i)
                s+= len(cmts)
        return s
    def writeLikeNumToFile(self, fileName):
        f = open(fileName,'r')
        data = json.load(f)
        Likes = {}
        for page in data:
            page = json.loads(page)
            for post in page:
              count = self.getNumLikesForPost(post['id'])
              Likes[post['id']] = count

        json.dump(Likes,open('LikesForPost.txt','w'))

    def numCommentsForPost(self,postID,comments_file):
        comments=json.load(comments_file)
        return len(comments[postID])
    def getSharesPerPost(self,postID):
         r = requests.get('https://graph.facebook.com/v2.8/'+ postID +'/?fields=shares&access_token='+Globals.access_token)
         txt = r.json()
         if 'shares' not in txt:
             print txt
             return 0
         return  txt['shares']['count']
    def getNumShares(self):
        f = open('posts.txt')
        data = json.load(f)
        Shares = {}
        for page in data:
            page = json.loads(page)
            for post in page:
                Shares[post['id']]=self.getSharesPerPost(post['id'])
        json.dump(Shares,open('SharesForPost.txt','w'))
    def getNumReactionsForPost(self,postId):

        r = requests.get('https://graph.facebook.com/v2.8/'+ postId +'/?fields=reactions.summary(1).limit(1)&access_token='+Globals.access_token)
        #reactions = self.graph.get_connections(id=postId, connection_name='reactions',args={'fields': 'summary=1','total_count':1})
        #print r.text
        txt = r.json()
        if 'reactions' not in txt:
            return 0
        return  txt['reactions']['summary']['total_count']


    def getNumLikesForPost(self, postID):
        reqString = "https://graph.facebook.com/v2.8/" +postID + '/?fields=likes.summary(true).limit(1)&access_token=' + Globals.access_token
        r = requests.get(reqString)
        txt = r.json()
        if 'likes' not in txt:
            return 0
        return  txt['likes']['summary']['total_count']


    def numberOfKindOfChar(self, fileName,searchFor="?"):
        saveFileName = 'contains'+searchFor+'.txt'
        count = 0
        total = 0
        rFile = open(fileName,'r')
        posts = json.load(rFile)
        rFile.close()
        likesForSearchFor ={}
        for page in posts:
            page = json.loads(page)
            for post in page:
                total+=1
                if 'message' in post:
                    txt = set(post['message'])
                    if searchFor in txt:
                        count+=1
                        id = post['id']
                        likesForSearchFor[id] = self.getNumLikesForPost(id)
        f = open(saveFileName,'w')
        json.dump(likesForSearchFor,f)
        print 'count = {}, total ={}, total-count = {},count/total ={}'.format( count,total, total-count,float(count)/total)
        f.close()

    def timesXIsMentioned(self,fileName,X,saveFileName):
        punctuation = set(string.punctuation)
        if len(X) == 0: return
        if type(X) == str:
            X=[X]
            X = set(X)
        elif type(X) == list:
            X = set(X)
        assert type(X) == set
        counts = {}

        rFile = open(fileName,'r')
        posts = json.load(rFile)
        rFile.close()
        for page in posts:
            page = json.loads(page)
            for post in page:
                if 'message' in post:

                    txt = post['message'].lower().split()
                    for c,word in enumerate(txt):
                        word = word.strip()
                        word2 =''
                        if word[-1] in punctuation:
                            word = word[:-1]
                        if c + 1 < len(txt):
                            word2 = txt[c+1]
                            word2 = word2.strip()
                            if word2[-1] in punctuation:
                                word2 = word2[:-1]
                        if  word + ' ' + word2 in X:
                             if post['id'] not in counts:
                                 counts[post['id']] ={}
                                 counts[post['id']][word + ' ' + word2]= 1
                             else:
                                if word not in counts[post['id']]:
                                   counts[post['id']][ word + ' ' + word2] =1
                                else:
                                   counts[post['id']][ word + ' ' + word2]+=1
                        elif word in X:
                            if post['id'] not in counts:
                                 counts[post['id']] ={}
                                 counts[post['id']][word] =1
                            else:
                                if word not in counts[post['id']]:
                                   counts[post['id']][word] =1
                                else:
                                   counts[post['id']][word]+=1


        print counts
        f = open(saveFileName,'w')
        json.dump(counts,f)

    def getLikesForPostsInOrderOfDate(self,fileName):
        rFile = open(fileName,'r')
        posts = json.load(rFile)
        rFile.close()
        mostLikedID ={}
        for page in posts:
            page = json.loads(page)
            for post in page:
                count = self.getNumLikesForPost(post['id'])
                if count > 0:
                    cDate = post['created_time'][0:-5]
                    #print datetime(*strptime(post['created_time'][0:-5], "%Y-%m-%dT%H:%M:%S")[0:6])
                    if cDate not in mostLikedID:
                        mostLikedID[cDate] = count
                    else:
                        mostLikedID[cDate]+=count


        sortedLikes = collections.OrderedDict(sorted(mostLikedID.items()))
        print 'done looping'
        f= open('likesByDate.txt','w')
        json.dump(sortedLikes,f,indent=4)
        print 'Done saving'
        f.close()
        return sortedLikes

    def graphLikes(self, sortedDict=None, fileName="likesByDate.txt"):

        if sortedDict == None:
            f =  open(fileName, 'r')
            sortedDict = json.load(f)

            tempDict = collections.OrderedDict()
            sortedDict = collections.OrderedDict(sorted(sortedDict.items()))

            for key in sortedDict:
                    tempDict[key[0:10]] = sortedDict[key]

        dates = np.arange(len(tempDict.keys()))
        print len(dates)
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        #major_ticks = np.arange(0, len(dates), 100)
        #ax.set_xticks(major_ticks)
        #with plt.style.context('fivethirtyeight'):
        plt.plot(dates, tempDict.values(),color='b')
        plt.xticks(dates[::100], tempDict.keys()[::100])
        plt.xticks(rotation=75)
        plt.tight_layout()


        plt.show()
    def movingAverageWithTotal(self,fileName, window = 5):
            f = open(fileName,'r')
            likes = json.load(f)
            f.close()
            tempDict = collections.OrderedDict()
            likes = collections.OrderedDict(sorted(likes.items()))

            for key in likes:
               key2 = key[0:10]
               tempDict[key2] = likes[key]
            df = pd.DataFrame(tempDict.items(),columns=['Date', 'Total Likes'],index=tempDict.keys())
            rolling = pd.rolling_mean(df, window)
            rolling.columns=['Date', 'Mean Likes']
            ax = df.plot(x_compat=True, color=["g"])
            ax.set_ylabel("Likes")
            rolling.plot( ax=ax, style="b-")

            #ax = df_mean.plot()
            ticks = ax.xaxis.get_ticklocs()
            ticklabels = [l.get_text() for l in ax.xaxis.get_ticklabels()]
            #print len(ticklabels)
            ax.xaxis.set_ticks(ticks[::])
            ax.xaxis.set_ticklabels(ticklabels[::],rotation=75)
            plt.tight_layout()
            ax.lines[-1].set_linewidth(5)
            plt.show()
    def movingAverage(self,fileName, window = 5):
            f = open(fileName,'r')
            likes = json.load(f)
            f.close()
            tempDict = collections.OrderedDict()
            likes = collections.OrderedDict(sorted(likes.items()))
            for key in likes:
               key2 = key[0:10]
               tempDict[key2] = likes[key]
            df = pd.DataFrame(tempDict.items(),columns=['Date', 'Total Likes'],index=tempDict.keys())
            rolling = pd.rolling_mean(df, window)
            rolling.columns=['Date', 'Mean Likes']
            ax = rolling.plot(title='Rolling Mean with Window = '+ str(window))
            ax.set_ylabel("Likes")

            #ax = df_mean.plot()
            ticks = ax.xaxis.get_ticklocs()
            ticklabels = [l.get_text() for l in ax.xaxis.get_ticklabels()]
            #print len(ticklabels)
            ax.xaxis.set_ticks(ticks[::])
            ax.xaxis.set_ticklabels(ticklabels[::],rotation=75)

            plt.tight_layout()
            ax.lines[-1].set_linewidth(1)
            plt.show()

    def rollingStd(self,fileName,window=10):
            f = open(fileName,'r')
            likes = json.load(f)
            f.close()
            tempDict = collections.OrderedDict()
            likes = collections.OrderedDict(sorted(likes.items()))
            for key in likes:
               key2 = key[0:10]
               tempDict[key2] = likes[key]
            df = pd.DataFrame(tempDict.items(),columns=['Date', 'Total Likes'],index=tempDict.keys())
            rolling = pd.rolling_std(df, window)
            rolling.columns=['Date', 'Rolling STD of Likes']
            ax = rolling.plot(title='Rolling Mean with Window = '+ str(window))
            ax.set_ylabel("Likes")
            ticks = ax.xaxis.get_ticklocs()
            ticklabels = [l.get_text() for l in ax.xaxis.get_ticklabels()]
            #print len(ticklabels)
            ax.xaxis.set_ticks(ticks[::])
            ax.xaxis.set_ticklabels(ticklabels[::],rotation=75)
            plt.tight_layout()
            ax.lines[-1].set_linewidth(1)
            plt.show()
    def percentGain(self,fileName):
            f = open(fileName,'r')
            likes = json.load(f)
            f.close()
            tempDict = collections.OrderedDict()
            count = 3200
            likes = collections.OrderedDict(sorted(likes.items()))
            for i,key in enumerate(likes):
                if i>count:
                    key2 = key[0:10]
                    tempDict[key2] = likes[key]
            df = pd.DataFrame(tempDict.items(),columns=['Date', 'Total Likes'],index=tempDict.keys())
            #print df['Total Likes']
            df = pd.to_numeric(df['Total Likes'])
            df = df/df.ix[0]
            ax = df.plot()
            #daily_rets = df[:] / df.shift(1) -1
            ax.set_ylabel("% Increase in Likes")
            #ticks = ax.xaxis.get_ticklocs()
            ticklabels = [l.get_text() for l in ax.xaxis.get_ticklabels()]
            #print len(ticklabels)
            #ax.xaxis.set_ticks(ticks[::])
            ax.xaxis.set_ticklabels(ticklabels[::],rotation=75)
            plt.tight_layout()
            ax.lines[-1].set_linewidth(1)
            plt.show()
            #print daily_rets

    def SharesOverTime(self,fileName):
        rFile = open(fileName,'r')
        posts = json.load(rFile)
        rFile.close()
        sharesDict ={}
        s_count = float('-inf')
        s_date =None
        shares = json.load(open("SharesForPost.txt",'r'))
        for page in posts:
            page = json.loads(page)
            for post in page:
                count = shares[post['id']]
                if count > 0:
                    cDate = post['created_time'][0:10]
                    #print datetime(*strptime(post['created_time'][0:-5], "%Y-%m-%dT%H:%M:%S")[0:6])
                    if cDate not in sharesDict:
                        sharesDict[cDate] = count
                    else:
                        sharesDict[cDate]+=count

                if s_count < sharesDict[cDate] and cDate != '2016-06-10':
                    s_count = sharesDict[cDate]
                    s_date = cDate

        sharesDict = collections.OrderedDict(sorted(sharesDict.items()))
        tempDict = collections.OrderedDict()
        for i in sharesDict:
                tempDict[i[0:10]] = sharesDict[i]

        dates = np.arange(len(tempDict.keys()))

        print len(dates)
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        #major_ticks = np.arange(0, len(dates), 100)
        #ax.set_xticks(major_ticks)
        #with plt.style.context('fivethirtyeight'):
        plt.barh(dates,tempDict.values(),color='g',align='center')
        plt.yticks(dates[::90], tempDict.keys()[::90])
        #plt.xticks(rotation=75)
        plt.tight_layout()
        plt.show()

    def getSharesOnDay(self,fileName,date):
        rFile = open(fileName,'r')
        posts = json.load(rFile)
        rFile.close()
        sharesDict ={}
        s_count = float('-inf')
        s_date =None
        shares = json.load(open("SharesForPost.txt",'r'))
        for page in posts:
            page = json.loads(page)
            for post in page:
                time = post['created_time'][0:10]
                if time == date:
                    print post['id'],post,shares[post['id']]
graph = GraphAPI()
#comments = graph.getAllComments()
#graph.saveToFile('all_comments.txt',comments)
#r = graph.getNumLikesForPost('79770243223_10154089375478224')
#print r
graph.getSharesOnDay('posts.txt','2016-07-11' )
provinces = ['phnom penh', 'banteay meanchey', 'battambang','kampong cham', 'kampong chhang','kampong thom', 'kampot province', 'kandal', 'koh kong',
             'kep', 'kratié', 'kratie','mondulkiri', 'oddary meanchev', 'pailin', 'preah sihanouk', 'preah vihear', 'pursat', 'prey veng', 'ratanakiri',
             'siem reap', 'stung treng', 'svay rieng', 'takéo', 'takeo','tboung khmum']


