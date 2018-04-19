pyoracc
=======

[![Build Status](https://travis-ci.org/cdli-gh/pyoracc.svg?branch=master)](https://travis-ci.org/cdli-gh/pyoracc) 
[![Maintainability](https://api.codeclimate.com/v1/badges/7244ac087b45146c5e3e/maintainability)](https://codeclimate.com/github/cdli-gh/pyoracc/maintainability)
[![codecov](https://codecov.io/gh/cdli-gh/pyoracc/branch/master/graph/badge.svg)](https://codecov.io/gh/cdli-gh/pyoracc)

Python tools for working with ORACC

Depends on PLY, Mako and Pytest

# Installation

If you don't use `pip`, you're missing out.
Here are [installation instructions](https://pip.pypa.io/en/stable/installing/).

Simply run:

```bash
    $ cd pyoracc
    $ git pull origin master
    $ pip install .
```

Or you can just do

    $ pip install git+git://github.com/cdli-gh/pyoracc.git 

Or you can also do

    $ pip install git+https://github.com/cdli-gh/pyoracc.git 


# Upgrading

If you already have installed it and want to upgrade the tool:

```bash
    $ cd pyoracc
    $ git pull origin master
    $ pip install . --upgrade
```

Or you can just do

    $ pip install git+git://github.com/cdli-gh/pyoracc.git --upgrade

Or you can also do

    $ pip install git+https://github.com/cdli-gh/pyoracc.git --upgrade


# Usage

To use it:

    $ pyoracc --help

*Only files with the .atf extension can be processed.  *
 
To run it on file:

    $ pyoracc -i ./pyoracc/test/data/cdli_atf_20180104.atf -f cdli

For a fresh copy of CDLI ATF, download the data bundle here : https://github.com/cdli-gh/data/blob/master/cdliatf_unblocked.atf

To run it on oracc file:

    $ pyoracc -i ./pyoracc/test/data/cdli_atf_20180104.atf -f oracc

To run it on folder:

    $ pyoracc -i ./pyoracc/test/data -f cdli

To see the console messages of the tool, use --verbose switch

    $ pyoracc -i ./pyoracc/test/data -f cdli --verbose
    
Note that using the verbose option will also create a parselog.txt file, 
containing the log output along with displaying it on command line. 
The verbose output contains the lexical symbols, the parse grammer table
and the LR parsing table states.

Also note that, first time usage with any atf format will always display 
the parse tables irrespective of verbose switch.

If you don't give arguments, it will prompt for the path and atf file type.  

# Help

```bash
$ pyoracc --help
Usage: pyoracc [OPTIONS]

  My Tool does one work, and one work well.

Options:
  -i, --input_path PATH      Input the file/folder name.  [required]
  -f, --atf_type [cdli|atf]  Input the atf file type.  [required]
  -v, --verbose              Enables verbose mode
  --version                  Show the version and exit.
  --help                     Show this message and exit.

```

## Internal Dev Usage

### To run on directory

    $ python  -m pyoracc.model.corpus ./pyoracc/test/data  cdli

### To run on individual file

    $ python -m pyoracc.atf.common.atffile ./pyoracc/test/data/cdli_atf_20180104.atf cdli True

## Running Tests

Before running pytest and coverage, install [py.test](https://docs.pytest.org/en/latest/getting-started.html) and [pytest-cov](https://pypi.org/project/pytest-cov/).

    $ py.test --cov=pyoracc --cov-report xml --cov-report html --cov-report annotate --runslow
    
## API Consumption

```python
from pyoracc.atf.common.atffile import file_process
file_process(pathname, atftype, verbose)
```
