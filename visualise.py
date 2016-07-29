import argparse
import json
from itertools import groupby
from nameremapper import NameRemapper

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--in", dest="infile", help="the name of the summary JSON file")
parser.add_argument("-o", "--out", dest="outfile", help="name of JSON file to write to")
parser.add_argument("-a", "--anonymize", dest="anonymize", action='store_true', help="anonymize the channel names")
parser.add_argument("-w", "--words-file", dest="words_file", default="/usr/share/dict/words",
                    help="file with words for anonymization")

args = parser.parse_args()
print("{} -> {}; anonymize={}, words_file={}".format(args.infile, args.outfile, args.anonymize, args.words_file))


def passthrough(arg):
    return arg


remap_names = passthrough

with open(args.infile, 'r') as infile:
    summary = json.load(infile)
    with open(args.outfile, 'w') as outfile:
        node_number = dict()
        nodes = list()

        if args.anonymize:
            remapper = NameRemapper \
                .from_words_file(args.words_file) \
                .for_names(summary["names"])
            remap_names = remapper.remap_names

        for name in remap_names(summary["names"]):
            node = {'name': name}
            node_number[name] = len(nodes)
            nodes.append(node)

        links = list()
        for (distance, pairs) in summary["distances"].items():
            for pair in pairs:
                (source, target) = remap_names(pair)
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
            for rank, link in enumerate(sorted(g, key=sort_by_distance)):
                link["source_rank"] = rank
                links_with_distance_rank.append(link)

        summary = {
            'nodes': nodes,
            'links': links_with_distance_rank}
        json.dump(summary, outfile, sort_keys=True, indent=4, separators=(',', ': '))
