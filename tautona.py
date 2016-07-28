import os
import argparse
import logging
from analyse import Analyser
from channeltexts import ChannelTexts
from crawl import Crawler
from similarity import Similarity
from slacker import Slacker

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def crawl(args):
    token = os.environ["SLACK_API_TOKEN"]
    slack = Slacker(token)

    texts = ChannelTexts()

    Crawler(slack).crawl(texts)

    texts.save("text/channel_text_id.json", "text/channel_texts.txt")


def analyse(args):
    channel_texts = ChannelTexts.load("text/channel_text_id.json", "text/channel_texts.txt")

    Analyser().analyse(channel_texts.texts_only()).save("analysis")


def similarity(args):
    channel_name = args.channel
    top_n = int(args.topn)

    similarity = Similarity.load("analysis")
    scores = similarity.find_similar_channels_for_channel(channel_name)
    print("Top {0} channels similar to {1}:".format(top_n, channel_name))
    for score in list(scores)[:top_n]:
        print(score)


parser = argparse.ArgumentParser(prog='Tautona')
subparsers = parser.add_subparsers()

parser_crawl = subparsers.add_parser('crawl')
parser_crawl.set_defaults(func=crawl)

parser_analyse = subparsers.add_parser('analyse')
parser_analyse.set_defaults(func=analyse)

parser_similarity = subparsers.add_parser('similarity')
parser_similarity.add_argument("--channel", help="name of channel we want to find similarities to")
parser_similarity.add_argument("--topn", help="limit to Top N scores")
parser_similarity.set_defaults(func=similarity)

args = parser.parse_args()
args.func(args)
