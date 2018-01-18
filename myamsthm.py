#!/usr/bin/env python

"""
Matt's custom version of 
plasTeX.Package.amsthm.py
"""

import plasTeX


class swapnumbers(plasTeX.Command):
    pass


def ProcessOptions(options, document):
    context = document.context
    context.newenvironment("proof", 1, [
        u"\\par\\noindent{\\normalfont\\itshape #1.}\\enspace",
        r""
    ], opt = u"\\proofname")
    document.userdata.setPath('packages/amsthm/styles',{
        'plain' : {
            'name': 'plain',
            'above': u"0pt",
            'below': u"0pt",
            'bodyfont': u"\\itshape",
            'indentamount': u'0pt',
            'headfont': u"\\bfseries",
            'punctuation': u".",
            'between': u' ',
            'headspec': None
        },
        'definition' : {
            'name': 'definition',
            'above': u"0pt",
            'below': u"0pt",
            'bodyfont': u"",
            'indentamount': u'0pt',
            'headfont': u"\\bfseries",
            'punctuation': u".",
            'between': u' ',
            'headspec': None
        },
        'remark' : {
            'name': u'remark',
            'above': u'0pt',
            'below': u'0pt',
            'bodyfont': u"",
            'indentamount': '0pt',
            'headfont': u"\\bfseries",
            'punctuation': u".",
            'between': u' ',
            'headspec': None
        },

    })
    document.userdata.setPath('packages/amsthm/theorems',[])
    document.userdata.setPath('packages/amsthm/currentstyle', 'plain')



class theoremstyle(plasTeX.Command):
    args = 'style:str'
    def invoke(self, tex):
        self.parse(tex)
        self.ownerDocument.userdata.setPath('packages/amsthm/currentstyle', self.attributes['style'])


class newtheoremstyle(plasTeX.Command):
    args = 'name above below bodyfont indentamount headfont punctuation between headspec'
    def invoke(self, tex):
        self.parse(tex)
        d = self.ownerDocument.userdata.getPath("packages/amsthm/styles")
        s = {}
        for k, v in self.attributes.items():
            s[str(k)]=tex.source(v)
        d[tex.source(self.attributes['name'])] = s


class newtheorem(plasTeX.Command):
    args = ' * name:str [ shared:str ] header:str [ parent:str] '
    
    def invoke(self, tex):
        self.parse(tex)
        a = self.attributes
        name = str(a['name'])
        header = a['header']
        star = a['*modifier*'] == '*'
        parent = a['parent']
        shared = a['shared']
        style = self.ownerDocument.userdata.getPath('packages/amsthm/currentstyle')

        l = self.ownerDocument.userdata.getPath('packages/amsthm/theorems')
        l += [name]


        if star:
            thecounter = None
        else:
            if parent and not shared:
                self.ownerDocument.context.newcounter(name, initial=0, resetby=parent)
                self.ownerDocument.context.newcommand("the"+name, 0,
                                        "\\arabic{%s}.\\arabic{%s}"%(parent,name))
                thecounter = name
            elif shared:
                thecounter = shared
            else:
                thecounter = name
                self.ownerDocument.context.newcounter(name, initial=0)
                self.ownerDocument.context.newcommand("the"+name, 0, "\\arabic{%s}" %name)

        data = {
                'macroName': name,
                'counter': thecounter,
                'thehead': header,
                'thename': name,
                'labelable': True,
                'forcePars': True,
                'thestyle': style
            }
        th = type(name, (theoremCommand,), data)
        self.ownerDocument.context.addGlobal(name, th)


class theoremCommand(plasTeX.Environment):
    args = '[ note:chr ]'
    blockType = True
    
    def invoke(self, tex):
        # self.style['class'] = u'amsthm '+self.thename
        if self.macroMode == self.MODE_BEGIN:
            note = tex.readArgument('[]')
            if note:
                note = tex.source(note)
                print(note)
            super(theoremCommand, self).invoke(tex)
        elif self.macroMode == self.MODE_END:
            self.ownerDocument.context.pop(self)
            return

