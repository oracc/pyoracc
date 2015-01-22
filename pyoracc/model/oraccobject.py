from mako.template import Template

class OraccObject(object):
    
    template = Template("""@${objecttype}\n
% for child in children:
${child}
% endfor""")
    
    def __init__(self, objecttype):
        self.objecttype = objecttype
        self.children = []
        self.query = False
        self.broken = False
        self.remarkable = False
        self.collated = False
        
    def __str__(self):
        return OraccObject.template.render(**vars(self))
    
