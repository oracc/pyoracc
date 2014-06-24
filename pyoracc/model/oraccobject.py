class OraccObject(object):
    def __init__(self, objecttype):
        self.objecttype = objecttype
        self.children = []
        self.query = False
        self.broken = False
        self.remarkable = False
        self.collated = False
