from mako.template import Template

class Line(object):
    template = Template("""${label}. ${words}
#lem: ${lemmas}\n""")
    
    def __init__(self, label):
        self.label = label
        self.words = []
        self.lemmas = []
        self.witnesses = []
        self.translation = None
        self.notes = []
        self.references = []
        self.links = []
        
    def __str__(self):
        return self.template.render(**vars(self))
