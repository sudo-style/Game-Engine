import math, pygame

class GameObject():
    def __init__(self, pos):
        self.pos = pos

    def getDirectionTo(self, target):
        return math.atan2(target.pos[1] - self.pos[1], target.pos[0] - self.pos[0])
    
    def getDistanceTo(self, target):
        return math.sqrt((target.pos[1] - self.pos[1])**2 + (target.pos[0] - self.pos[0])**2)
    
    # calculate the angle of the position of the target compared to whichever way they are looking
    def isInLineOfSight(self, target, angleLooking, thresholdAngleDegrees = 10):
        targetToPlayer_angle = self.getDirectionTo(target)
        angle_difference = abs(angleLooking - targetToPlayer_angle)
        # if the difference is small enough then return true
        return angle_difference <= math.radians(thresholdAngleDegrees) 