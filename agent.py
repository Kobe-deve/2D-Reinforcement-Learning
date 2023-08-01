# object in the world 
# determine possible actions from the environment 
# select action

class Agent:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.heldBlock = 0
        self.riskSteps = 0

    def setCoords(self,x,y,z):
        self.z = z
        self.x = x
        self.y = y

    # check if an action can be performed based on position
    def canPerformDirection(self,action,listOfAgents=[]):
        newCoords = [self.z,self.y,self.x]

        # if action is pickup/dropoff return true as policy already checks if this action is applicable
        if(action < 0):
            return True

        # check for out of bounds 
        if(action == 0 and newCoords[0] < 2): # up
            newCoords[0] = newCoords[0]+1
        elif(action == 1 and newCoords[0] > 0): # down
            newCoords[0] = newCoords[0]-1
        elif(action == 2 and newCoords[1] > 0): # north
            newCoords[1] = newCoords[1]-1
        elif(action == 3 and newCoords[1] < 2): # south 
            newCoords[1] = newCoords[1]+1
        elif(action == 4 and newCoords[2] < 2): # east
            newCoords[2] = newCoords[2]+1
        elif(action == 5 and newCoords[2] > 0): # west
            newCoords[2] = newCoords[2]-1
        
        oldCoords = [self.z,self.y,self.x]
        
        # check if there aren't any other agents in the same position
        for i in listOfAgents:
            if((newCoords[0] == i.z and newCoords[1] == i.y and newCoords[2] == i.x)):
                return False
        # check boundaries 
        for j in range(len(newCoords)):
            if(newCoords[j] > 2 or newCoords[j] < 0):
                return False
            if(oldCoords[j] != newCoords[j]):
                return True
        return False

    # movement in world
    def performAction(self,action,world):
        if(action == -1): # pickup
            world.map[self.z][self.y][self.x].blocks = world.map[self.z][self.y][self.x].blocks - 1
            self.heldBlock = 1
        elif(action == -2): # dropoff
            world.map[self.z][self.y][self.x].blocks = world.map[self.z][self.y][self.x].blocks + 1
            self.heldBlock = 0
        elif(action == 0): # up
            self.z = self.z + 1
        elif(action == 1): # down
            self.z = self.z - 1
        elif(action == 2): # north
            self.y = self.y - 1
        elif(action == 3): # south 
            self.y = self.y + 1
        elif(action == 4): # east
            self.x = self.x + 1
        elif(action == 5): # west
            self.x = self.x - 1
        if(world.map[self.z][self.y][self.x].risk == True):
            self.riskSteps = self.riskSteps + 1