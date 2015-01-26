from mako.template import Template

class Note(object):
    template = Template("""\\
% if references:
% for reference in references:
@note ^${reference}^ ${content} 
% endfor
% else:
#note: ${content}
% endif""")

    def __init__(self, content=""):
        self.content = content
        self.references = []
    
    def serialize(self):
        return self.template.render_unicode(**vars(self))
