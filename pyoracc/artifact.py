from mako.template import Template

class Artifact(object):
  template=Template("&${code} = ${id}")
  def __init__(self):
    pass

  def __str__(self):
    return Artifact.template.render(**vars(self))
