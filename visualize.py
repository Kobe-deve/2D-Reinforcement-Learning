# GUI used for the program with handling display/input
import pygame

class Gui:
    def __init__(self):
        self.spaceSize = 80

        pygame.init()
        self.screen = pygame.display.set_mode((1200, 750))
        self.screen.fill((255, 255, 255))
        self.running = True
        self.presentModel = False

        self.mainFont = pygame.font.SysFont("Arial", 32)
        self.smallFont = pygame.font.SysFont("Arial", 15)

        self.mAgentImage = pygame.image.load("agent.png")
        self.fAgentImage = pygame.image.load("f_agent.png")

        # input variables
        self.seed = '0'
        self.maxDistance = 0
        self.minDistance = 0
        self.finishedRuns = 0
        self.learningRateText = '0.'
        self.discountRateText = '0.'
        self.stepsText = ''
        self.policy = 'PRANDOM'
        self.algorithm = 'Q-Learning'

        # input booleans
        self.inputSeed = False
        self.startRun = False
        self.inputLearning = False
        self.inputDiscount = False
        self.inputStep = False
        self.resetRun = False
        self.e4World = False

    # handling parameter inputs
    def inputHandling(self):
        for event in pygame.event.get():
          # check button input 
          if event.type == pygame.MOUSEBUTTONDOWN:
             if self.startRun == False and self.startButton.collidepoint(pygame.mouse.get_pos()):
                 self.startRun = True

             # toggle experiment 4 world
             if self.startRun == False and self.experimentButton.collidepoint(pygame.mouse.get_pos()):
                 self.e4World = not self.e4World

             if self.resetButton.collidepoint(pygame.mouse.get_pos()):
                self.resetRun = True

             if self.stepInput.collidepoint(pygame.mouse.get_pos()):
                self.inputStep = True
             else:
                self.inputStep = False
             
             # policy input
             if self.policyInput.collidepoint(pygame.mouse.get_pos()):
                if(self.policy == 'PRANDOM'):
                    self.policy = 'PEXPLOIT'
                elif(self.policy == 'PEXPLOIT'):
                    self.policy = 'PGREEDY'
                elif(self.policy == 'PGREEDY'):
                    self.policy = 'PRANDOM'

             # Learning algorithm
             if self.algorithmInput.collidepoint(pygame.mouse.get_pos()):
                if(self.algorithm == 'Q-Learning'):
                    self.algorithm = 'SARSA'
                elif(self.algorithm == 'SARSA'):
                    self.algorithm = 'Q-Learning'

             if self.startRun == False and self.modelPresentInput.collidepoint(pygame.mouse.get_pos()):
                self.presentModel = True

             if self.startRun == False and self.learningRateInput.collidepoint(pygame.mouse.get_pos()):
                self.inputLearning = True
             else:
                self.inputLearning = False
          
             if self.startRun == False and self.discountRateInput.collidepoint(pygame.mouse.get_pos()):
                self.inputDiscount = True
             else:
                self.inputDiscount = False

             if self.inputSeed == False and self.seedInput.collidepoint(pygame.mouse.get_pos()):
                self.inputSeed = True
             else:
                self.inputSeed = False

          # input seed
          if self.inputSeed and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and self.seed != '':
                self.seed = self.seed[:-1]
            elif event.unicode.isnumeric() and len(self.seed) < 7:
                if self.seed == '0':
                    self.seed = event.unicode
                else:
                    self.seed += event.unicode
                    
          # step input 
          if self.inputStep and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and self.stepsText != '':
                self.stepsText = self.stepsText[:-1]
            elif event.unicode.isnumeric() and len(self.stepsText) < 7:
                if self.stepsText == '0':
                    self.stepsText = event.unicode
                else:
                    self.stepsText += event.unicode
          
          # learning rate input
          if self.inputLearning and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and self.learningRateText[len(self.learningRateText)-1] != '.':
                self.learningRateText = self.learningRateText[:-1]
            elif event.unicode.isnumeric() and len(self.learningRateText) < 7:
                self.learningRateText += event.unicode
          
          # discount rate input
          if self.inputDiscount and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and self.discountRateText[len(self.discountRateText)-1] != '.':
                self.discountRateText = self.discountRateText[:-1]
            elif event.unicode.isnumeric() and len(self.discountRateText) < 7:
                self.discountRateText += event.unicode
      
          # exit window
          elif event.type == pygame.QUIT: 
                self.running = False
        if self.stepsText == '':
            self.stepsText = '0'

    # color action q-table
    def colorSpaceAction(self,value,values,currentQ):
        red = 0
        green = 0

        minQ = min(values[0][1],values[1][1],values[2][1],values[3][1],values[4][1],values[5][1]) 
        maxQ = max(values[0][1],values[1][1],values[2][1],values[3][1],values[4][1],values[5][1]) 

        negativeMin = minQ
        for i in values:
            if(i[1] < negativeMin and  i[1] < 0):
                negativeMin = i[1]

        scaleMaxq = maxQ
        scaleMinq = minQ

        if maxQ == 0:
            scaleMaxq = 1
        if minQ == 0:
            scaleMinq = 1
        if values[currentQ][1] > maxQ or values[currentQ][1] < minQ:
            return (0,0,255)

        if values[currentQ][1] == 0:
            return (100,100,100)
        elif values[currentQ][1] > 0:
            scale = values[currentQ][1] / scaleMaxq
            green = scale*200+55
        else:
            scale = (values[currentQ][1])/ (scaleMinq)
            red = scale*200+55

        return (red,green,0)

    # display agent coordination information
    def agentCoordination(self,agents):

        # display agent distances
        text = self.mainFont.render("Agent Coordination", True, (0, 0, 0)) 
        text_rect = text.get_rect(center=(600, 20))
        self.screen.blit(text, text_rect)
        
        # manhattan distance between agents
        distance = abs(agents[0].z-agents[1].z)+abs(agents[0].y-agents[1].y)+abs(agents[0].x-agents[1].x)

        if(distance > self.maxDistance):
            self.maxDistance = distance
        if(self.minDistance == 0 or distance < self.minDistance):
            self.minDistance = distance 

        text = self.mainFont.render("Manhattan Distance:"+str(distance), True, (0, 0, 0)) 
        text_rect = text.get_rect(center=(600, 70))
        self.screen.blit(text, text_rect)   
        text = self.mainFont.render("Min:"+str(self.maxDistance), True, (0, 0, 0)) 
        text_rect = text.get_rect(center=(600, 100))
        self.screen.blit(text, text_rect) 
        text = self.mainFont.render("Max:"+str(self.minDistance), True, (0, 0, 0)) 
        text_rect = text.get_rect(center=(600, 130))
        self.screen.blit(text, text_rect) 

        text = self.mainFont.render("Risk Steps", True, (0, 0, 0)) 
        text_rect = text.get_rect(center=(600, 430))
        self.screen.blit(text, text_rect) 

        # display number of times agents have stepped into risk zones 
        for i in agents:
            if(agents.index(i) == 0):
                name = "Female"
            else: 
                name = "Male"
            text = self.mainFont.render("Agent " + name + ": " + str(i.riskSteps), True, (0, 0, 0)) 
            text_rect = text.get_rect(center=(600, 460+agents.index(i)*30))
            self.screen.blit(text, text_rect) 

    # display a singular space and its q-table actions
    def displaySpace(self,x,y,z,spot):
        # display n/s/e/w q-table
        
        # up
        pygame.draw.rect(self.screen, self.colorSpaceAction(spot[0][1],spot,0), (x*self.spaceSize, z*(self.spaceSize*3+10)+y*self.spaceSize, self.spaceSize, self.spaceSize/5))
        pygame.draw.rect(self.screen, (0,0,0), (x*self.spaceSize, z*(self.spaceSize*3+10)+y*self.spaceSize, self.spaceSize, self.spaceSize/5),1)
        
        text = self.smallFont.render(str(round(spot[0][1],2)), True, (0, 0, 0)) 
        self.screen.blit(text, (x*self.spaceSize+self.spaceSize/2, z*(self.spaceSize*3+10)+y*self.spaceSize-2))
        
        # down 
        pygame.draw.rect(self.screen, self.colorSpaceAction(spot[1][1],spot,1), (x*self.spaceSize, z*(self.spaceSize*3+10)+y*self.spaceSize+self.spaceSize-self.spaceSize/5, self.spaceSize, self.spaceSize/5))
        pygame.draw.rect(self.screen, (0,0,0), (x*self.spaceSize, z*(self.spaceSize*3+10)+y*self.spaceSize+self.spaceSize-self.spaceSize/5, self.spaceSize, self.spaceSize/5),1)
        
        text = self.smallFont.render(str(round(spot[1][1],2)), True, (0, 0, 0)) 
        self.screen.blit(text, (x*self.spaceSize+self.spaceSize/2, z*(self.spaceSize*3+10)+y*self.spaceSize+(self.spaceSize*4)/5-2)) 

        # north 
        pygame.draw.polygon(self.screen, self.colorSpaceAction(spot[2][1],spot,2), [(x*self.spaceSize, z*(self.spaceSize*3+10)+y*self.spaceSize+self.spaceSize/5),(x*self.spaceSize+self.spaceSize/2, z*(self.spaceSize*3+10)+y*self.spaceSize+self.spaceSize/2),(x*self.spaceSize+self.spaceSize, z*(self.spaceSize*3+10)+y*self.spaceSize+self.spaceSize/5)])
        pygame.draw.polygon(self.screen, (0,0,0), [(x*self.spaceSize, z*(self.spaceSize*3+10)+y*self.spaceSize+self.spaceSize/5),(x*self.spaceSize+self.spaceSize/2, z*(self.spaceSize*3+10)+y*self.spaceSize+self.spaceSize/2),(x*self.spaceSize+self.spaceSize, z*(self.spaceSize*3+10)+y*self.spaceSize+self.spaceSize/5)],1)

        text = self.smallFont.render(str(round(spot[2][1],2)), True, (0, 0, 0)) 
        self.screen.blit(text, (x*self.spaceSize+self.spaceSize/3, z*(self.spaceSize*3+10)+y*self.spaceSize+self.spaceSize/5))

        # west
        pygame.draw.polygon(self.screen, self.colorSpaceAction(spot[5][1],spot,5), [(x*self.spaceSize, z*(self.spaceSize*3+10)+y*self.spaceSize+self.spaceSize/5),(x*self.spaceSize+self.spaceSize/2, z*(self.spaceSize*3+10)+y*self.spaceSize+self.spaceSize/2),(x*self.spaceSize, z*(self.spaceSize*3+10)+y*self.spaceSize+self.spaceSize-self.spaceSize/5)])
        pygame.draw.polygon(self.screen, (0,0,0), [(x*self.spaceSize, z*(self.spaceSize*3+10)+y*self.spaceSize+self.spaceSize/5),(x*self.spaceSize+self.spaceSize/2, z*(self.spaceSize*3+10)+y*self.spaceSize+self.spaceSize/2),(x*self.spaceSize, z*(self.spaceSize*3+10)+y*self.spaceSize+self.spaceSize-self.spaceSize/5)],1)
                    
        text = self.smallFont.render(str(round(spot[5][1],2)), True, (0, 0, 0)) 
        self.screen.blit(text, (x*self.spaceSize+self.spaceSize/25, z*(self.spaceSize*3+10)+y*self.spaceSize+self.spaceSize/3))
                    
        # east
        pygame.draw.polygon(self.screen, self.colorSpaceAction(spot[4][1],spot,4), [(x*self.spaceSize+self.spaceSize, z*(self.spaceSize*3+10)+y*self.spaceSize+self.spaceSize/5),(x*self.spaceSize+self.spaceSize/2, z*(self.spaceSize*3+10)+y*self.spaceSize+self.spaceSize/2),(x*self.spaceSize+self.spaceSize, z*(self.spaceSize*3+10)+y*self.spaceSize+self.spaceSize-self.spaceSize/5)])
        pygame.draw.polygon(self.screen, (0,0,0), [(x*self.spaceSize+self.spaceSize, z*(self.spaceSize*3+10)+y*self.spaceSize+self.spaceSize/5),(x*self.spaceSize+self.spaceSize/2, z*(self.spaceSize*3+10)+y*self.spaceSize+self.spaceSize/2),(x*self.spaceSize+self.spaceSize, z*(self.spaceSize*3+10)+y*self.spaceSize+self.spaceSize-self.spaceSize/5)],1)

        text = self.smallFont.render(str(round(spot[4][1],2)), True, (0, 0, 0)) 
        self.screen.blit(text, (x*self.spaceSize+(self.spaceSize*7)/10, z*(self.spaceSize*3+10)+y*self.spaceSize+self.spaceSize/3))

        # south
        pygame.draw.polygon(self.screen, self.colorSpaceAction(spot[3][1],spot,3), [(x*self.spaceSize, z*(self.spaceSize*3+10)+y*self.spaceSize+self.spaceSize-self.spaceSize/5),(x*self.spaceSize+self.spaceSize/2, z*(self.spaceSize*3+10)+y*self.spaceSize+self.spaceSize/2),(x*self.spaceSize+self.spaceSize, z*(self.spaceSize*3+10)+y*self.spaceSize+self.spaceSize-self.spaceSize/5)])
        pygame.draw.polygon(self.screen, (0,0,0), [(x*self.spaceSize, z*(self.spaceSize*3+10)+y*self.spaceSize+self.spaceSize-self.spaceSize/5),(x*self.spaceSize+self.spaceSize/2, z*(self.spaceSize*3+10)+y*self.spaceSize+self.spaceSize/2),(x*self.spaceSize+self.spaceSize, z*(self.spaceSize*3+10)+y*self.spaceSize+self.spaceSize-self.spaceSize/5)],1)
                    
        text = self.smallFont.render(str(round(spot[3][1],2)), True, (0, 0, 0)) 
        self.screen.blit(text, (x*self.spaceSize+self.spaceSize/3, z*(self.spaceSize*3+10)+y*self.spaceSize+(self.spaceSize*8)/10-self.spaceSize/5))

        displaySpace = pygame.draw.rect(self.screen, (0,0,0), (x*self.spaceSize, z*(self.spaceSize*3+10)+y*self.spaceSize, self.spaceSize, self.spaceSize), 1)           

    # main display function
    def display(self,world,q_table,agents):
        # clear screen
        self.screen.fill((255,255,255))

        if(self.startRun == False):
            self.modelPresentInput = pygame.draw.rect(self.screen, (255,0,0), pygame.Rect(1000, 420, 150, 60))
            self.startButton = pygame.draw.rect(self.screen, (255,0,0), pygame.Rect(1000, 500, 120, 60))
            self.experimentButton = pygame.draw.rect(self.screen, (255,0,0), pygame.Rect(700, 640, 250, 60))
            self.resetButton = pygame.draw.rect(self.screen, (255,0,0), pygame.Rect(1000, 640, 120, 60))
        
        self.learningRateInput = pygame.draw.rect(self.screen, (255,0,0), pygame.Rect(1000, 100, 120, 60))
        self.discountRateInput = pygame.draw.rect(self.screen, (255,0,0), pygame.Rect(1000, 180, 120, 60))
        self.stepInput = pygame.draw.rect(self.screen, (255,0,0), pygame.Rect(1000, 20, 120, 60))
        self.policyInput = pygame.draw.rect(self.screen, (255,0,0), pygame.Rect(1000, 260, 150, 60))
        self.algorithmInput = pygame.draw.rect(self.screen, (255,0,0), pygame.Rect(1000, 340, 150, 60))
        self.seedInput = pygame.draw.rect(self.screen, (255,0,0), pygame.Rect(600, 340, 150, 60))

        # display spaces and q-table
        for z in range(0,3):
            text = self.mainFont.render(str(z), True, (0, 0, 0)) 
            text_rect = text.get_rect(center=(self.spaceSize/4+self.spaceSize*3, self.spaceSize+z*(self.spaceSize*3+10)))
            self.screen.blit(text, text_rect)
            for y in range(0,3):
                for x in range(0,3):
                    self.displaySpace(z,y,x,q_table.map[z][y][x])
        
        # display space types
        for z in range(0,3):
            for y in range(0,3):
                for x in range(0,3):
                    # display outline based on if it's a pickup/dropoff/risk and show number of blocks it's holding 
                    if(world.map[z][y][x].pickup):
                        displaySpace = pygame.draw.rect(self.screen, (0,0,255), (x*self.spaceSize, z*(self.spaceSize*3+10)+y*self.spaceSize, self.spaceSize, self.spaceSize), 3)           
                        outlineBox = displaySpace = pygame.draw.rect(self.screen, (0,0,0), (x*self.spaceSize, z*(self.spaceSize*3+10)+y*self.spaceSize, self.spaceSize/4, self.spaceSize/4))             
                        text = self.smallFont.render(str(world.map[z][y][x].blocks), True, (255, 255, 255)) 
                        self.screen.blit(text, (outlineBox.x+5, outlineBox.y))
                    elif(world.map[z][y][x].dropoff):
                        displaySpace = pygame.draw.rect(self.screen, (0,255,0), (x*self.spaceSize, z*(self.spaceSize*3+10)+y*self.spaceSize, self.spaceSize, self.spaceSize), 3)           
                        outlineBox = pygame.draw.rect(self.screen, (0,0,0), (x*self.spaceSize, z*(self.spaceSize*3+10)+y*self.spaceSize, self.spaceSize/4, self.spaceSize/4))           
                        text = self.smallFont.render(str(world.map[z][y][x].blocks), True, (255, 255, 255)) 
                        self.screen.blit(text, (outlineBox.x+5, outlineBox.y))
                    elif(world.map[z][y][x].risk):
                        displaySpace = pygame.draw.rect(self.screen, (255,0,0), (x*self.spaceSize, z*(self.spaceSize*3+10)+y*self.spaceSize, self.spaceSize, self.spaceSize), 3)           
        # display agents
        for i in range(len(agents)):
            if(i == 0):
                imageUsed = self.fAgentImage
            else:
                imageUsed = self.mAgentImage
            self.screen.blit(imageUsed, (agents[i].x*self.spaceSize+self.spaceSize/2-16, agents[i].z*(self.spaceSize*3+10)+agents[i].y*self.spaceSize+self.spaceSize/2-16))
    
        # labels
        if(self.startRun == False):
            text = self.mainFont.render("Start", True, (0, 0, 0)) 
            text_rect = text.get_rect(center=(1060, 530))
            self.screen.blit(text, text_rect)

            if(self.e4World):
                e4Toggled = self.mainFont.render("Toggled", True, (0, 0, 0))
                self.screen.blit(e4Toggled, (self.experimentButton.x-100, self.experimentButton.y+5))

            resetText = self.mainFont.render("Experiment4 World", True, (0, 0, 0))
            self.screen.blit(resetText, (self.experimentButton.x+5, self.experimentButton.y+5))

            resetText = self.mainFont.render("Restart", True, (0, 0, 0))
            self.screen.blit(resetText, (self.resetButton.x+5, self.resetButton.y+5))
            
            text = self.mainFont.render("3D Model", True, (0, 0, 0)) 
            self.screen.blit(text, (self.modelPresentInput.x+5, self.modelPresentInput.y+5))

        text = self.mainFont.render("Steps", True, (0, 0, 0)) 
        self.screen.blit(text, (self.stepInput.x-200, self.stepInput.y+5))

        text = self.mainFont.render("Learning Rate", True, (0, 0, 0)) 
        self.screen.blit(text, (self.learningRateInput.x-200, self.learningRateInput.y+5))

        text = self.mainFont.render("Discount Rate", True, (0, 0, 0)) 
        self.screen.blit(text, (self.discountRateInput.x-200, self.discountRateInput.y+5))

        text = self.mainFont.render("Policy", True, (0, 0, 0)) 
        self.screen.blit(text, (self.policyInput.x-200, self.policyInput.y+5))
        
        text = self.mainFont.render("Algorithm", True, (0, 0, 0)) 
        self.screen.blit(text, (self.algorithmInput.x-200, self.algorithmInput.y+5))

        text = self.mainFont.render("Seed", True, (0, 0, 0)) 
        self.screen.blit(text, (self.seedInput.x-200, self.seedInput.y+5))

        # display input text 
        steptext = self.mainFont.render(self.stepsText, True, (0, 0, 0)) 
        self.screen.blit(steptext, (self.stepInput.x+5, self.stepInput.y+5))

        learningtext = self.mainFont.render(self.learningRateText, True, (0, 0, 0)) 
        self.screen.blit(learningtext, (self.learningRateInput.x+5, self.learningRateInput.y+5))
    
        discounttext = self.mainFont.render(self.discountRateText, True, (0, 0, 0)) 
        self.screen.blit(discounttext, (self.discountRateInput.x+5, self.discountRateInput.y+5))

        policytext = self.mainFont.render(self.policy, True, (0, 0, 0)) 
        self.screen.blit(policytext, (self.policyInput.x+5, self.policyInput.y+5))

        algorithmtext = self.mainFont.render(self.algorithm, True, (0, 0, 0)) 
        self.screen.blit(algorithmtext, (self.algorithmInput.x+5, self.algorithmInput.y+5))

        seedText = self.mainFont.render(self.seed, True, (0, 0, 0)) 
        self.screen.blit(seedText, (self.seedInput.x+5, self.seedInput.y+5))
        
        self.agentCoordination(agents)

        # display number of finished runs
        text = self.mainFont.render("Terminal states reached: " + str(self.finishedRuns), True, (0, 0, 0)) 
        text_rect = text.get_rect(center=(600, 620))
        self.screen.blit(text, text_rect)
        pygame.display.update()

    def exitOperations(self):
        pygame.quit()

    def mainLoop(self,world,q_table,agents):
        self.display(world,q_table,agents)
        self.inputHandling()
