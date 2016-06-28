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


class OraccObject(object):

    template = Template(r"""@${objecttype}
% for child in children:
${child.serialize()}
% endfor""", output_encoding='utf-8')

    def __init__(self, objecttype):
        self.objecttype = objecttype
        self.children = []
        self.query = False
        self.broken = False
        self.remarkable = False
        self.collated = False

    def __str__(self):
        return OraccObject.template.render_unicode(**vars(self))

    def serialize(self):
        return OraccObject.template.render_unicode(**vars(self))
