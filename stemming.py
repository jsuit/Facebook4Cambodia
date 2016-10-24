# -- coding: UTF-8 --
import pandas as pd
import math
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
tokenizer = RegexpTokenizer(r'\w+')
en_stop = get_stop_words('en')
data = pd.read_csv('data2.csv', index_col=0)
data = data[1:]

p_stemmer = PorterStemmer()

for index, row in data.iterrows():
	# row[3] = row[3].encode('utf-8')
	if isinstance(row[3], (str, unicode)):
		try:
			row[3].decode('utf-8')
			tokens = tokenizer.tokenize(row[3])
			stopped_tokens = [i for i in tokens if not i in en_stop]
			texts = [p_stemmer.stem(i) for i in stopped_tokens]
			print texts

		except UnicodeError:
			pass
