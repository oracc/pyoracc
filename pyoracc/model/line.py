from mako.template import Template

class Line(object):
    template = Template("""${label}. \\
% for word in words:
${word} \\
% endfor 
% if lemmas:
\n#lem: \\
% for lemma in lemmas:
${lemma}; \\
% endfor \n
%endif
""", output_encoding='utf-8')


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
        return self.template.render_unicode(**vars(self))
    
    def serialize(self):
        return self.template.render_unicode(**vars(self))
