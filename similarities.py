from gensim import similarities
from collections import defaultdict
from optparse import OptionParser
import logging
import json

from channeltotextmapping import ChannelToTextMapping
from analyse import Analysed

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)

parser = OptionParser()
parser.add_option("-d", "--distance", dest="max_distance",
                  help="maximum distance between nodes (0 .. 1)")
parser.add_option("-o", "--out", dest="outfile",
                  help="name of JSON file to write to")

(options, args) = parser.parse_args()

mapping = ChannelToTextMapping.load("channel_text_id.json")

analysed = Analysed.load()

index = similarities.MatrixSimilarity(analysed.model[analysed.corpus])

names = set()
distances = defaultdict(list)
max_distance = float(options.max_distance)
for (channel_name, channel_text_id) in mapping.items():
    channel_as_query = analysed.model[analysed.corpus[channel_text_id]]
    sims = sorted(enumerate(index[channel_as_query]),
                  key=lambda item: -item[1])
    for sim in sims:
        channel_sim_name = mapping.channel_name_for_id(sim[0])
        if channel_sim_name < channel_name:  # assume distance is symmetric
            channel_sim_cosine_distance = sim[1]
            # assume cosine distance always > 0
            distance = 1.0 - channel_sim_cosine_distance
            if distance < max_distance:
                bucket = float("{0:.2f}".format(distance))
                names.add(channel_name)
                names.add(channel_sim_name)
                distances[bucket].append((channel_name, channel_sim_name))

with open(options.outfile, 'w') as outfile:
    summary = {
        'names': list(names),
        'distances': distances
    }
    json.dump(summary, outfile, sort_keys=True,
              indent=4, separators=(',', ': '))
