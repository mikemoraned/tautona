from slacker import Slacker

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-t", "--token", dest="token", help="your slack token")

(options, args) = parser.parse_args()

slack = Slacker(options.token)

response = slack.channels.list()

for channel in response.body["channels"]:
    print channel["name"]



