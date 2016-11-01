__author__ = 'jsuit'

import facebook
import pprint
import requests
import json
import sys
import Globals
reload(sys)
sys.setdefaultencoding('utf8')

import pandas as pd
fileName = 'counts.csv'

file = open(fileName,'r')

df =pd.read_csv(file,index_col='ids')

def countComments(comments_file,df):
    comments=json.load(open(comments_file,'r'))
    #df = pd.DataFrame(columns=['ids','poster_id','message'])
    #s = 0
    ids = []
    poster_id = []
    message=[]
    comment_id = []
    date_list= []
    #iterate through ids
    for id in comments:
        cmtList = comments[id]

        #iterate through list of dicts
        for i in cmtList:
            cmts = json.loads(i)

            for comment in cmts:
                ids.append(id)
                message.append(comment['message'])
                poster_id.append(comment['from']['id'])
                comment_id.append(comment['id'])
                date_list.append(comment['created_time'])
    df2 = pd.DataFrame({'ids':ids,'messages': message,'poster_id':poster_id,'comment_id':comment_id, 'datetime':date_list})
    #df = df.set_index('ids')
    #print df
    groupByID = df2.groupby('ids')
    print sum(groupByID.poster_id.nunique())
    print sum(groupByID.poster_id.agg('count'))
    series= -groupByID.poster_id.nunique() +groupByID.poster_id.agg('count')
    df3 = pd.DataFrame(series)
    #df.join( -groupByID.poster_id.nunique() +groupByID.poster_id.agg('count'))
    df = df.join(df3)
    df=df.rename(columns = {'poster_id':'unique_comments'})
    df.to_csv("countsWithUniqueCommentsCounts.csv")
countComments('all_comments.txt',df)