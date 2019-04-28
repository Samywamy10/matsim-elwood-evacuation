import xml.etree.ElementTree as ET

class XmlElement:
    def __init__(self, elementName):
        self.xmlElement = ET.Element(elementName)
    
    def getXml(self):
        return self.xmlElement

    def addSubElement(self, subElement):
        self.xmlElement.append(subElement)

    def getTree(self):
        return ET.ElementTree(self.xmlElement)

    def writeTreeToFile(self, filename, header2 = ''):
        tree = self.getTree()
        header1 = '<?xml version="1.0" encoding="utf-8"?>'
        tree.write(filename)
        with open(filename, 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            f.write(header1 + '\n' + header2 + '\n')
            f.write(content)