from optparse import OptionParser
from slacker import Slacker
from gensim import corpora
from gensim.models import tfidfmodel
from collections import defaultdict
import logging
import json
import re

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

parser = OptionParser()
parser.add_option("-t", "--token", dest="token", help="your slack token")

(options, args) = parser.parse_args()

slack = Slacker(options.token)

response = slack.channels.list()

channel_members = dict()

texts = []

special = re.compile("<.+?>")
stoplist = set('for a of the and to in'.split())
def messages_to_text(messages):
    text = list()
    for m in messages:
        for word in m["text"].lower().split():
            if word not in stoplist and not special.match(word):
                text.append(word)
    return text

def remove_single_occurrences(texts):
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1

    texts = [[token for token in text if frequency[token] > 1]
             for text in texts]
    return texts

channel_to_text_id = {}

min_messages = 100
max_messages = 1000
channel_limit = 1000
for channel in response.body["channels"]:
    name = channel["name"]
    if channel["is_archived"]:
        print("Ignoring %s (archived)" % name)
    else:
        id = channel["id"]
        history = slack.channels.history(id, count=max_messages)
        newest = messages = history.body["messages"]
        text_messages = [m for m in messages if m["type"] == "message" and "subtype" not in m]

        if len(text_messages) >= min_messages:
            print("Found {0} messages in {1}".format(len(text_messages), name))
            text_id = len(texts)
            channel_to_text_id[name] = text_id
            texts.append(messages_to_text(text_messages))
            if len(texts) >= channel_limit:
                break
        else:
            print("Ignoring {0} (not enough text messages, {1})".format(name, len(text_messages)))

texts = remove_single_occurrences(texts)

dictionary = corpora.Dictionary(texts)

corpus = [dictionary.doc2bow(text) for text in texts]
tfidf_model = tfidfmodel.TfidfModel(corpus, normalize=True)
tfidf_corpus = tfidf_model[corpus]

with open('channel_text_id.json', 'w') as outfile:
    json.dump(channel_to_text_id, outfile, sort_keys=True, indent=4, separators=(',', ': '))
dictionary.save('dictionary.dict')
corpora.MmCorpus.serialize('tfidf_corpus.mm', tfidf_corpus)

print(dictionary)
