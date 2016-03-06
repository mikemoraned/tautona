from slacker import Slacker

from optparse import OptionParser
from collections import defaultdict
import json

parser = OptionParser()
parser.add_option("-i", "--in", dest="infile", help="the name of the summary JSON file")
parser.add_option("-o", "--out", dest="outfile", help="name of JSON file to write to")

(options, args) = parser.parse_args()

with open(options.infile, 'r') as infile:
    summary = json.load(infile)
    with open(options.outfile, 'w') as outfile:
        node_number = dict()
        nodes = list()
        for name in summary["names"]:
            node = {'name': name}
            node_number[name] = len(nodes)
            nodes.append(node)

        links = list()
        for (distance, pairs) in summary["distances"].items():
            for pair in pairs:
                (source, target) = pair
                links.append({
                    'source': node_number[source],
                    'target': node_number[target],
                    'distance': distance
                })

        summary = {
            'nodes': nodes,
            'links': links}
        json.dump(summary,outfile, sort_keys=True, indent=4, separators=(',', ': '))
