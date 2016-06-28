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


class State(object):
    template = Template("""$ \\
% if scope:
${scope} \\
% endif
% if state:
${state}\\
% elif scope:
${scope}\\
% elif extent:
${extent}\\
% elif qualification:
${qualification}\\
% elif loose:
${loose}\\
% endif
""")

    def __init__(self, state=None, scope=None, extent=None,
                 qualification=None, loose=None):
        self.state = state
        self.scope = scope
        self.extent = extent
        self.qualification = qualification
        self.loose = loose

    def __str__(self):
        return self.template.render_unicode(**vars(self))

    def serialize(self):
        return self.template.render_unicode(**vars(self))
