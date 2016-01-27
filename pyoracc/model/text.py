from mako.template import Template
from oraccobject import OraccObject


class Text(object):
    template = Template(
"""&${code} = ${description}
#project: ${project}
#atf: lang ${language}
% for child in children:
${child.serialize()}
% endfor""")
    
    composite_template = Template(
"""&${code} = ${description}
@composite
#project: ${project}
#atf: lang ${language}
% for child in children:
${child.serialize()}
% endfor""")
    
    def __init__(self):
        self.children = []
        self.composite = False
        self.links = []
        self.score = None
        self.code = None
        self.description = None
        self.project = None
        self.language = None

    def __str__(self):
        return Text.template.render_unicode(**vars(self))
    
    def serialize(self):
        return Text.template.render_unicode(**vars(self))

    def serialize_composite(self):
        return Text.composite_template.render_unicode(**vars(self))

    def objects(self):
        return [x for x in self.children if isinstance(x, OraccObject)]
