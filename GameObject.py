import math, pygame

class GameObject():
    def __init__(self, pos):
        self.pos = pos

    def getDirectionTo(self, target):
        return math.atan2(target.pos[1] - self.pos[1], target.pos[0] - self.pos[0])
    
    def getDistanceTo(self, target):
        return math.sqrt((target.pos[1] - self.pos[1])**2 + (target.pos[0] - self.pos[0])**2)