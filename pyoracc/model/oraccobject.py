from mako.template import Template

class OraccObject(object):
    
    template = Template(
"""% if len(objecttype):
@${objecttype}
% endif
% for child in children:
${child.serialize()}
% endfor""", output_encoding='utf-8')
    
    def __init__(self, objecttype):
        self.objecttype = objecttype
        self.children = []
        self.query = False
        self.broken = False
        self.remarkable = False
        self.collated = False
        
    def __str__(self):
        return OraccObject.template.render_unicode(**vars(self))
    
    def serialize(self):
        return OraccObject.template.render_unicode(**vars(self))
    
