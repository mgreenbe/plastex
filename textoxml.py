import sys
import argparse
from plasTeX.TeX import TeX
from xml.dom.minidom import parseString


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
        doc.normalizeDocument()
        xml = doc.toXML()

    if args.outfile:
        with open(args.outfile, 'w', encoding='utf8') as outfile:
            outfile.write(xml)
    else:
        sys.stdout.write(parseString(xml).toprettyxml())
else:
    while True:
        source=input("> ")
        print(source)
        if source:
            doc=TeX().input(source).parse()
            doc.normalizeDocument()
            xml=doc.toXML()
            print(parseString(xml).toprettyxml(indent="    "))
        else:
            break
