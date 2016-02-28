from slacker import Slacker

from optparse import OptionParser
from collections import defaultdict
import json

parser = OptionParser()
parser.add_option("-t", "--token", dest="token", help="your slack token")
parser.add_option("-s", "--size", dest="min_overlap", help="minimum size of overlap")
parser.add_option("-o", "--out", dest="outfile", help="name of JSON file to write to")

(options, args) = parser.parse_args()

slack = Slacker(options.token)

response = slack.channels.list()

channel_members = dict()

for channel in response.body["channels"]:
    name = channel["name"]
    channel_members[name] = set(channel["members"])

min_overlap = int(options.min_overlap)
names_with_any_overlap = set()
overlaps = defaultdict(list)
max_overlap = 0
for (outer_name, outer_members) in channel_members.items():
    for (inner_name, inner_members) in channel_members.items():
        if outer_name < inner_name:
            overlap = outer_members & inner_members
            overlap_size = len(overlap)
            if overlap_size >= min_overlap:
                max_overlap = max(max_overlap, overlap_size)
                names_with_any_overlap.add(outer_name)
                names_with_any_overlap.add(inner_name)
                overlaps[overlap_size].append((outer_name,inner_name))

with open(options.outfile, 'w') as outfile:
    node_number = dict()
    nodes = list()
    for name in names_with_any_overlap:
        node = {'name': name}
        node_number[name] = len(nodes)
        nodes.append(node)

    links = list()
    for (overlap, pairs) in overlaps.items():
        for pair in pairs:
            (source, target) = pair
            value = int(20 * (float(max_overlap - overlap) / float(max_overlap)))
            links.append({
                'source': node_number[source],
                'target': node_number[target],
                'value': value
            })

    summary = {
        'nodes': nodes,
        'links': links}
    json.dump(summary,outfile, sort_keys=True, indent=4, separators=(',', ': '))
