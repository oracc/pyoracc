import os
import click
from stat import ST_MODE, S_ISREG

from pyoracc.atf.common.atffile import check_atf


def check_and_process(pathname, atftype, verbose=False):
    mode = os.stat(pathname)[ST_MODE]
    if S_ISREG(mode) and pathname.lower().endswith('.atf'):
        # It's a file, call the callback function
        if verbose:
            click.echo('Info: Parsing {0}.'.format(pathname))
        check_atf(pathname, atftype, verbose)


@click.command()
@click.option('--input_path', '-i',
              type=click.Path(exists=True, writable=True), prompt=True,
              required=True,
              help='Input the file/folder name.')
@click.option('--atf_type', '-f', type=click.Choice(['cdli', 'oracc']),
              prompt=True, required=True,
              help='Input the atf file type.')
@click.option('-v', '--verbose', default=False, required=False, is_flag=True,
              help='Enables verbose mode.')
@click.version_option()
def main(input_path, atf_type, verbose):
    """My Tool does one work, and one work well."""
    if os.path.isdir(input_path):
        failures = 0
        successes = 0
        with click.progressbar(os.listdir(input_path),
                               label='Info: Checking the files') as bar:
            for f in bar:
                pathname = os.path.join(input_path, f)
                try:
                    check_and_process(pathname, atf_type, verbose)
                    successes += 1
                    click.echo('Info: Correctly parsed {0}.'.format(pathname))
                except (SyntaxError, IndexError, AttributeError,
                        UnicodeDecodeError) as e:
                    failures += 1
                    click.echo("Info: Failed with message: {0} in {1}"
                               .format(e, pathname))
        click.echo("Failed with {0} out of {1} ({2}%)"
                   .format(failures, failures + successes,
                           failures * 100.0 / (failures + successes)))
    else:
        try:
            check_and_process(input_path, atf_type, verbose)
            click.echo('Info: Correctly parsed {0}.'.format(input_path))
        except (SyntaxError, IndexError, AttributeError,
                UnicodeDecodeError) as e:
            click.echo(
                "Info: Failed with message: {0} in {1}".format(e, input_path))
