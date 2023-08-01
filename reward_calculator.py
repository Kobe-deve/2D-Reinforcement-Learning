# calculate reward based on the state and action an agent took

def calculate_reward(agent,world, action,agents):
        reward = 0
        current_space = world.map[agent.z][agent.y][agent.x]

        if (current_space.pickup and action == -1 and agent.heldBlock == 0) : #pickup
            reward += 20
        elif (current_space.dropoff and action == -2  and agent.heldBlock == 1): # dropoff
            reward += 20
        elif current_space.risk: # in risk zone
            reward -= 10
        elif(agent.canPerformDirection(action,agents)): # basic movement
            reward -= 1
        
        return reward