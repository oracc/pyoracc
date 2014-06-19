from mako.template import Template


class Text(object):
    template = Template("&${code} = ${id}")

    def __init__(self):
        self.children = []
        self.composite = False
        self.links = []

    def __str__(self):
        return Text.template.render(**vars(self))
