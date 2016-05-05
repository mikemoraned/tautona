import logging
from gensim import corpora, models, similarities
from optparse import OptionParser

from channeltotextmapping import ChannelToTextMapping
from analyse import Analysed


class Similarity():

    def __init__(self, channel_mapping, analysed, index):
        self.channel_mapping = channel_mapping
        self.analysed = analysed
        self.index = index

    @classmethod
    def load(cls):
        mapping = ChannelToTextMapping.load("text/channel_text_id.json")

        analysed = Analysed.load("analysis")

        index = similarities.MatrixSimilarity(analysed.model[analysed.corpus])

        return Similarity(mapping, analysed, index)

    def find_similar_channels_for_channel(self, channel_name):
        channel_text_id = self.channel_mapping.text_id_for_name(channel_name)
        channel_as_query = self.analysed.model[self.analysed.corpus[channel_text_id]]

        sims = sorted(enumerate(self.index[channel_as_query]), key=lambda item: -item[1])

        for sim in sims:
            channel_sim_name = self.channel_mapping.channel_name_for_id(sim[0])
            score = sim[1]
            if channel_name != channel_sim_name:
                yield (channel_sim_name, score)

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-c", "--channel", dest="channel", help="name of channel we want to find similarities to")
    parser.add_option("-t", "--topn", dest="topn", help="limit to Top N scores")

    (options, args) = parser.parse_args()
    channel_name = options.channel
    top_n = int(options.topn)

    similarity = Similarity.load()
    scores = similarity.find_similar_channels_for_channel(channel_name)
    print("Top {0} channels similar to {1}:".format(top_n, channel_name))
    for score in list(scores)[:top_n]:
        print(score)