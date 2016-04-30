import logging
from optparse import OptionParser
from slacker import Slacker

from channeltexts import ChannelTexts

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

parser = OptionParser()
parser.add_option("-t", "--token", dest="token", help="your slack token")

(options, args) = parser.parse_args()

slack = Slacker(options.token)

response = slack.channels.list()

texts = ChannelTexts()

min_messages = 100
max_messages = 1000
channel_limit = 1000


def channel_message_sample(channel_id, max_messages):
    history = slack.channels.history(channel_id, count=max_messages)
    messages = history.body["messages"]
    return [m for m in messages if m["type"] == "message" and "subtype" not in m]


for channel in response.body["channels"][:channel_limit]:
    name = channel["name"]
    if channel["is_archived"]:
        print("Ignoring %s (archived)" % name)
    else:
        text_messages = channel_message_sample(channel["id"], max_messages)

        if len(text_messages) >= min_messages:
            print("Found {0} messages in {1}".format(len(text_messages), name))
            texts.add_messages_for_channel(name, text_messages)
        else:
            print("Ignoring {0} (not enough text messages, {1})".format(name, len(text_messages)))

texts.save("channel_text_id.json", "channel_texts.txt")
