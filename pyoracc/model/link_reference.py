class LinkReference(object):
    def __init__(self, operator, target):
        self.label = []
        self.rangelabel = []
        self.plus = False
        self.operator = operator
        self.target = target
