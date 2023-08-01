# holds q-table values and update functions
import random
from reward_calculator import *

class Q_table:
    def __init__(self):
       self.states=((x,y,z) for x in range(3) for y in range(3) for z in range(3))
       self.actions=((0, 'Up'), (1, 'Down'), (2, 'North'), (3, 'South'), (4, 'East'), (5, 'West'))
       self.map = [[[[[a,0.0] for a in range(6)] for j in range(3)] for i in range(3)] for i in range(3)] 
    
    # q-learning function
    def qLearningUpdate(self,world,oldAgent,newAgent,action,agents,alpha=0.5,gamma=0.5):
        
        # receive award
        reward = calculate_reward(oldAgent,world,action,agents)

        max_q_new_state = max(self.map[newAgent.z][newAgent.y][newAgent.x][a][1] for a in range(len(self.actions))) # select highest q value action from space 

        self.map[oldAgent.z][oldAgent.y][oldAgent.x][action][1] = self.map[oldAgent.z][oldAgent.y][oldAgent.x][action][1] + alpha * (reward + gamma * max_q_new_state - self.map[oldAgent.z][oldAgent.y][oldAgent.x][action][1])

    # sarsa function
    def sarsaUpdate(self,world,oldAgent,newAgent,action,next_action,agents,alpha=0.5,gamma=0.5):
        reward = calculate_reward(oldAgent,world,action,agents)

        # In SARSA, the Q value of the next state and next action is used instead of the max Q value
        q_next_state_next_action = self.map[newAgent.z][newAgent.y][newAgent.x][next_action][1]

        self.map[oldAgent.z][oldAgent.y][oldAgent.x][action][1] = self.map[oldAgent.z][oldAgent.y][oldAgent.x][action][1] + alpha * (reward + gamma * q_next_state_next_action - self.map[oldAgent.z][oldAgent.y][oldAgent.x][action][1])
