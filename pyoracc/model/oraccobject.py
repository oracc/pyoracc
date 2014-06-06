class OraccObject(object):
    def __init__(self, objecttype):
        self.objecttype = objecttype
        self.children = []
        self.prime = False
        self.query = False
        self.broken = False
        self.remarkable = False
        self.collated = False
