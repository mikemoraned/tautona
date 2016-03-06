from slacker import Slacker

from optparse import OptionParser
from collections import defaultdict
import json
from statistics import mean

parser = OptionParser()
parser.add_option("-i", "--in", dest="infile", help="the name of the summary JSON file")
parser.add_option("-t", "--token", dest="token", help="your slack token")
parser.add_option("-u", "--user", dest="userid", help="userid to produce recommendations for")

(options, args) = parser.parse_args()

slack = Slacker(options.token)


def find_user_channel_names(userid):
    response = slack.channels.list()

    def fetch():
        for channel in response.body["channels"]:
            name = channel["name"]
            members = channel["members"]
            if userid in members:
                yield name

    return frozenset(fetch())


class Recommender():
    def __init__(self, summary):
        self.summary = summary

    def recommend_channels(self, user_channel_set):
        channel_distances = defaultdict(list)
        for (distance, channel_pairs) in self.summary["distances"].items():
            for channel_pair in channel_pairs:
                channel_set = frozenset(channel_pair)
                overlapping_channels = user_channel_set.intersection(channel_set)
                missing_channels = channel_set.difference(overlapping_channels)
                if len(missing_channels) > 0:
                    for missing_channel in missing_channels:
                        channel_distances[missing_channel].append(float(distance))

        scored_channels = list()
        for (channel_name, distances) in channel_distances.items():
            score = 1.0 - mean(distances)
            bucketed_score = float("{0:.2f}".format(score))
            scored_channels.append({"name": channel_name, "score": bucketed_score})

        return sorted(scored_channels, key=lambda i: i["score"], reverse=True)


with open(options.infile, 'r') as infile:
    summary = json.load(infile)
    recommender = Recommender(summary)
    user = slack.users.info(options.userid)
    user_channels = find_user_channel_names(options.userid)
    print(user_channels)
    recommended_channels = recommender.recommend_channels(user_channels)
    for recommended_channel in recommended_channels:
        print(recommended_channel)
