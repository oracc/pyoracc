import os
import codecs

here = os.path.abspath(__file__)


def belsunu():
    return codecs.open(os.path.join(
                       os.path.dirname(here), "belsunu.atf"),
                       encoding='utf-8').read()
