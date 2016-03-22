from slacker import Slacker

from optparse import OptionParser
from collections import defaultdict
import json

parser = OptionParser()
parser.add_option("-t", "--token", dest="token", help="your slack token")

(options, args) = parser.parse_args()

slack = Slacker(options.token)

response = slack.channels.list()

channel_members = dict()

for channel in response.body["channels"]:
    name = channel["name"]
    created = channel["created"]
    print("%s: %d" % (name, created))
