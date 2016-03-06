from slacker import Slacker

from optparse import OptionParser
from collections import defaultdict
import json

parser = OptionParser()
parser.add_option("-i", "--in", dest="infile", help="the name of the summary JSON file")
parser.add_option("-t", "--token", dest="token", help="your slack token")
parser.add_option("-u", "--user", dest="userid", help="userid to produce recommendations for")

(options, args) = parser.parse_args()

slack = Slacker(options.token)

def find_user_channels(userid):
    response = slack.channels.list()

    for channel in response.body["channels"]:
        name = channel["name"]
        members = channel["members"]
        if userid in members:
            yield name


with open(options.infile, 'r') as infile:
    summary = json.load(infile)
    user = slack.users.info(options.userid)
    user_channels = find_user_channels(options.userid)
    print(list(user_channels))
