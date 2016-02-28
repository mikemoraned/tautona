from slacker import Slacker

from optparse import OptionParser
from sets import Set
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
member_channels = defaultdict(set)

for channel in response.body["channels"]:
    name = channel["name"]
    # print name
    members = Set(channel["members"])
    channel_members[name] = members
    for member in members:
        member_channels[member].add(name)

# print channel_members

min_overlap = int(options.min_overlap)

channel_names_with_any_overlap = Set()
channel_overlaps = defaultdict(list)
max_channel_overlap = 0
for (outer_name, outer_members) in channel_members.items():
    for (inner_name, inner_members) in channel_members.items():
        if outer_name < inner_name:
            overlap = outer_members & inner_members
            overlap_size = len(overlap)
            if overlap_size >= min_overlap:
                max_channel_overlap = max(max_channel_overlap, overlap_size)
                channel_names_with_any_overlap.add(outer_name)
                channel_names_with_any_overlap.add(inner_name)
                channel_overlaps[overlap_size].append((outer_name, inner_name))

member_names_with_any_overlap = Set()
member_overlaps = defaultdict(list)
max_member_overlap = 0
for (outer_name, outer_channels) in member_channels.items():
    for (inner_name, inner_channels) in member_channels.items():
        if outer_name < inner_name:
            overlap = outer_channels & inner_channels
            overlap_size = len(overlap)
            if overlap_size >= min_overlap:
                max_member_overlap = max(max_member_overlap, overlap_size)
                member_names_with_any_overlap.add(outer_name)
                member_names_with_any_overlap.add(inner_name)
                member_overlaps[overlap_size].append((outer_name, inner_name))

# print names_with_any_overlap
# print overlaps

with open(options.outfile, 'w') as outfile:
    node_number = dict()
    nodes = list()
    for name in member_names_with_any_overlap:
        node = {'name': "%s: %s" % (name, member_channels[name])}
        node_number[name] = len(nodes)
        nodes.append(node)

    links = list()
    for (overlap, pairs) in member_overlaps.iteritems():
        for pair in pairs:
            (source, target) = pair
            value = int(20 * (float(max_member_overlap - overlap) / float(max_member_overlap)))
            links.append({
                'source': node_number[source],
                'target': node_number[target],
                'value': value
            })

    summary = {
        'nodes': nodes,
        'links': links}
    json.dump(summary,outfile, sort_keys=True, indent=4, separators=(',', ': '))
