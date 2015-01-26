from mako.template import Template

class Comment(object):
    template = Template("""# ${content}""")
    
    def __init__(self, content):
        self.content = content
        self.check = False

    def __str__(self):
        return self.template.render_unicode(**vars(self))
    
    def serialize(self):
        return self.template.render_unicode(**vars(self))