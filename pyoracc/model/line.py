'''
Copyright 2015, 2016 University College London.

This file is part of PyORACC.

PyORACC is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PyORACC is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PyORACC. If not, see <http://www.gnu.org/licenses/>.
'''


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
% if links:
\n#link: \\
% for link in links:
${link};
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
