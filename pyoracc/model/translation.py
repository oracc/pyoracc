from mako.template import Template


class Translation(object):
    # TODO: the type of translation (parallel, labelled,  is going to be
    # recorded as text metadata (like the atf protocols, etc), as it's a
    # property of the textual representation and not the object itself. Left
    # "parallel" hardcoded by now.
    template = Template("""@translation parallel en project
% for child in children:
${child.serialize()}
% endfor""")

    def __init__(self):
        self.children = []

    def __str__(self):
        return self.template.render_unicode(**vars(self))

    def serialize(self):
        return self.template.render_unicode(**vars(self))
