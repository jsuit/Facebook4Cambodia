__author__ = 'jsuit'
import json
from gensim import corpora
import logging, gensim, bz2
from nltk.stem.porter import PorterStemmer
import pandas as pd
from functools import partial
import string
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
fileName = 'posts_language.txt'

#open file
f = open(fileName, 'r')
#load json
data = json.load(f)
df =  pd.DataFrame(data)
df = df.transpose()

#stopwords file
fileName = 'stopwords.txt'
#get set of stopwords
f = open(fileName, 'r')
stopWords = set()
for line in f:
    line = set(line.split())
    stopWords = stopWords|line

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

p_stemmer = PorterStemmer()
def stem_words(entry):
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

lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=20, update_every=1, chunksize=10000, passes=10)
lda.print_topics(20)

print lda.get_document_topics(dictionary.doc2bow(stemmed_texts[0]))
df = df.ix[:,[0,1,3,4,5,6]]
df.to_csv("processed_data.csv")