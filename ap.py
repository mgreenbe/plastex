import argparse
import sys
parser = argparse.ArgumentParser()
parser.add_argument("infile", help="the file to read from",
                    type=str, nargs="?")
parser.add_argument("outfile", help="the file to write to",
                    type=str, nargs="?")
args = parser.parse_args()

if args.infile:
    with open(args.infile, 'r', encoding='utf8') as infile:
        source = infile.read()
    if args.outfile:
        with open(args.outfile, 'w', encoding='utf8') as outfile:
            outfile.write(source.upper())
    else:
        sys.stdout.write(source.upper())
else:
    while True:
        source = input("> ")
        if source:
            print("\n%s\n" % source.upper())
        else:
            break
