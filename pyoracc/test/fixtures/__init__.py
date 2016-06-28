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
import os
import codecs
import time
import re

here = os.path.abspath(__file__)


def belsunu():
    return codecs.open(os.path.join(
                       os.path.dirname(here), 'tiny_corpus', "belsunu.atf"),
                       encoding='utf-8').read()


def tiny_corpus():
    return os.path.join(os.path.dirname(here), 'tiny_corpus')


def sample_corpus():
    return os.path.join(os.path.dirname(here), 'sample_corpus')


def whole_corpus():
    """
    Return the path to the full oracc corpus. This is not bundled with
    pyoracc and only works if the environmental variable oracc_corpus_path
    is set to the correct directory.
    """
    try:
        oracc_corpus_path = os.environ['oracc_corpus_path']
    except KeyError:
        oracc_corpus_path = None
    return oracc_corpus_path


def anzu():
    return sample_file("anzu")


def sample_file(name):
    return codecs.open(os.path.join(
                       os.path.dirname(here), 'sample_corpus', name + ".atf"),
                       encoding='utf-8-sig').read()


def output_folder():
    output = os.path.join(os.path.dirname(here), 'output')
    if not os.path.isdir(output):
        os.makedirs(output)
    return output


def output_filepath(atf_filename):
    atf_without_ext = re.sub('.atf$', '', atf_filename)
    return os.path.join(output_folder(), atf_without_ext + "_" +
                        time.strftime("%Y%m%d%H%M%S") + ".atf")
# return os.path.join(output_folder(), atf_filename)
