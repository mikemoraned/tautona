from gensim import corpora, models, similarities
from collections import defaultdict
from optparse import OptionParser
import logging
import json

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

parser = OptionParser()
parser.add_option("-d", "--distance", dest="max_distance", help="maximum distance between nodes (0 .. 1)")
parser.add_option("-o", "--out", dest="outfile", help="name of JSON file to write to")

(options, args) = parser.parse_args()

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

names = set()
distances = defaultdict(list)
max_distance = float(options.max_distance)
for (channel_name, channel_text_id) in channel_to_text_id.items():
    channel_as_query = lsi[corpus[channel_text_id]]
    sims = sorted(enumerate(index[channel_as_query]), key=lambda item: -item[1])
    for sim in sims:
        channel_sim_name = text_id_to_channel[sim[0]]
        if channel_sim_name < channel_name: # assume distance is symmetric
            channel_sim_cosine_distance = sim[1]
            distance = 1.0 - ((channel_sim_cosine_distance + 1.0) / 2.0)
            if distance < max_distance:
                bucket = float("{0:.2f}".format(distance))
                print("{0} -> {1}: {2}".format(channel_name, channel_sim_name, bucket))
                names.add(channel_name)
                names.add(channel_sim_name)
                distances[bucket].append((channel_name, channel_sim_name))

with open(options.outfile, 'w') as outfile:
    summary = {
        'names': list(names),
        'distances': distances
    }
    json.dump(summary, outfile, sort_keys=True, indent=4, separators=(',', ': '))