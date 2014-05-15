from mako.template import Template

class Text(object):
  template=Template("&${code} = ${id}")
  def __init__(self):
    self.children=[]

  def __str__(self):
    return Text.template.render(**vars(self))
