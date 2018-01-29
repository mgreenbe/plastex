""" parses a LaTeX to a JSON tree, using plasTeX """

import argparse
import json
from plasTeX.TeX import TeX
from transform import transform


parser = argparse.ArgumentParser()
parser.add_argument("infile", help="the file to read from",
                    type=str, nargs="?")
parser.add_argument("outfile", help="the file to write to",
                    type=str, nargs="?")
args = parser.parse_args()

if args.infile:
    with open(args.infile, 'r', encoding='utf8') as infile:
        source = infile.read()
        doc = TeX().input(source).parse()
        print(doc)
        doc.normalizeDocument()
        tree = json.dumps(transform(doc), indent=4)
    if args.outfile:
        with open(args.outfile, 'w', encoding='utf8') as outfile:
            outfile.write(tree)
    else:
        print(tree)
else:
    while True:
        source = input("> ")
        if source:
            doc = TeX().input(source).parse()
            # doc.normalizeDocument()
            tree = json.dumps(transform(doc), indent=4)
            print(tree)
        else:
            break
