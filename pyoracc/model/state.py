from mako.template import Template

class State(object):
    template = Template("""$ ${loose}""")    
    
    def __init__(self, state=None, scope=None, extent=None,
                 qualification=None, loose=None):
        self.state = state
        self.scope = scope
        self.extent = extent
        self.qualification = qualification
        self.loose = loose
        
    def __str__(self):
        return self.template.render(**vars(self))
