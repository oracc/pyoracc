from mako.template import Template

class State(object):
    template = Template("""$ \\
% if scope:
${scope} \\
% endif    
% if state:
${state}\\
% elif scope:
${scope}\\
% elif extent:
${extent}\\
% elif qualification:
${qualification}\\
% elif loose:
${loose}\\
% endif
""")    
    
    def __init__(self, state=None, scope=None, extent=None,
                 qualification=None, loose=None):
        self.state = state
        self.scope = scope
        self.extent = extent
        self.qualification = qualification
        self.loose = loose
        
    def __str__(self):
        return self.template.render_unicode(**vars(self))
    
    def serialize(self):
        return self.template.render_unicode(**vars(self))
