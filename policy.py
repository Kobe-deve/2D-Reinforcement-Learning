# defines the strategy that the agent uses to select actions based on the state
#policy functions.
import random
import numpy as np

def getargmax(values:list):
    max=-10000
    indexes=[]
    for i, value in enumerate(values):
        if value>max:
            max=value
    for i, value in enumerate(values):
        if(value==max):
            indexes+=[i]
    return indexes

# pexploit function
def pexploit(agent,qtable,actions):
    eps=round(random.random(), 2)
    
    # 85% of the time, go for the best action.
    if(eps<=0.85):
        values=[]
        for a in actions:
            values+=[qtable.map[agent.z][agent.y][agent.x][a][1]]
        bestactions=getargmax(values)
        if(len(bestactions)==1):
            return actions[bestactions[0]]
        else:#break ties by rolling a dice.
            return actions[random.choice(bestactions)]
    #take a random action 15% of the time
    else:
        return random.choice(actions)
    
# pgreedy policy 
def pgreedy(agent,qtable,actions,agents):
    values=[]

    # go through actions 
    for a in actions:
        values+=[[qtable.map[agent.z][agent.y][agent.x][a][1],a]]
  
    bestActions = []
    max = -99999999

    # loop through all values and select the best legal actions
    for v in values:
        if(agent.canPerformDirection(v[1],agents) and v[0] >= max):
            max = v[0]

            # check if other best actions are less than new max, if so remove them       
            for b in bestActions:
                if(b[0] < max):
                    bestActions.remove(b)
            bestActions+=[v] 
    
    # if there's only one good action    
    if(agent.canPerformDirection(bestActions[0][1],agents) and len(bestActions)==1): # select the best action
        return actions[bestActions[0][1]]
    else: #break ties by rolling a dice.
        choice = random.choice(bestActions)
        return actions[choice[1]]

class Policy:
    def __init__(self,type):
        if(type == 'PRANDOM'):
            self.policyType = 1
        elif(type == 'PEXPLOIT'):
            self.policyType = 2
        elif(type == 'PGREEDY'):
            self.policyType = 3
    
    def decide(self,agent,s,qtable,actions,agents):
        # check if pickup/dropoff is applicable 
        if(agent.heldBlock == 0 and s.map[agent.z][agent.y][agent.x].pickup == True and s.map[agent.z][agent.y][agent.x].blocks > 0):
            return -1 # pickup
        elif(agent.heldBlock > 0 and s.map[agent.z][agent.y][agent.x].dropoff and s.map[agent.z][agent.y][agent.x].blocks < 5):
            return -2 # dropoff
        # PRANDOM
        elif(self.policyType == 1):
            return random.choice(actions)
        # PEXPLOIT
        elif(self.policyType == 2):
            return pexploit(agent,qtable,actions)
        # PGREEDY
        elif(self.policyType == 3):
            return pgreedy(agent,qtable,actions,agents)
