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


from setuptools import setup
from setuptools.command.build_py import build_py


class MyBuildPy(build_py):
    """We subclass build_py so that we can run _generate_parsetab after
       installing the dependencies (Ply and Mako)"""
    def run(self):
        """Generate the parsetab file so that we can install that too before
        calling the regular installer in the super class"""
        from pyoracc import _generate_parsetab
        _generate_parsetab()
        # Can't use super because build_py is an old style class in the Maven
        # Jython plugin setuptools version 0.6...
        build_py.run(self)

setup(name='pyoracc',
      version='0.0.1',
      author='James Hetherington',
      author_email='j.hetherington@ucl.ac.uk',
      url='https://github.com/ucl/pyoracc',
      download_url='https://github.com/ucl/pyoracc/archive/master.tar.gz',
      packages=['pyoracc',
                'pyoracc/atf',
                'pyoracc/model',
                'pyoracc/test',
                'pyoracc/test/atf',
                'pyoracc/test/fixtures'],
      install_requires=['mako', 'ply'],
      setup_requires=['mako', 'ply'],
      package_data={'pyoracc': ['test/fixtures/*/*.atf']},
      zip_safe=False,
      cmdclass=dict(build_py=MyBuildPy)
      )
