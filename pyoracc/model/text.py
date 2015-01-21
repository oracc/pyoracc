from mako.template import Template
from oraccobject import OraccObject


class Text(object):
    template = Template(
    """
    &${code} = ${description}
    """)
#  template = Template(
#     """
#     &${code} = ${id}
#     %for child in children:
#        ${child}
#     %endfor
#     """)
#  
    
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
        return Text.template.render(**vars(self))

    def objects(self):
        return [x for x in self.children if isinstance(x, OraccObject)]
