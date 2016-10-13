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

    def numCommentsForPost(self,postID,comments_file):
        comments=json.load(comments_file)
        return len(comments[postID])

    def getNumReactionsForPost(self,postId):

        r = requests.get('https://graph.facebook.com/v2.8/'+ postId +'/?fields=reactions.summary(1).limit(1)&access_token='+Globals.access_token)
        #reactions = self.graph.get_connections(id=postId, connection_name='reactions',args={'fields': 'summary=1','total_count':1})
        #print r.text
        txt = r.json()
        return  txt['reactions']['summary']['total_count']


    def getNumLikesForPost(self, postID):
        reqString = "https://graph.facebook.com/v2.8/" +postID + '/?fields=likes.summary(true).limit(1)&access_token=' + Globals.access_token
        r = requests.get(reqString)
        txt = r.json()
        return  txt['likes']['summary']['total_count']



def some_action(post):
    """ Here you might want to do something with each post. E.g. grab the
    post's message (post['message']) or the post's picture (post['picture']).
    In this implementation we just print the post's created time.
    """
    print(post['created_time'])


graph = GraphAPI()
#comments = graph.getAllComments()
#graph.saveToFile('all_comments.txt',comments)
r = graph.getNumLikesForPost('79770243223_10154089375478224')
print r
#graph.saveToFile('all_reactions.txt',r)

