def main():
    i = Inventory()
    i.print()
    i.addItem('smg',30)
    i.print()
    i.addItem('pistol',30)
    i.print()
    i.addItem('crowbar')
    i.print()
    i.addItem('camera')

    i.addItem('smg',30)
    i.print()

    i.selectLeft()
    i.print()
    i.selectRight()
    i.print()

    i.shoot()
    i.print()
    
    i.selectRight()
    i.print()

    i.shoot()
    i.print()

    i.selectRight()
    i.print()

    i.shoot()
    i.print()

    i.selectRight()
    i.print()

    i.shoot()
    i.print()

    i.selectRight()
    i.print()

    i.shoot()
    i.print()

    i.removeItem()
    i.print()

    i.removeItem()
    i.print()

    i.removeItem()
    i.print()

    i.removeItem()
    i.print()

    i.removeItem()
    i.print()
    






class Inventory:
    def __init__(self):
        self.maxInventory = {'smg': 100, 'pistol': 69, 'siniper':100}        
        self.inventory = {}
        self.updated = []
        self.addItem('camera')

    def addItem(self, item, count = 1):
        print("adding item " + item)
        if item not in self.inventory:
            self.inventory[item] = count
            self.updated = [item] + self.updated
            return
        self.updated.remove(item)
        self.updated = [item] + self.updated
        self.inventory[item] += count
        if item in self.maxInventory:
            self.inventory[item] = min(self.inventory[item],self.maxInventory[item])

    def removeItem(self):
        if len(self.updated) <= 0: return
    
        item = self.updated[0]
        print("removing: " + item)
        
        isGun = item in self.maxInventory
        willRemoveAll = self.inventory[item] <= 1
        if isGun or willRemoveAll:
            self.inventory.pop(item)
            self.updated.remove(item)
            return
        self.inventory[item]-=1 

    def shoot(self):
        gun = self.updated[0]
        print("trying to shoot " + gun)
        if not gun in self.maxInventory:
            print("not a gun")
            return
        print("was a gun")
        if self.inventory[gun] > 0:        
            self.inventory[gun] -= 1

    def print(self):
        print(f"inventory: {self.inventory}")
        print(f"updated: {self.updated}\n")


    def selectLeft(self):
        self.updated = [self.updated[-1]] + self.updated[0:-1]
        print("selected left: ")
        
    def selectRight(self):
        self.updated = self.updated[1:] + self.updated[:1]
        print("selected Right: ")
    
if __name__ == "__main__":
    main()
        

    # add object
    # remove object
    # selectLeft
    # selectRight
    # print

    
