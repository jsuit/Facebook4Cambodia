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
import pandas as pd
from datetime import datetime

#files
likes = open('LikesForPost.txt','r')
shares = open('SharesForPost.txt','r')
comments = open('commntCnts.txt','r')
likes_reactions = open('LikesReactions.txt','r')
date = open('PostCreatedTime.txt','r')
messages = open('PostIdWithEngMessage.txt','r')
chars = open('PostIdWithCharCount.txt','r')
words = open('PostIdWithWordCount.txt','r')

#likes_reactions
ids = []
date_list = []
post_date = json.load(date)
for i,id in enumerate(post_date):
	ids.append(id)
	date = datetime.strptime(post_date[id], '%Y-%m-%dT%H:%M:%S')
	# date_list.append(post_date[id])
	date_list.append(date)
#likes_reactions dataframe
df = pd.DataFrame({'ids':ids,'datetime':date_list})
df = df.set_index('ids')

#likes
ids = []
num_likes_list = []
num_likes = json.load(likes)
for i,id in enumerate(num_likes):
	ids.append(id)
	num_likes_list.append(num_likes[id])
#likes dataframe
df_likes = pd.DataFrame({'ids':ids,'likes':num_likes_list})
df_likes = df_likes.set_index('ids')
# df_likes['ids'] = df_likes.index
df = df.join(df_likes)

#shares
ids = []
num_shares_list = []
num_shares = json.load(shares)
for i,id in enumerate(num_shares):
	ids.append(id)
	num_shares_list.append(num_shares[id])
#shares dataframe
df_shares = pd.DataFrame({'ids':ids,'shares':num_shares_list})
df_shares = df_shares.set_index('ids')

df = df.join(df_shares)

#comments
ids = []
num_comments_list = []
num_comments = json.load(comments)
for i,id in enumerate(num_comments):
	ids.append(id)
	num_comments_list.append(num_comments[id])
#comments dataframe
df_comments = pd.DataFrame({'ids':ids,'comments':num_comments_list})
df_comments = df_comments.set_index('ids')

df = df.join(df_comments)

#likes_reactions
ids = []
num_likes_reactions_list = []
num_likes_reactions = json.load(likes_reactions)
for i,id in enumerate(num_likes_reactions):
	ids.append(id)
	num_likes_reactions_list.append(num_likes_reactions[id])
#likes_reactions dataframe
df_likes_reactions = pd.DataFrame({'ids':ids,'likes_reactions':num_likes_reactions_list})
df_likes_reactions = df_likes_reactions.set_index('ids')

#whole dataframe
df = df.join(df_likes_reactions)
df['reactions'] = df['likes_reactions'] - df['likes']
df['total'] = df['likes'] + df['shares'] + df['comments'] + df['reactions']

#char_count
ids = []
chars_list = []
num_chars = json.load(chars)
for i,id in enumerate(num_chars):
	ids.append(id)
	chars_list.append(num_chars[id])
#likes_reactions dataframe
df_chars = pd.DataFrame({'ids':ids,'chars_count':chars_list})
df_chars = df_chars.set_index('ids')
#whole dataframe
df = df.join(df_chars)

#word_count
ids = []
words_list = []
num_words = json.load(words)
for i,id in enumerate(num_words):
	ids.append(id)
	words_list.append(num_words[id])
#likes_reactions dataframe
df_words = pd.DataFrame({'ids':ids,'words_count':words_list})
df_words = df_words.set_index('ids')
#whole dataframe
df = df.join(df_words)

# message/story
ids = []
message_list = []
num_messages = json.load(messages)
for i,id in enumerate(num_messages):
	ids.append(id)
	message_list.append(num_messages[id])
#message dataframe
df_messages = pd.DataFrame({'ids':ids,'message':message_list})
df_messages = df_messages.set_index('ids')

df = df.join(df_messages)

df['date'] = df['datetime'].dt.date
print df
df.to_csv("counts.csv")

# messages = open('posts_language.txt','r')
# ids = []
# message_list = []
# num_messages = json.load(messages)
# for i,id in enumerate(num_messages):
# 	ids.append(id)
# 	message_list.append(num_messages[id])
# #likes_reactions dataframe
# df_messages = pd.DataFrame({'ids':ids,'message':message_list})
# df_messages = df_messages.set_index('ids')
# print df_messages
# df_messages.to_csv("posts_dummy.csv")


# data = pd.read_csv('processed_data.csv', index_col=0)
# data = data[['eng', 'id']]
# data = data.merge(df,)