from slacker import Slacker

from optparse import OptionParser
from collections import defaultdict
import json
from statistics import mean

parser = OptionParser()
parser.add_option("-i", "--in", dest="infile", help="the name of the summary JSON file")
parser.add_option("-t", "--token", dest="token", help="your slack token")
parser.add_option("-u", "--user", dest="username", help="username to produce recommendations for")

(options, args) = parser.parse_args()

slack = Slacker(options.token)


class UnknownUsername(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "unknown user: {0}".format(self.name)


def find_user_by_name(username):
    response = slack.users.list()

    for member in response.body["members"]:
        if member["name"] == username:
            return member

    raise UnknownUsername(username)


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
                if len(overlapping_channels) > 0 and len(missing_channels) > 0:
                    for missing_channel in missing_channels:
                        channel_distances[missing_channel].append({
                            "distance": float(distance),
                            "overlapping": list(overlapping_channels)
                        })

        scored_channels = list()
        for (channel_name, support) in channel_distances.items():
            score = 1.0 - mean(map(lambda s: s["distance"], support))
            bucketed_score = float("{0:.2f}".format(score))
            scored_channels.append({
                "name": channel_name,
                "score": bucketed_score,
                "support": support
            })

        return sorted(scored_channels, key=lambda i: i["score"], reverse=True)


with open(options.infile, 'r') as infile:
    summary = json.load(infile)
    recommender = Recommender(summary)

    user = find_user_by_name(options.username)
    user_channels = find_user_channel_names(user["id"])

    print("Recommended channels for {real_name}:".format(**user))
    recommended_channels = recommender.recommend_channels(user_channels)
    for recommended_channel in recommended_channels:
        print("{score:.2f}: {name}, because:".format(**recommended_channel))
        for support in recommended_channel["support"]:
            print("\t{overlapping}: distance: {distance}".format(**support))
