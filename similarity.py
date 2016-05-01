import logging
from gensim import corpora, models, similarities
from optparse import OptionParser

from channeltotextmapping import ChannelToTextMapping


class Similarity():

    def __init__(self, channel_mapping, dictionary, corpus, model, index):
        self.channel_mapping = channel_mapping
        self.corpus = corpus
        self.dictionary = dictionary
        self.index = index
        self.model = model

    @classmethod
    def load(cls):
        mapping = ChannelToTextMapping.load("channel_text_id.json")

        dictionary = corpora.Dictionary.load('dictionary.dict')
        corpus = corpora.MmCorpus('corpus.mm')

        lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=400)
        lsi.print_topics(20)

        model = lsi
        index = similarities.MatrixSimilarity(model[corpus])

        return Similarity(mapping, dictionary, corpus, model, index)

    def find_similar_channels_for_channel(self, channel_name):
        channel_text_id = self.channel_mapping.text_id_for_name(channel_name)
        channel_as_query = self.model[self.corpus[channel_text_id]]

        sims = sorted(enumerate(self.index[channel_as_query]), key=lambda item: -item[1])

        for sim in sims:
            channel_sim_name = self.channel_mapping.channel_name_for_id(sim[0])
            score = sim[1]
            yield (channel_sim_name, score)

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-c", "--channel", dest="channel", help="name of channel we want to find similarities to")
    parser.add_option("-t", "--topn", dest="topn", help="limit to Top N scores")

    (options, args) = parser.parse_args()
    channel_name = options.channel
    top_n = int(options.topn)

    print("Top {0} channels similar to {1}:".format(top_n, channel_name))

    similarity = Similarity.load()
    scores = similarity.find_similar_channels_for_channel(channel_name)
    for score in list(scores)[:top_n]:
        print(score)