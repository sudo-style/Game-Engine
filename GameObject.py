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
    
    def rot_center(self, image, angle):
        """rotate an image while keeping its center and size"""
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image, rot_rect