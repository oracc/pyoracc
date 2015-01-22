from mako.template import Template

class Translation(object):
    template = Template("""% for child in children:
${child}
% endfor""")    

    
    def __init__(self):
        self.children = []
        
#     def __str__(self):
#         return self.template.render(**vars(self))
