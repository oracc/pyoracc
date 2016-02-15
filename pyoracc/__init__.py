def _generate_parsetab():
    """
    Simple function to generate a parsetab file. This is done by creating a
    parser which automatically generates the parsetab file too.
    """
    from pyoracc.atf.atfyacc import AtfParser
    myparser = AtfParser()
