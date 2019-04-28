from coordinate import Coordinate
from shape import Shape

class Network(Shape):
    def __init__(self, networkXml):
        Shape.__init__(self)
        self.networkXml = networkXml
        self.__initNetwork()
        self.__calculateMinAndMax()
    
    def __initNetwork(self):
        self.root = self.networkXml.getroot()

    def __calculateMinAndMax(self):
        for child in self.root.iter('node'):
            self.min.x = min(float(child.attrib['x']),self.min.x)
            self.min.y = min(float(child.attrib['y']),self.min.y)
            self.max.x = max(float(child.attrib['x']),self.max.x)
            self.max.y = max(float(child.attrib['y']),self.max.y)