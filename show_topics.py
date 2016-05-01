from gensim import corpora, models, similarities
from collections import defaultdict
from optparse import OptionParser
import logging
import json

from channeltotextmapping import ChannelToTextMapping

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

parser = OptionParser()

(options, args) = parser.parse_args()

mapping = ChannelToTextMapping.load("channel_text_id.json")

dictionary = corpora.Dictionary.load('dictionary.dict')
corpus = corpora.MmCorpus('corpus.mm')

lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=400)
lsi.print_topics(20)

model = lsi
index = similarities.MatrixSimilarity(model[corpus])

for (channel_name, channel_text_id) in mapping.items():
    topic_id_wieghts = model[corpus[channel_text_id]]
    sorted_topic_id_wieghts = sorted(topic_id_wieghts, key=lambda item: -item[1])
    print(channel_name)
    # for (topic_id, wieght) in sorted_topic_id_wieghts[:5]:
    #     print("{0}: {1}".format(wieght, lsi.print_topic(topic_id, topn=5)))
    multiplied_word_wieghts = {}
    for (topic_id, topic_wieght) in topic_id_wieghts:
        for (word, word_wieght) in lsi.show_topic(topic_id, topn=10):
            if word in multiplied_word_wieghts:
                multiplied_word_wieght = multiplied_word_wieghts[word]
                multiplied_word_wieghts[word] = multiplied_word_wieght * topic_wieght * word_wieght
            else:
                multiplied_word_wieghts[word] = topic_wieght * word_wieght
    sorted_multiplied_word_wieghts = sorted(multiplied_word_wieghts.items(), key=lambda item: -item[1])
    print(sorted_multiplied_word_wieghts[:10])
