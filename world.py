# world generation
# world array
# holds state of the world at a time
import random

# represents individual spaces
class Space:
    def __init__(self):
        # determine the space characteristics
        self.pickup = False
        self.dropoff = False
        self.risk = False
        self.blocks = 0

# represents the world state
class World:
    # initialize
    def __init__(self):
        self.rows = 3
        self.cols = 3
        self.map = [[[Space() for j in range(self.cols)] for i in range(self.rows)] for i in range(3)]
        
        self.map[0][1][1].pickup = True
        self.map[0][1][1].blocks = 5

        self.map[0][2][2].dropoff = True
        self.map[0][1][2].risk = True

        self.map[1][0][2].pickup = True
        self.map[1][0][2].blocks = 5

        self.map[1][2][0].dropoff = True
        self.map[1][1][1].risk = True

        self.map[2][1][2].dropoff = True
        self.map[2][2][0].dropoff = True
    
    # when running experiment 4, this changes the pickup locations
    def experiment4Change(self):
        # get rid of old pickup locations
        self.map[0][1][1].pickup = False
        self.map[0][1][1].blocks = 0

        self.map[1][0][2].pickup = False
        self.map[1][0][2].blocks = 0

        # set new pickup locations
        self.map[1][2][2].pickup = True
        self.map[1][2][2].blocks = 5

        self.map[0][2][1].pickup = True
        self.map[0][2][1].blocks = 5

    # randomly generate world
    def generatePoints(self,seed):
        random.seed(seed)

    # checks if terminal state is reached 
    def checkTerminalState(self):
        for z in range(0,3):
            for y in range(0,3):
                for x in range(0,3):
                    if(self.map[z][y][x].pickup and self.map[z][y][x].blocks > 0):
                        return False
        return True
