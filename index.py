from slacker import Slacker

from optparse import OptionParser
from collections import defaultdict
import json

parser = OptionParser()
parser.add_option("-t", "--token", dest="token", help="your slack token")
parser.add_option("-d", "--distance", dest="max_distance", help="maximum distance between nodes (0 .. 1)")
parser.add_option("-o", "--out", dest="outfile", help="name of JSON file to write to")

(options, args) = parser.parse_args()

slack = Slacker(options.token)

response = slack.channels.list()

channel_members = dict()

for channel in response.body["channels"]:
    name = channel["name"]
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
    node_number = dict()
    nodes = list()
    for name in names:
        node = {'name': name}
        node_number[name] = len(nodes)
        nodes.append(node)

    links = list()
    for (distance, pairs) in distances.items():
        for pair in pairs:
            (source, target) = pair
            links.append({
                'source': node_number[source],
                'target': node_number[target],
                'distance': distance
            })

    summary = {
        'nodes': nodes,
        'links': links}
    json.dump(summary,outfile, sort_keys=True, indent=4, separators=(',', ': '))
