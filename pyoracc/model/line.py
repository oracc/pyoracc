from mako.template import Template

class Line(object):
    template = Template("""\n${label}.\t\\
${' '.join(words)}\\
% if references:
% for reference in references:
^${reference}^ 
% endfor
% endif
% if lemmas:
\n#lem:\\
${'; '.join(lemmas)}\\
% endif
% if notes:
\n
% for note in notes:
${note.serialize()}
% endfor
% endif
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
