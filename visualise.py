from slacker import Slacker

from optparse import OptionParser
from itertools import groupby
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

        links_with_distance_rank = list()
        def sort_by_source(link):
            return link["source"]
        def sort_by_distance(link):
            return link["distance"]
        for k, g in groupby(sorted(links, key=sort_by_source), sort_by_source):
            for rank, link in enumerate(sorted(g,key=sort_by_distance)):
                link["source_rank"] = rank
                links_with_distance_rank.append(link)

        summary = {
            'nodes': nodes,
            'links': links_with_distance_rank}
        json.dump(summary,outfile, sort_keys=True, indent=4, separators=(',', ': '))
