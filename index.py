from slacker import Slacker

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-t", "--token", dest="token", help="your slack token")

(options, args) = parser.parse_args()

slack = Slacker(options.token)

response = slack.channels.list()

channel_users = dict()

for channel in response.body["channels"]:
    name = channel["name"]
    print name
    channel_users[name] = channel["members"]

print channel_users


