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
import sys


def _generate_parsetab():
    """
    Simple function to generate a parsetab file. This is done by creating a
    parser which automatically generates the parsetab file too.
    """
    from pyoracc.atf.atfyacc import AtfParser
    myparser = AtfParser()


def _pyversion():
    """
    Are we on Python 2 or 3
    Do this in an as simple as possible way to ensure that it works with old
    versions of Jython too.
    Jython does not use a named touple here so we have to just take the first
    element and not major as normal.
    """
    if sys.version_info[0] == 2:
        return 2
    else:
        return 3
