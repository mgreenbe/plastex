from plasTeX import Node
from plasTeX.DOM import Text
from plasTeX.Base.LaTeX import Math
from collections import OrderedDict

PRIMITIVE_TYPES = [bool, str, int, float]

JSON_TYPES = [list, dict] + PRIMITIVE_TYPES


def maybe_value(n, prop):
    if hasattr(n, prop):
        value = getattr(n, prop)
        if value and (type(value) in JSON_TYPES or isinstance(value, Node)):
            return value
    return None


def transform(x):
    if isinstance(x, Node):
        return node(x)
    elif type(x) in PRIMITIVE_TYPES:
        return x
    elif isinstance(x, list):
        return [transform(y) for y in x if y]
    elif isinstance(x, dict):
        return {k: transform(x[k]) for k in x if x[k]}
    else:
        raise Exception("Unrecognized node type: {}".format(str(x)))


NODE_PROPS = ['nodeName', 'nodeType', 'id', 'counter',
              'attributes', 'ref', 'title', 'tocEntry']


def node(n):

    d = []

    for prop in NODE_PROPS:
        value = maybe_value(n, prop)
        if value:
            d.append((prop, transform(value)))

    if isinstance(n, Text):
        d.append(('isElementContentWhitespace', n.isElementContentWhitespace))
        d.append(('textContent', n.textContent))

    elif isinstance(n, Math.MathEnvironment):
        d.append(('childrenSource', n.childrenSource))

    else:
        value = maybe_value(n, "childNodes")
        if value:
            d.append(("childNodes", transform(value)))

    return OrderedDict(d)

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
