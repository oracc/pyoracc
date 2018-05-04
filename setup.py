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

from setuptools import find_packages, setup
from setuptools.command.build_py import build_py

# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

dependencies = ['click', 'mako', 'ply']

extra_dependencies = ['pytest', 'pytest-cov', 'codecov', 'pycodestyle']


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
      version='0.1.0',
      author='UCL Research IT Services',
      author_email='rc-softdev@ucl.ac.uk',
      description='Python tools for working with ORACC/CDLI ATF files',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/ucl/pyoracc',
      download_url='https://github.com/ucl/pyoracc/archive/master.tar.gz',
      license='GPLv3',
      packages=find_packages(exclude=["*.test", "*.test.*", "test.*", "test"]),
      install_requires=dependencies,
      extras_require={  # Optional
          'dev': extra_dependencies,
          'test': extra_dependencies,
      },
      zip_safe=False,
      cmdclass=dict(build_py=MyBuildPy),
      entry_points={
          'console_scripts': [
              'pyoracc = pyoracc.wrapper.cli:main',
          ],
      },
      classifiers=[
          # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
          # 'Development Status :: 1 - Planning',
          # 'Development Status :: 2 - Pre-Alpha',
          # 'Development Status :: 3 - Alpha',
          # 'Development Status :: 4 - Beta',
          'Development Status :: 5 - Production/Stable',
          # 'Development Status :: 6 - Mature',
          # 'Development Status :: 7 - Inactive',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Operating System :: POSIX',
          'Operating System :: MacOS',
          'Operating System :: Unix',
          'Operating System :: Microsoft :: Windows',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Utilities'
      ],
      keywords='oracc cdli atf cuneiform parser',  # Optional
      project_urls={  # Optional
          'Bug Reports': 'https://github.com/oracc/pyoracc/issues',
          'Donating!': 'http://oracc.museum.upenn.edu/doc/about/contributing/',
          'Help!': 'http://oracc.museum.upenn.edu/doc/help/index.html',
          'Source': 'https://github.com/oracc/pyoracc/',
      },
      python_requires='>=2.6, !=3.0.*, !=3.1.*, !=3.2.*, <4'
      )
