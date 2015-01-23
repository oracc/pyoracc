from mako.template import Template

class Ruling(object):
    template = Template("""$ single ruling\n""")
    
    def __init__(self, count):
        self.count = count
        self.query = False
        self.broken = False
        self.remarkable = False
        self.collated = False
        
    def __str__(self):
        return self.template.render_unicode(**vars(self))
    
    def serialize(self):
        return self.template.render_unicode(**vars(self))
