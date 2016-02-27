from slacker import Slacker

from optparse import OptionParser
from sets import Set

parser = OptionParser()
parser.add_option("-t", "--token", dest="token", help="your slack token")

(options, args) = parser.parse_args()

slack = Slacker(options.token)

response = slack.channels.list()

channel_members = dict()

for channel in response.body["channels"]:
    name = channel["name"]
    #print name
    channel_members[name] = Set(channel["members"])

print channel_members

names_with_any_overlap = Set()
overlaps = dict()
for (outer_name, outer_members) in channel_members.items():
    for (inner_name, inner_members) in channel_members.items():
        if outer_name < inner_name:
            overlap = outer_members & inner_members
            if len(overlap) > 1:
                names_with_any_overlap.add(outer_name)
                names_with_any_overlap.add(inner_name)
                overlaps[(outer_name, inner_name)] = overlap

print names_with_any_overlap
print overlaps