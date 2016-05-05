import logging
from collections import defaultdict
from gensim import corpora, models
from gensim.models import tfidfmodel
from optparse import OptionParser

from channeltexts import ChannelTexts


def remove_single_occurrences(texts):
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1

    texts = [[token for token in text if frequency[token] > 1]
             for text in texts]
    return texts


class Analysed():
    def __init__(self, dictionary, corpus, model):
        self.dictionary = dictionary
        self.corpus = corpus
        self.model = model

    def save(self):
        self.dictionary.save('dictionary.dict')
        corpora.MmCorpus.serialize('corpus.mm', self.corpus)
        self.model.save("model_lsi")

    @classmethod
    def load(cls):
        dictionary = corpora.Dictionary.load('dictionary.dict')
        corpus = corpora.MmCorpus('corpus.mm')
        lsi_model = models.LsiModel.load("model_lsi")

        print(dictionary)
        print(corpus)
        lsi_model.print_topics(20)

        return Analysed(dictionary, corpus, lsi_model)


class Analyser():
    def analyse(self, texts):
        dictionary = corpora.Dictionary(texts)

        corpus = [dictionary.doc2bow(text) for text in texts]

        tfidf_model = tfidfmodel.TfidfModel(corpus, normalize=True)
        tfidf_corpus = tfidf_model[corpus]

        lsi_model = models.LsiModel(tfidf_corpus, id2word=dictionary, num_topics=400)

        return Analysed(dictionary, tfidf_corpus, lsi_model)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    parser = OptionParser()

    (options, args) = parser.parse_args()

    channel_texts = ChannelTexts.load("channel_text_id.json", "channel_texts.txt")
    texts = remove_single_occurrences(channel_texts.texts_only())

    Analyser().analyse(texts).save()
