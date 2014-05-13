import os

here=os.path.abspath(__file__)
def belsunu():
  return open(os.path.join(os.path.dirname(here),"belsunu.atf")).read()
