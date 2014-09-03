from mako.template import Template
from oraccobject import OraccObject

class Text(object):
    template = Template("&${code} = ${id}")

    def __init__(self):
        self.children = []
        self.composite = False
        self.links = []

    def __str__(self):
        return Text.template.render(**vars(self))

    def objects(self):
        return [x for x in self.children if isinstance(x,OraccObject)]
