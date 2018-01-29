from plasTeX import Node
from plasTeX.DOM import Text
from plasTeX.Base.LaTeX import Math
from collections import OrderedDict

PRIMITIVE_TYPES = [bool, str, int, float]

JSON_TYPES = [list, dict] + PRIMITIVE_TYPES

NODE_PROPS = ['nodeName', 'nodeType', 'id', 'counter',
              'args', 'attributes', 'ref', 'title', 'tocEntry']


def isWhitespace(n):
    if isinstance(n, str):
        return n.strip() == ''
    if isinstance(n, Node) and n.nodeType == 3:
        return n.isElementContentWhitespace


def transform(x):
    if isinstance(x, Node):
        return node(x)
    elif type(x) in PRIMITIVE_TYPES:
        return x
    elif isinstance(x, list):
        return [transform(y) for y in x if y is not None
                and not isWhitespace(x)]
    elif isinstance(x, dict):
        return {k: transform(x[k]) for k in x if x[k] is not None
                and not isWhitespace(x)}
    else:
        raise Exception("Unrecognized node type: {}".format(str(x)))


def node(n):
    d = []

    for prop in NODE_PROPS:
        value = getattr(n, prop) if hasattr(n, prop) else None
        if any([isinstance(value, t) for t in JSON_TYPES + [Node]]):
            d.append((prop, transform(value)))

    if isinstance(n, Text):

        assert not n.isElementContentWhitespace
        d.append(('textContent', str(n)))

    elif isinstance(n, Math.MathEnvironment):
        d.append(('childrenSource', n.childrenSource))

    else:
        children = getattr(n, "childNodes") \
                        if hasattr(n, "childNodes") else None
        if children:
            filtered_children = [
                child for child in children if not isWhitespace(child)
            ]
            d.append(("childNodes", transform(filtered_children)))

    return OrderedDict(d)
