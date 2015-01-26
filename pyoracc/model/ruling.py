from mako.template import Template

class Ruling(object):
    template = Template("""\n$ ${type} ruling""")
    
    def __init__(self, count):
        self.count = count
        self.type = self.getRulingType()
        self.query = False
        self.broken = False
        self.remarkable = False
        self.collated = False
        
    def __str__(self):
        return self.template.render_unicode(**vars(self))
    
    def serialize(self):
        return self.template.render_unicode(**vars(self))
    
    def getRulingType(self):
        typeArr = [ "single", "double", "triple"]
        try:
            return typeArr[self.count - 1]
        except TypeError:
            print("Error: Ruling count " + self.count + " must be an integer.")
        except IndexError:
            print("Error: Ruling count (" + self.count + ") is out of bounds (" 
                  + typeArr.__len__() + ").")
            
      
