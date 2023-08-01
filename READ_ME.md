COSC 4368 - Group Capella
Reinforcement learning 

Kobe
Kian 
Fausto 

File layout:
    main.py - the main function which contains the initialization of the program and the main loop 
    agent.py - contains the agent class and agent operations
    policy.py - contains the policy class that decides actions for agents and the specific functions representing those strategies
    q_table.py - contains the q-table class and the learning algorithms used 
    reward_calculator.py - contains the reward function 
    visualize - contains the GUI class for displaying the operations and getting input 
    visualize3d - contains a class for running the 3D model visualization 
    world - contains the world class that contains the state 

    agent.png - images used to represent the agents 
    f_agent.png

This specific implemenation of the q-table involves one singular q-table being used by both the male and
female agents as they operate.

Run command:
    (need the pygame,matplotlib, and mpl_toolkits libraries installed beforehand)
    python main.py

GUI:
    Displays the q-table on the left side with all the actions being represented
    with 
    _____________
         up
    _____________
        north
    west    east
        south
    _____________
        down
    _____________

    The type of block has the following outline borders:
        Space types:
            Dropoff - Green 
            Pickup - Blue
            Risk - Red

    Click on parameters on the right hand side to input specific values

    Inputs:
        Steps: the number of steps to run 
        Learning Rate: the alpha (learning rate) value used when learning 
        Discount Rate: the gamma (discount rate) value used when learning
        Policy: What policy is being used
        Algorithm: What learning algorithm is being used
        3D Model: Displays a 3D model of the world 

        Starts: If applicable, begins running the steps (will not run with 0 steps)
        Restart: resets pickup/dropoff counts
        Experiment4 World: Sets up condition for the world to change based on the finished terminal states outside of runs (after 3 the world will change, after 6 it will revert to reset it back to 0 close and reopen the program)
        Seed: The seed used by the algorithm for random number generation 

    Values:
        Terminal states reached: In the individual run (when you click start), how many times a terminal state was reached
        Risk Steps: the number of times each agent steps on a risk zone in the run 
        Agent Coordination: The manhattan min and max difference during the run 

Actions:
    value
    -1  - pickup
    -2  - dropoff
     0  - up 
     1  - down
     2  - north
     3  - south
     4  - east
     5  - west

