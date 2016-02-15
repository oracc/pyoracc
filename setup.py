from distutils.core import setup

# Generate the parsetab file so that we can install that too
# from pyoracc import _generate_parsetab
# _generate_parsetab()

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
      package_data={'pyoracc': ['test/fixtures/*/*.atf']}
      )
