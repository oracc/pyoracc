from .oraccobject import OraccObject


class OraccNamedObject(OraccObject):
    def __init__(self, objecttype, name):
        super(OraccNamedObject, self).__init__(objecttype)
        self.name = name
