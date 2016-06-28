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


class Translation(object):
    # TODO: the type of translation (parallel, labelled,  is going to be
    # recorded as text metadata (like the atf protocols, etc), as it's a
    # property of the textual representation and not the object itself. Left
    # "parallel" hardcoded by now.
    template = Template("""@translation parallel en project
% for child in children:
${child.serialize()}
% endfor""")

    def __init__(self):
        self.children = []

    def __str__(self):
        return self.template.render_unicode(**vars(self))

    def serialize(self):
        return self.template.render_unicode(**vars(self))
