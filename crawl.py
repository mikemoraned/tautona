from slacker import Slacker

from optparse import OptionParser
from collections import defaultdict
from ages import newest_message
import json

parser = OptionParser()
parser.add_option("-t", "--token", dest="token", help="your slack token")
parser.add_option("-d", "--distance", dest="max_distance", help="maximum distance between nodes (0 .. 1)")
parser.add_option("-r", "--recency", dest="recency_limit", help="only allow channels written to after this timestamp")
parser.add_option("-o", "--out", dest="outfile", help="name of JSON file to write to")

(options, args) = parser.parse_args()

slack = Slacker(options.token)

response = slack.channels.list()

channel_members = dict()

recency_limit = int(options.recency_limit)

for channel in response.body["channels"]:
    name = channel["name"]
    if channel["is_archived"]:
        print("Ignoring %s (archived)" % name)
    else:
        id = channel["id"]
        history = slack.channels.history(id)
        newest = newest_message(history.body["messages"])
        if newest is None:
            print("Ignoring %s (no actual messages)" % name)
        else:
            newest_ts = int(float(newest["ts"]))
            if newest_ts < recency_limit:
                print("Ignoring %s (not written to recently)" % name)
            else:
                channel_members[name] = frozenset(channel["members"])

names = set()
distances = defaultdict(list)
max_distance = float(options.max_distance)
for (outer_name, outer_members) in channel_members.items():
    for (inner_name, inner_members) in channel_members.items():
        if outer_name < inner_name:
            union_size = len(outer_members.union(inner_members))
            if union_size >= 1:

                similarity = \
                    len(outer_members.intersection(inner_members)) \
                    / union_size
                distance = 1.0 - similarity

                if distance < max_distance:
                    names.add(outer_name)
                    names.add(inner_name)
                    bucket = float("{0:.2f}".format(distance))
                    distances[bucket].append((outer_name, inner_name))

with open(options.outfile, 'w') as outfile:
    summary = {
        'names': list(names),
        'distances' : distances
    }
    json.dump(summary,outfile, sort_keys=True, indent=4, separators=(',', ': '))
