import math

class Coordinate:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    
    @staticmethod
    def distanceBetweenPoints(coordinate1, coordinate2):
        return math.sqrt((coordinate2.x - coordinate1.x)**2 + (coordinate2.y - coordinate1.y)**2)