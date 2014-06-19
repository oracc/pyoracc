import os
import codecs

here = os.path.abspath(__file__)


def belsunu():
    return codecs.open(os.path.join(
                       os.path.dirname(here), 'tiny_corpus', "belsunu.atf"),
                       encoding='utf-8').read()


def tiny_corpus():
    return os.path.join(os.path.dirname(here), 'tiny_corpus')


def anzu():
    return sample_file("anzu")


def sample_file(name):
    return codecs.open(os.path.join(
                       os.path.dirname(here), 'sample_corpus', name + ".atf"),
                       encoding='utf-8').read()
