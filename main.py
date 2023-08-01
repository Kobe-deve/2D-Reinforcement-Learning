import random
import copy
from visualize import Gui
from world import World
from agent import Agent 
from q_table import Q_table
from policy import Policy
from visualize3d import CubePlotter

# initialize agents
agents = []
agents.append(Agent())
agents.append(Agent())

agents[0] = Agent()
agents[0].setCoords(1,1,1)

agents[1] = Agent()
agents[1].setCoords(2,2,2)

# initialize gui
visualizer = Gui()

# initialize world 
worldUsed = World()

# initialize policy
usedPolicy = Policy('')

# initialize q-table
qTable = Q_table()

# initialize input rates
learningRate = 0
discountRate = 0
steps = 0
algorithmUsed = "Q-Learning"

totalRuns = 0

# boolean for if the algorithm is running 
runningAlgo = False

# main program loop
while visualizer.running:
    # display gui 
    visualizer.mainLoop(worldUsed,qTable,agents)
    visualizer.agentCoordination(agents)

    if(visualizer.resetRun and runningAlgo == False):
        worldUsed = World()
        visualizer.resetRun = False  
    
    # detects if the run should start because the button was pressed 
    if(visualizer.startRun and runningAlgo == False):
        # set the seed
        random.seed(int(visualizer.seed))

        # resetting world when clicking the button
        worldUsed = World()
        visualizer.resetRun = False
    
        # set displayed agent distances and finished runs back to zero
        visualizer.maxDistance = 0
        visualizer.minDistance = 0
        visualizer.finishedRuns = 0

        # reset risk steps in agents
        for i in agents:
            i.riskSteps = 0

        # get rates/policy/algorithm from input 
        steps = float(visualizer.stepsText)
        if(worldUsed.checkTerminalState() ==  False and steps != 0):
            usedPolicy = Policy(visualizer.policy)
            learningRate = float(visualizer.learningRateText)
            discountRate = float(visualizer.discountRateText)
            algorithmUsed = visualizer.algorithm
            runningAlgo = True
        else:
            visualizer.startRun = False


    # display 3D view
    if(visualizer.presentModel):
        cube_plotter = CubePlotter(center_coords=(0, 0, 0), edge_length=1, world=worldUsed)
        cube_plotter.show()
        visualizer.presentModel = False

    # running operations
    if(runningAlgo):
        # loop through agents 
        for i in agents:            
            # save agent before performing action
            oldAgent = copy.deepcopy(i)

            # agent selects action based on policy
            selectedMove = usedPolicy.decide(i,worldUsed,qTable,[0,1,2,3,4,5],agents)
            
            # if the action can be performed, perform it
            if(i.canPerformDirection(selectedMove,agents) == True):
                i.performAction(selectedMove,worldUsed)

            # print agent action and state movement
            if(selectedMove == -1):
                performedMove = "pickup"
            if(selectedMove == -2):
                performedMove = "dropof"
            if(selectedMove == 0):
                performedMove = "up"
            if(selectedMove == 1):
                performedMove = "down"
            if(selectedMove == 2):
                performedMove = "north"
            if(selectedMove == 3):
                performedMove = "south"
            if(selectedMove == 4):
                performedMove = "east"
            if(selectedMove == 5):
                performedMove = "west"
            
            print("Agent " + str(agents.index(i)) + " - ACTION: " + performedMove + " FROM: (" + str(oldAgent.z) + ", " + str(oldAgent.y) + ", " + str(oldAgent.x) + ") TO: (" + str(i.z) + ", " + str(i.y) + ", " + str(i.x) + ")")

            # update q-table
            # change update based on the learning type
            if(algorithmUsed == 'Q-Learning'):
                qTable.qLearningUpdate(worldUsed,oldAgent,i,selectedMove,agents,learningRate,discountRate)
            else: # SARSA
                next_selectedmove = usedPolicy.decide(i,worldUsed,qTable,[0,1,2,3,4,5],agents)
                qTable.sarsaUpdate(worldUsed,oldAgent,i,selectedMove,next_selectedmove,agents,learningRate,discountRate)
        
        print()

        # decreases step counter if running 
        steps = steps - 1

    # check if world is in terminal state and then reset
    if(worldUsed.checkTerminalState() == True):
        worldUsed = World()
        
        visualizer.resetRun = False
        visualizer.finishedRuns = visualizer.finishedRuns+1
        totalRuns = totalRuns + 1

        # setting experiment 4 world
        if(visualizer.e4World and totalRuns < 6 and totalRuns == 3):
            worldUsed.experiment4Change()


    # checks if steps are done 
    if(runningAlgo and ((runningAlgo and steps == 0))):
        print("Ended on step:" + str(steps))
        runningAlgo = False
        visualizer.startRun = False
        
# exit 
visualizer.exitOperations()