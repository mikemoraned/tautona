from optparse import OptionParser
from slacker import Slacker
from gensim import corpora, models
from gensim.models import tfidfmodel
from collections import defaultdict
import logging
import json
import re

from channeltexts import ChannelTexts

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

parser = OptionParser()

(options, args) = parser.parse_args()

channel_texts = ChannelTexts.load("channel_text_id.json", "channel_texts.txt")
texts = channel_texts.texts_only()

def remove_single_occurrences(texts):
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1

    texts = [[token for token in text if frequency[token] > 1]
             for text in texts]
    return texts

texts = remove_single_occurrences(texts)

dictionary = corpora.Dictionary(texts)

corpus = [dictionary.doc2bow(text) for text in texts]
tfidf_model = tfidfmodel.TfidfModel(corpus, normalize=True)
tfidf_corpus = tfidf_model[corpus]

lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=400)
lsi.print_topics(20)

model = lsi

dictionary.save('dictionary.dict')
corpora.MmCorpus.serialize('corpus.mm', tfidf_corpus)
model.save("model_lsi")

print(dictionary)
