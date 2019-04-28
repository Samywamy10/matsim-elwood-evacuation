from coordinate import Coordinate
import random
import math

class Shape:
    def __init__(self):
        self.min = Coordinate(math.inf,math.inf)
        self.max = Coordinate(-math.inf,-math.inf)

    def getRandomPosition(self):
        return Coordinate(random.uniform(self.min.x, self.max.x), random.uniform(self.min.y, self.max.y))

    @staticmethod
    def getClosestShapeFromCoordinate(startCoordinate, shapes):
        closestDistance = math.inf
        closestDistanceShape = shapes[0]
        for shape in shapes:
            toMinPointDistance = Coordinate.distanceBetweenPoints(startCoordinate, shape.min)
            toMaxPointDistance = Coordinate.distanceBetweenPoints(startCoordinate, shape.max)
            if toMinPointDistance < closestDistance or toMaxPointDistance < closestDistance:
                closestDistance = min(toMinPointDistance, toMaxPointDistance)
                closestDistanceShape = shape
        return closestDistanceShape

class Polygon(Shape):
    def __init__(self,topLeft,topRight,bottomLeft,bottomRight):
        Shape.__init__(self)
        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight
        self.__calculateMinAndMax()
    
    def __calculateMinAndMax(self):
        #topLeft
        self.min.x = min(self.topLeft.x, self.min.x)
        self.max.x = max(self.topLeft.x, self.max.x)
        self.min.y = min(self.topLeft.y, self.min.y)
        self.max.y = max(self.topLeft.y, self.max.y)

        #topRight
        self.min.x = min(self.topRight.x, self.min.x)
        self.max.x = max(self.topRight.x, self.max.x)
        self.min.y = min(self.topRight.y, self.min.y)
        self.max.y = max(self.topRight.y, self.max.y)

        #bottomLeft
        self.min.x = min(self.bottomLeft.x, self.min.x)
        self.max.x = max(self.bottomLeft.x, self.max.x)
        self.min.y = min(self.bottomLeft.y, self.min.y)
        self.max.y = max(self.bottomLeft.y, self.max.y)

        #bottomRight
        self.min.x = min(self.bottomRight.x, self.min.x)
        self.max.x = max(self.bottomRight.x, self.max.x)
        self.min.y = min(self.bottomRight.y, self.min.y)
        self.max.y = max(self.bottomRight.y, self.max.y)