from plasTeX import Node
from plasTeX.DOM import Text
from plasTeX.Base.LaTeX import Math
# from collections import OrderedDict

PRIMITIVE_TYPES = [bool, str, int, float]

JSON_TYPES = [list, dict] + PRIMITIVE_TYPES


def maybe_value(n, prop):
    if hasattr(n, prop):
        value = getattr(n, prop)
        if value and (type(value) in JSON_TYPES or isinstance(value, Node)):
            return value
    return None


def isWhitespace(n):
    return isinstance(n, Text) and n.isElementContentWhitespace


def transform(x):
    # print("x: %s" % str(x))
    if isinstance(x, Node):
        return node(x)
    elif type(x) in PRIMITIVE_TYPES:
        return x
    elif isinstance(x, list):
        for y in x:
            print("\nNode: %s\nTransform: %s" % (str(y), str(transform(y))))
        # print("\nList: %s\n" % str(x))
        transformedList = [transform(y) for y in x if y]
        print("\nTransformed list: %s" % str(transformedList))
        return transformedList
    elif isinstance(x, dict):
        return {k: transform(x[k]) for k in x if x[k]}
    else:
        raise Exception("Unrecognized node type: {}".format(str(x)))


NODE_PROPS = ['nodeName', 'nodeType', 'id', 'counter',
              'attributes', 'ref', 'title', 'tocEntry']


def node(n):

    d = {}

    for prop in NODE_PROPS:
        value = maybe_value(n, prop)
        if value:
            d[prop] = transform(value)

    if isinstance(n, Text):
        # assert not n.isElementContentWhitespace
        d['isElementContentWhitespace'] = n.isElementContentWhitespace
        d['textContent'] = n.textContent

    elif isinstance(n, Math.MathEnvironment):
        d['childrenSource'] = n.childrenSource

    else:
        value = maybe_value(n, "childNodes")
        if value:
            d["childNodes"] = transform(value)

    return d

# NODE_TYPES = ['ELEMENT_NODE',
#               'ATTRIBUTE_NODE',
#               'TEXT_NODE',
#               'CDATA_SECTION_NODE',
#               'ENTITY_REFERENCE_NODE',
#               'ENTITY_NODE',
#               'PROCESSING_INSTRUCTION_NODE',
#               'COMMENT_NODE',
#               'DOCUMENT_NODE',
#               'DOCUMENT_TYPE_NODE',
#               'DOCUMENT_FRAGMENT_NODE',
#               'NOTATION_NODE']


# TEST
# from plasTeX.TeX import TeX
# import json

# source = r'''
# $\int_a^b \frac{f\prime(x)}{f(x)}dx=\log\left(\frac{f(b)}{f(a)}\right)$'''
# tex = TeX()
# tex.input(source)
# document = tex.parse()
# document.normalizeDocument()
# print(json.dumps(transform(document), indent=4))
