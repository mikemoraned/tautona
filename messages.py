from optparse import OptionParser
from slacker import Slacker

parser = OptionParser()
parser.add_option("-t", "--token", dest="token", help="your slack token")

(options, args) = parser.parse_args()

slack = Slacker(options.token)

response = slack.channels.list()

channel_members = dict()

documents = []

for channel in response.body["channels"]:
    name = channel["name"]
    if channel["is_archived"]:
        print("Ignoring %s (archived)" % name)
    else:
        id = channel["id"]
        history = slack.channels.history(id)
        newest = messages = history.body["messages"]
        text_messages = [m for m in messages if m["type"] == "message" and "subtype" not in m]

        if len(text_messages) > 0:
            print("Found {0} messages in {1}".format(len(text_messages), name))
            documents.append(text_messages)
        else:
            print("Ignoring %s (no text messages)" % name)

print(documents)