from slacker import Slacker

from optparse import OptionParser
from sets import Set
from collections import defaultdict
import json

parser = OptionParser()
parser.add_option("-t", "--token", dest="token", help="your slack token")
parser.add_option("-o", "--out", dest="outfile", help="name of JSON file to write to")

(options, args) = parser.parse_args()

slack = Slacker(options.token)

response = slack.channels.list()

channel_members = dict()

for channel in response.body["channels"]:
    name = channel["name"]
    # print name
    channel_members[name] = Set(channel["members"])

# print channel_members

names_with_any_overlap = Set()
overlaps = defaultdict(list)
for (outer_name, outer_members) in channel_members.items():
    for (inner_name, inner_members) in channel_members.items():
        if outer_name < inner_name:
            overlap = outer_members & inner_members
            overlap_size = len(overlap)
            if overlap_size > 1:
                names_with_any_overlap.add(outer_name)
                names_with_any_overlap.add(inner_name)
                overlaps[overlap_size].append("%s,%s" % (outer_name,inner_name))

# print names_with_any_overlap
# print overlaps

with open(options.outfile, 'w') as outfile:
    summary = {
        'names': list(names_with_any_overlap),
        'overlaps': overlaps}
    json.dump(summary,outfile, sort_keys=True, indent=4, separators=(',', ': '))
