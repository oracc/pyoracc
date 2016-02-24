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
