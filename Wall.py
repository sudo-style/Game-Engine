# I want the NPC to block their vision if the player is behind a wall

# assume these are perpendicular angles
class Wall:
    def __init__(self, shape, name):
        self.shape = shape
        self.points = []
        self.name = name
        self.findPoints()

    def findPoints(self):
        for i in range(0,len(self.shape),2):
            self.points.append((self.shape[i], self.shape[i+1]))
            
class Character:
    def __init__(self, pos, name):
        self.pos = pos
        self.name = name
        self.dir = 0

    def getDirectionTo(self, target):
        return math.atan2(target.pos[1] - self.pos[1], target.pos[0] - self.pos[0])    
    
    def getDistanceTo(self, target):
        return math.sqrt((target.pos[1] - self.pos[1])**2 + (target.pos[0] - self.pos[0])**2)

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.characters = []
        self.walls = []
        self.addCharacter((3,3), "p 1")
        self.addCharacter((width-1, height-1), "p 2")
        self.addWall((0,0,
                      2,2), 'w 1')
    
    def addCharacter(self, pos, name):
        self.characters.append(Character(pos, name))
    
    def addWall(self, shape, name):
        self.walls.append(Wall(shape, name))

    def print(self):
        charPos = {}
        wallPos = {}
        for character in self.characters: charPos[character.pos] = character.name

        for wall in self.walls:
            for point in wall.points:
                wallPos[point] = wall.name

        for y in range(self.height):
            for x in range(self.width):
                if (x,y) in charPos:
                    print(charPos[(x,y)], end = '')
                elif (x,y) in wallPos:
                    print(wallPos[(x,y)], end = '')
                else:
                    print('   ', end = '')
            print("|")

    def canTheySee(self, character1, character2):
        # check if the line between the two characters intersects with any wall
        for wall in self.walls:
            for i in range(0,len(wall.points), 2):
                if (self.lineIntersects(character1.pos, character2.pos, wall.points[i], wall.points[i+1])):
                    return False
        return True


def main():
    board = Board(8,8)
    board.print()

if __name__ == "__main__":
    main()
    