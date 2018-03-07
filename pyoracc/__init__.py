import sys


def _generate_parsetab():
    """
    Simple function to generate a parsetab file. This is done by creating a
    parser which automatically generates the parsetab file too.
    """
    from pyoracc.atf.common.atfyacc import AtfParser
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
