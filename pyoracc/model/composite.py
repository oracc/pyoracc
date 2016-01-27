from mako.template import Template

class Composite(object):
   
    template = Template(
"""% for text in texts:
${text.serialize_composite()}
% endfor""")
    
    def __init__(self):
        self.texts = []
    
    def __str__(self):
        return Composite.template.render_unicode(**vars(self))
    
    def serialize(self):
        return Composite.template.render_unicode(**vars(self))
    
# 
#     def objects(self):
#         return [x for x in self.children if isinstance(x, OraccObject)]
