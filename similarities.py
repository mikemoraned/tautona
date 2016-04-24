from gensim import corpora, models, similarities
from collections import defaultdict
import logging
import json

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

channel_to_text_id = {}
text_id_to_channel = []
with open('channel_text_id.json', 'r') as infile:
    channel_to_text_id = json.load(infile)
    for (channel, text_id) in channel_to_text_id.items():
        text_id_to_channel.append("")
    for (channel,text_id) in channel_to_text_id.items():
        text_id_to_channel[text_id] = channel

print(channel_to_text_id)
print(text_id_to_channel)

dictionary = corpora.Dictionary.load('dictionary.dict')
corpus = corpora.MmCorpus('corpus.mm')

lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=100)
index = similarities.MatrixSimilarity(lsi[corpus])

for (channel_name, channel_text_id) in channel_to_text_id.items():
    channel_as_query = lsi[corpus[channel_text_id]]
    sims = sorted(enumerate(index[channel_as_query]), key=lambda item: -item[1])
    for sim in sims:
        channel_sim_name = text_id_to_channel[sim[0]]
        if channel_sim_name is not channel_name:
            print("{0} -> {1}: {2}".format(channel_name, channel_sim_name, sim[1]))