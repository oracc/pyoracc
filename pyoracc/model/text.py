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
from .oraccobject import OraccObject


class Text(object):
    template = Template("""&${code} = ${description}
#project: ${project}
#atf: lang ${language}
% for child in children:
${child.serialize()}
% endfor""")

    def __init__(self):
        self.children = []
        self.composite = False
        self.links = []
        self.score = None
        self.code = None
        self.description = None
        self.project = None
        self.language = None

    def __str__(self):
        return Text.template.render_unicode(**vars(self))

    def serialize(self):
        return Text.template.render_unicode(**vars(self))

    def objects(self):
        return [x for x in self.children if isinstance(x, OraccObject)]
