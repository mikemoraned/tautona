from collections import defaultdict
from gensim import corpora, models
from gensim.models import tfidfmodel


class Analysed():
    def __init__(self, dictionary, corpus, model):
        self.dictionary = dictionary
        self.corpus = corpus
        self.model = model

    def save(self,dir):
        self.dictionary.save(dir + '/dictionary.dict')
        corpora.MmCorpus.serialize(dir + '/corpus.mm', self.corpus)
        self.model.save(dir + '/model_lsi')

    @classmethod
    def load(cls, dir):
        dictionary = corpora.Dictionary.load(dir + '/dictionary.dict')
        corpus = corpora.MmCorpus(dir + '/corpus.mm')
        lsi_model = models.LsiModel.load(dir + '/model_lsi')

        print(dictionary)
        print(corpus)
        lsi_model.print_topics(20)

        return Analysed(dictionary, corpus, lsi_model)


class Analyser():
    def analyse(self, texts):
        reduced_texts = self.remove_single_occurrences(texts)

        dictionary = corpora.Dictionary(reduced_texts)

        corpus = [dictionary.doc2bow(text) for text in reduced_texts]

        tfidf_model = tfidfmodel.TfidfModel(corpus, normalize=True)
        tfidf_corpus = tfidf_model[corpus]

        lsi_model = models.LsiModel(tfidf_corpus, id2word=dictionary, num_topics=400)

        return Analysed(dictionary, tfidf_corpus, lsi_model)

    def remove_single_occurrences(self, texts):
        frequency = defaultdict(int)
        for text in texts:
            for token in text:
                frequency[token] += 1

        texts = [[token for token in text if frequency[token] > 1]
                 for text in texts]
        return texts

