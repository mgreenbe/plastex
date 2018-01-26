""" parses a LaTeX to a JSON tree, using plasTeX """

import sys
import argparse
import json
from plasTeX.TeX import TeX
from plasTeX import Node, TeXFragment
from plasTeX.Tokenizer import Space
from plasTeX.DOM import Text


def is_parsable(x):
    return isinstance(x, Node) or isinstance(x, dict) or isinstance(x, list) or isinstance(x, str) or isinstance(x, int) or isinstance(x, float)


node_attrs = ['attributes', 'childNodes', 'counter', 'id',
              'nodeName', 'nodeType', 'ref', 'title', 'tocEntry']

math_node_attrs = ['nodeName', 'nodeType', 'source']

text_node_attrs = ['isElementContentWhitespace',
                   'nodeName', 'nodeType', 'textContent']


def inner_source(n):
    """ concatenated source of the proper children of n """
    if n.childNodes:
        return ''.join([inner_source(child) for child in n.childNodes])
    else:
        return n.source


def good_attr(n, a):
    """ determines whether an attribute exists on a node and is parsable """
    return hasattr(n, a) and getattr(n, a) and is_parsable(getattr(n, a))


def parse_node(n, attrs):
    """ parses a node to a dict """
    return {a: parse(getattr(n, a)) for a in attrs if good_attr(n, a)}


def is_whitespace_node(n):
    """ determines whether a node is whitespace """
    return isinstance(n, Space) or (isinstance(n, Text) and n.isElementContentWhitespace)


def parse(x):
    """ parse something """
#    if is_whitespace_node:
#        pass
    if isinstance(x, Text):
        return {a: getattr(x, a) for a in text_node_attrs if good_attr(x, a)}
    elif isinstance(x, Node) and (x.nodeName == "math" or x.nodeName == "displaymath"):
        print('% s: % s\n' % (x.nodeName, inner_source(x)))
        return parse_node(x, math_node_attrs)
    elif isinstance(x, Node):
        return parse_node(x, node_attrs)
    elif isinstance(x, dict):
        return {key: parse(x[key]) for key in x if is_parsable(x[key]) and key != 'self'}
    elif isinstance(x, list):
        return [z for z in [parse(y) for y in x if is_parsable(y)] if z]
    elif isinstance(x, str) or isinstance(x, int) or isinstance(x, float):
        return x
    else:
        raise TypeError("I don't know how to parse %s" % str(x))


NODE_TYPES = ['ELEMENT', 'ATTRIBUTE', 'TEXT', 'CDATA_SECTION', 'ENTITY_REFERENCE', 'ENTITY',
              'PROCESSING_INSTRUCTION', 'COMMENT', "DOCUMENT", "DOCUMENT_TYPE", "DOCUMENT_FRAGMENT", "NOTATION"]


def printTextNode(node, p):
    p('textContent: "{}"'.format(node.textContent))


def printDict(dct, p):
    for key in dct:
        p("{}: {}".format(key, dct[key]))


def printNode(node, indent=4, depth=0, count={"count": 0}):
    def p(s): print(" " * indent * depth + s)
    old_count = count['count']
    count['count'] = old_count + 1
    print("{}{}. nodeName: {}".format(
        " " * indent * depth, old_count, node.nodeName))
    p("nodeType: {}".format(NODE_TYPES[node.nodeType - 1]))
    if node.nodeName == "#text":
        printTextNode(node, p)
    if node.nodeName == "math":
        p("source: {}".format(
            ''.join([child.source for child in node.childNodes])))
    if hasattr(node, "attributes") and node.attributes:
        d = {key + "_attr": node.attributes[key]
             for key in node.attributes if key != "self"}
        if d:
            for key in d:
                if isinstance(d[key], Node):
                    p(key + ":")
                    printNode(d[key], indent=indent,
                              depth=depth + 1, count=count)
                else:
                    p("{}: {}".format(key, d[key]))

    if node.nodeName != "math" and node.childNodes:
        p("childNodes:")
        for child in node.childNodes:
            printNode(child, indent=indent, depth=depth + 1, count=count)

# infile = open('lab2.tex', 'r')
# source = infile.read()
# infile.close()
# doc = TeX().input(source).parse()
# tree = parse(doc)

# outfile = open('tree.json', 'w')
# outfile.write(json.dumps(tree))
# outfile.close()


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
        doc.normalize()
        # tree = parse(doc)
    if args.outfile:
        with open(args.outfile, 'w', encoding='utf8') as outfile:
            outfile.write(json.dumps(tree))
    else:
        printNode(doc, count={"count": 0})
else:
    while True:
        source = input("> ")
        if source:
            doc = TeX().input(source).parse()
            doc.normalize()
            # print(doc.toXML())
            printNode(doc, count={"count": 0})
        else:
            break
