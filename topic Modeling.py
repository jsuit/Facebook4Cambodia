__author__ = 'jsuit'
import json
from gensim import corpora
import logging, gensim, bz2
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
fileName = 'posts_language.txt'

stopWords = set(['a','an','the', 'by', 'and', 'be','all', 'http:','https:' 'here', 'also', 'goo.gl', 'do', 'like,' 'below','my', 'go', 'or', 'according', 'likely', 'now','more',
                 'he', 'she,', 'you', "you'll", "will", "till", 'about', 'above', 'before', 'after','your', "you're", 'whom', 'who', 'whoever','it','its', 'itself', "it's",
                 "i",'they','cant',"can't", "cannot", "not", "i'd","i'm",'more', 'most', 'then','if','his', 'her', 'hers', 'here', 'here is', "here's", 'while', 'which',
                 'so', 'therefore','in','that','for','on','with','as','you','do', 'at', 'this', 'but','from','we','say', 'said', 'told', 'my', 'all', 'their', 'what',
                 'out', 'about', 'when', 'just', 'know','into', 'onto,' 'than', 'only','these', 'because', 'after', 'some', 'them', 'mine', 'yours', "what's",'where','have',
                 'get','across','much','how', "how's",'has','was','are','afterwards',"couldn't", 'could', 'spoke','wrote', 'written','indeed','nor','once', 'perhaps','since',
                 'due to', 'something', 'somewhere', 'some','them', 'themselves','those','thus', 'too','upon','were',"weren't",'whether','whose', 'yet', 'corp','of','is', 'there','to', 'without', 'can',
                 'link', 'click', 'other', 'like', 'our', 'read', 'see','i'])
#open file
f = open(fileName, 'r')
#load json
data = json.load(f)
#lowercase, only english
texts = [[word.strip() for word in data[entry]['eng'].lower().split() if word not in stopWords] for entry in data]

#filter out punctuation
import string
punctuation = set(string.punctuation)
for i,text in enumerate(texts):
    tempText=[]
    print text
    for j,word in enumerate(text):
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
    texts[i] = tempText
    #texts[i]=tempText
print texts[0]
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=20, update_every=1, chunksize=10000, passes=10)


print lda.get_document_topics(corpus[0], minimum_probability=0.0)