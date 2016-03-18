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
        super(MyBuildPy, self).run()

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
