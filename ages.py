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

def newest_message(messages):
    text_messages = [m for m in messages if m["type"] == "message" and "subtype" not in m]
    by_ts = sorted(text_messages, key=lambda m : m["ts"], reverse=True)
    if len(by_ts) > 0:
        return by_ts[0]
    else:
        return None

for channel in response.body["channels"]:
    name = channel["name"]
    id = channel["id"]
    history = slack.channels.history(id)
    created = channel["created"]
    newest = newest_message(history.body["messages"])
    if newest is not None:
        print("%s: %d -> %s: %s" % (name, created, newest["ts"], newest["text"]))
