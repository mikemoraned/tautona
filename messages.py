from optparse import OptionParser
from slacker import Slacker
from gensim import corpora
from collections import defaultdict

parser = OptionParser()
parser.add_option("-t", "--token", dest="token", help="your slack token")

(options, args) = parser.parse_args()

slack = Slacker(options.token)

response = slack.channels.list()

channel_members = dict()

texts = []

stoplist = set('for a of the and to in'.split())
def messages_to_text(messages):
    text = list()
    for m in messages:
        for word in m["text"].lower().split():
            if word not in stoplist:
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

channel_limit = 10
for channel in response.body["channels"]:
    name = channel["name"]
    if channel["is_archived"]:
        print("Ignoring %s (archived)" % name)
    else:
        id = channel["id"]
        history = slack.channels.history(id)
        newest = messages = history.body["messages"]
        text_messages = [m for m in messages if m["type"] == "message" and "subtype" not in m]

        if len(text_messages) > 0:
            print("Found {0} messages in {1}".format(len(text_messages), name))
            texts.append(messages_to_text(text_messages))
            if len(texts) >= channel_limit:
                break
        else:
            print("Ignoring %s (no text messages)" % name)

texts = remove_single_occurrences(texts)

dictionary = corpora.Dictionary(texts)

corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('corpus.mm', corpus)

print(dictionary)
