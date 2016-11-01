__author__ = 'jsuit'

import json
from gensim import corpora
import logging, gensim, bz2
from nltk.stem.porter import PorterStemmer
import pandas as pd
from functools import partial
import string
from stopWords import stopWords
from gensim import corpora, models, similarities
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
fileName = 'posts_language.txt'

#open file
f = open(fileName, 'r')
#load json
data = json.load(f)
df =  pd.DataFrame(data)
df = df.transpose()

#stopwords file
#fileName = 'stopwords.txt'
#get set of stopwords
#f = open(fileName, 'r')
#stopWords = set()
#for line in f:
 #   line = set(line.split())
 #   stopWords = stopWords|line

def remove_stopwords(entry):
    res = [word.strip() for word in entry.lower().split() if word not in stopWords]
    return res

punctuation = set(string.punctuation)
def remove_punc(entry):
    tempText=[]
    for word in entry:
        if 'http' in word:
            continue
        if word == 'u.s.':
            tempText.append(word)
            continue
        newWord = []
        for c in word:
            if c in punctuation:
                continue
            else:
                newWord.append(c)
        s = ''.join(newWord)
        if not s.isspace() and s != '':
            tempText.append(s)
    return tempText


def stem_words(entry):
    p_stemmer = PorterStemmer()
    res =[p_stemmer.stem(i) for i in entry]
    return res

def bow(dictionary,entry):
    corpus = dictionary.doc2bow(entry)
    return corpus

df['stopwords_removed'] = df['eng'].apply(remove_stopwords)
df['punctuation_removed'] = df['stopwords_removed'].apply(remove_punc)
df['stemmed_text'] = df['punctuation_removed'].apply(stem_words)

stemmed_texts = df['stemmed_text'].tolist()
dictionary = corpora.Dictionary(stemmed_texts)

df['bow'] = df['stemmed_text'].apply(partial(bow,dictionary))
corpus = [dictionary.doc2bow(text) for text in stemmed_texts]

tfidf = models.TfidfModel(corpus,normalize=True)
corpus_tfidf = tfidf[corpus]
lsi = models.LsiModel(corpus=corpus, id2word=dictionary, num_topics=2)

lsi.print_topics(num_topics=20, num_words=2)
corpus_tfidf = tfidf[corpus]
corpus_lsi = lsi[corpus_tfidf]
x = []
y =[]
for i,doc in enumerate(corpus_lsi):
    print doc,i
    if len(doc) >= 1:
        x.append(doc[0][1])
        y.append(doc[1][1])

from matplotlib import pyplot as plt

plt.plot(x,y,'ro')
plt.show()
