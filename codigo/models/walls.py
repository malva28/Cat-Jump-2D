"""
autor: Valentina Garrido
"""

class Walls:
    def __init__(self, leftBound, rightBound):
        self.leftBound = leftBound
        self.rightBound = rightBound
        self.delta = 0.001

    def leftCollide(self, cat):
        if cat.leftLim() <= self.leftBound + self.delta:
            # print("left keks")
            return True

    def rightCollide(self, cat):
        if cat.rightLim() >= self.rightBound - self.delta:
            # print("right keks")
            return True