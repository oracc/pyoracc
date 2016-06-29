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


class Ruling(object):
    template = Template("""\n$ ${type} ruling""")

    def __init__(self, count):
        self.count = count
        self.type = self.getRulingType()
        self.query = False
        self.broken = False
        self.remarkable = False
        self.collated = False

    def __str__(self):
        return self.template.render_unicode(**vars(self))

    def serialize(self):
        return self.template.render_unicode(**vars(self))

    def getRulingType(self):
        typeArr = ["single", "double", "triple"]
        try:
            return typeArr[self.count - 1]
        except TypeError:
            print("Error: Ruling count " + self.count + " must be an integer.")
        except IndexError:
            print("Error: Ruling count (" +
                  self.count +
                  ") is out of bounds (" +
                  typeArr.__len__() + ").")
