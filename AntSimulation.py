import time
import pygame
import random
"""
ToDo List:
-Make fire ant (Should grow in a circle in open areas, wood plant ant should die if it touches its path)
202 noraml ants ~= 500 fps
"""

#Custom
import Ant
import AntStepVar
import Colors
import CustomPath
import Interactive
import Text
#Globals
global BNFont
global screenH
global screenW
global MenuX
global MenuY
global MenuW
global MenuH
global gameDisplay
global toolType
global stepUp
global stepDown
global stepLeft
global stepRight
global allowedAntNum
global T_AntCount
global mouse


#TextPaths
BNFont = CustomPath.Path("assets\BebasNeue-Regular.ttf")

#Define Screen
screenH = 600
screenW = 800
MenuX = 0
MenuY = 0
MenuW = (screenW//4)
MenuH = screenH

#Set up pygame screen
pygame.init()
gameDisplay = pygame.display.set_mode((screenW,screenH))
clock = pygame.time.Clock()

#Custom Event Handling
Spawn = True
SpawnRate = 1
spawn_Event  = pygame.USEREVENT + 1
coolDown = 0

#Simulation Vars
isPaused = False
r = [] #Pixels to render list
allowedAntNum = 500
input_boxes = []
buttons = []
texts = []
toolType = "Ant"

#Simulation speed vars
startMultipler = 512     #Must be a number 2^
baseSpeed = 10000
userSpeed = 1
isPaused = False

#Ant step vars
stepUp = AntStepVar.AntStepVar(0,screenH)
stepDown = AntStepVar.AntStepVar(0,screenH)
stepRight = AntStepVar.AntStepVar(0,screenH)
stepLeft = AntStepVar.AntStepVar(0,screenH)
AntStepVars = [stepUp,stepDown,stepRight,stepLeft]

def clamp(n, smallest, largest): return max(smallest, min(n, largest))

#Classes:
class StepBoxes:
    """Creates a set of interactive text boxes that executes functions based on given args. NOT A DEPENDENT CLASS!"""
    def __init__(self, x, y, fontPath, fontSize, display, runFunction, clearFunction, randomFunction, updateVars):
        self.x = x
        self.y = y
        self.fontPath = fontPath
        self.fontSize = fontSize
        self.Gdisplay = display
        self.runFunction = runFunction
        self.clearFunction = clearFunction
        self.updateVars = updateVars
        self.xBox = self.x+6
        self.randomFunction = randomFunction

        #Colors
        labelColor = Colors.A_white
        titleColor = Colors.A_white
        boxColor = Colors.A_white
        boxTextColor = Colors.A_white
        menuBG = Colors.A_optionsBg

        #Text lables
        T_Title = Text.Text("Ant Steps",self.fontPath,fontSize,titleColor,self.x,self.y,self.Gdisplay,True,"bottomleft")
        T_UpStep = Text.Text("Up :",self.fontPath,fontSize,labelColor,self.x,self.y,self.Gdisplay,True,"topright")
        T_DownStep = Text.Text("Down :",self.fontPath,fontSize,labelColor,self.x,T_UpStep.GetY()+T_UpStep.GetHieght(),self.Gdisplay,True,"topright")
        T_RightStep =Text.Text("Right :",self.fontPath,fontSize,labelColor,self.x,T_DownStep.GetY()+T_DownStep.GetHieght(),self.Gdisplay,True,"topright")
        T_LeftStep = Text.Text("Left :",self.fontPath,fontSize,labelColor,self.x,T_RightStep.GetY()+T_RightStep.GetHieght(),self.Gdisplay,True,"topright")
        self.textObjects = [T_UpStep,T_DownStep,T_RightStep,T_LeftStep,T_Title]

        #Text objects for input boxes
        T_upStep = Text.Text("1",BNFont,20,boxTextColor,self.xBox, self.y,self.Gdisplay)
        T_downStep = Text.Text("1",BNFont,20,boxTextColor,self.xBox, T_UpStep.GetY()+T_UpStep.GetHieght(),self.Gdisplay)
        T_rightStep = Text.Text("1",BNFont,20,boxTextColor,self.xBox, T_DownStep.GetY()+T_DownStep.GetHieght(),self.Gdisplay)
        T_leftStep = Text.Text("1",BNFont,20,boxTextColor,self.xBox, T_RightStep.GetY()+T_RightStep.GetHieght(),self.Gdisplay)

        #Clickable input boxes
        IB_UpStep = Interactive.InputBox(self.xBox, self.y, 50, fontSize,boxColor,menuBG,self.Gdisplay,T_upStep,lambda x: self.runFunction(self.updateVars[0], x),1)
        IB_DownStep = Interactive.InputBox(self.xBox, T_UpStep.GetY()+T_UpStep.GetHieght(), 50, fontSize,boxColor,menuBG,self.Gdisplay,T_downStep,lambda x: self.runFunction(self.updateVars[1], x),1)
        IB_RightStep = Interactive.InputBox(self.xBox, T_DownStep.GetY()+T_DownStep.GetHieght(), 50, fontSize,boxColor,menuBG,self.Gdisplay,T_rightStep,lambda x: self.runFunction(self.updateVars[2], x),1)
        IB_LeftStep = Interactive.InputBox(self.xBox, T_RightStep.GetY()+T_RightStep.GetHieght(), 50, fontSize,boxColor,menuBG,self.Gdisplay,T_leftStep,lambda x: self.runFunction(self.updateVars[3], x),1)
        self.boxObjects = [IB_UpStep,IB_DownStep,IB_RightStep,IB_LeftStep]
        self.h = abs(IB_LeftStep.getBottomRight()[1]-IB_UpStep.getTopRight()[1])
        
        #Reset Button
        relX, relY = (IB_UpStep.getTopRight()[0]+2,IB_UpStep.getTopRight()[1])
        T_random = Text.Text("R",BNFont,20,Colors.A_black,relX,relY,self.Gdisplay)
        B_random = Interactive.Button(relX,relY,15,self.h, Colors.A_clearN, self.Gdisplay, T_random, lambda: self.randomFunction(self.updateVars,self.boxObjects))
        T_reset = Text.Text("C",BNFont,20,Colors.A_black,B_random.getTopRight()[0],relY,self.Gdisplay)
        B_reset = Interactive.Button(B_random.getTopRight()[0]+5,relY,15,self.h, Colors.A_clearN, self.Gdisplay, T_reset, lambda: self.clearFunction(self.updateVars,self.boxObjects))

        self.buttonObjects = [B_reset,B_random]
        self.w = abs(max(T_UpStep.GetX(),T_DownStep.GetX(),T_RightStep.GetX(),T_LeftStep.GetX(),T_Title.GetX())-(B_reset.x+B_reset.w))




#TextBoxes
T_Watermark = Text.Text("By: MrJohnWeez",BNFont,16,Colors.A_white,1,screenH+3,gameDisplay,True,"bottomleft",Colors.A_optionsBg)
T_AntCount = Text.Text("0/"+str(allowedAntNum),BNFont,20,Colors.A_white,1,screenH+3-16,gameDisplay,True,"bottomleft",Colors.A_optionsBg)
texts += [T_Watermark,T_AntCount]


#Button Functions
def togglePause():
    global isPaused
    isPaused = not isPaused
    bPause.ChangeMsg("Play") if isPaused else bPause.ChangeMsg("Pause")

def clearSim():
    """Clears the entire ant screen of any ants and their paths"""
    Ant.Ant.KillAllAnts()
    pygame.draw.rect(gameDisplay, Colors.A_white, pygame.Rect(MenuW,0,screenW,screenH))
    pygame.display.update(pygame.Rect(MenuW,0,screenW,screenH))
    T_AntCount.AddText(str(Ant.Ant.GetAntCount())+"/"+str(allowedAntNum),True)

def speedButton():
    global userSpeed
    global startMultipler

    if userSpeed < startMultipler: userSpeed = int(userSpeed*2)
    else: userSpeed = 1
    bSpeed.ChangeMsg("x"+str(startMultipler//userSpeed))



#Define Buttons
T_clear = Text.Text("Clear",BNFont,20,Colors.A_black,MenuX,MenuY,gameDisplay)
bClear = Interactive.Button(MenuX,MenuY,100,50, Colors.A_clearN, gameDisplay, T_clear, clearSim)
T_pause = Text.Text("Pause",BNFont,20,Colors.A_black,MenuX,MenuY+60,gameDisplay)
bPause = Interactive.ButtonToggle(MenuX,MenuY+60,100,50, Colors.A_clearN, gameDisplay, T_pause, togglePause)
T_Speed = Text.Text("x"+str(startMultipler//userSpeed),BNFont,20,Colors.A_black,MenuX,MenuY+120,gameDisplay)
bSpeed = Interactive.Button(MenuX,MenuY+120,100,50, Colors.A_clearN, gameDisplay, T_Speed, speedButton)
buttons += [bClear,bPause,bSpeed]





def PlaceTool():
    newStep = (stepUp.GetValue(),stepDown.GetValue(),stepLeft.GetValue(),stepRight.GetValue())
    def HelperAdd():
        tempAnt.Spawn()         
        T_AntCount.AddText(str(Ant.Ant.GetAntCount())+"/"+str(allowedAntNum),True)

    
    if toolType == "Ant":
        tempAnt = Ant.Ant((mouse[0]),(mouse[1]),pygame.Rect(MenuW,0,screenW,screenH),0,gameDisplay,newStep)
        HelperAdd()
    elif toolType == "WaterAnt":
        tempAnt = Ant.AntWater((mouse[0]),(mouse[1]),pygame.Rect(MenuW,0,screenW,screenH),0,gameDisplay,newStep)
        HelperAdd()
    elif toolType == "WoodAnt":
        tempAnt = Ant.AntWood((mouse[0]),(mouse[1]),pygame.Rect(MenuW,0,screenW,screenH),0,gameDisplay,newStep)
        HelperAdd()
    elif toolType == "FireAnt":
        tempAnt = Ant.AntFire((mouse[0]),(mouse[1]),pygame.Rect(MenuW,0,screenW,screenH),0,gameDisplay,newStep)
        HelperAdd()
    elif toolType == "PlantAnt":
        tempAnt = Ant.AntPlant((mouse[0]),(mouse[1]),pygame.Rect(MenuW,0,screenW,screenH),0,gameDisplay,newStep)
        HelperAdd()
    elif toolType == "Fill":
        cubeSize = 15
        x = mouse[0] - cubeSize
        y = mouse[1] - cubeSize
        x = clamp(x,MenuW,screenW)
        y = clamp(y,0,screenH)
        gameDisplay.fill(Colors.A_white, ((x,y), (cubeSize*2,cubeSize*2)))
        pygame.display.update((x,y), (cubeSize*2,cubeSize*2))
        
    
        
def ChangeToolType(newToolType):
    global toolType
    toolType = newToolType

T_Ant = Text.Text("Ant",BNFont,20,Colors.A_black,1,200,gameDisplay)
bAnt = Interactive.Button(1,200,60,20, Colors.A_clearN, gameDisplay, T_Ant, lambda: ChangeToolType("Ant"), True)
T_AntWater = Text.Text("Water",BNFont,20,Colors.A_black,1,bAnt.getBottomLeft()[1]+5,gameDisplay)
bAntWater = Interactive.Button(1,bAnt.getBottomLeft()[1]+5,60,20, Colors.A_clearN, gameDisplay, T_AntWater, lambda: ChangeToolType("WaterAnt"), True)
T_FillWhite= Text.Text("Clear Path",BNFont,20,Colors.A_black,1,bAntWater.getBottomLeft()[1]+5,gameDisplay)
bFillWhite = Interactive.Button(1,bAntWater.getBottomLeft()[1]+5,60,20, Colors.A_clearN, gameDisplay, T_FillWhite, lambda: ChangeToolType("Fill"), True)
T_AntWood = Text.Text("Wood",BNFont,20,Colors.A_black,1,bFillWhite.getBottomLeft()[1]+5,gameDisplay)
bAntWood = Interactive.Button(1,bFillWhite.getBottomLeft()[1]+5,60,20, Colors.A_clearN, gameDisplay, T_AntWood, lambda: ChangeToolType("WoodAnt"), True)
T_AntFire = Text.Text("Fire",BNFont,20,Colors.A_black,1,bAntWood.getBottomLeft()[1]+5,gameDisplay)
bAntFire = Interactive.Button(1,bAntWood.getBottomLeft()[1]+5,60,20, Colors.A_clearN, gameDisplay, T_AntFire, lambda: ChangeToolType("FireAnt"), True)
T_AntPlant = Text.Text("Plant",BNFont,20,Colors.A_black,1,bAntFire.getBottomLeft()[1]+5,gameDisplay)
bAntPlant = Interactive.Button(1,bAntFire.getBottomLeft()[1]+5,60,20, Colors.A_clearN, gameDisplay, T_AntPlant, lambda: ChangeToolType("PlantAnt"), True)
buttons += [bAnt,bAntWater,bFillWhite,bAntWood,bAntFire,bAntPlant]


def UpdateStepVar(var, textBox):
    var.UpdateByString(textBox.getText())
    textBox.updateText(str(var.GetValue()))

def ResetStepVars(varList, boxVars):
    for i in range(len(varList)):
        varList[i].Reset()
        boxVars[i].updateText(str(varList[i].GetValue()))

def RandomStepVars(varList, boxVars):
    for i in range(len(varList)):
        r = random.randint(0,screenH)
        varList[i].SetValue(r)
        boxVars[i].updateText(str(varList[i].GetValue()))
    
#Ant step boxes module
StepBox1 = StepBoxes(50,screenH+3-200,BNFont, 20, gameDisplay, UpdateStepVar, ResetStepVars, RandomStepVars, AntStepVars)
stepBoxes = [StepBox1]

#Simulation Functions
def QuitSim():
    """Quits game"""
    pygame.quit()
    quit()

def ResetSim():
    """Make the state of the simulation new."""
    pygame.draw.rect(gameDisplay, Colors.A_white, pygame.Rect(MenuW,0,screenW,screenH))
    pygame.draw.rect(gameDisplay, Colors.A_optionsBg, (0,0,MenuW,MenuH))

    #Reset buttons
    global buttons
    for button in buttons:
        button.DrawButton()
    for box in input_boxes:
        box.update()
    for text in texts:
        text.AddText(forceUpdate=True)
    for sbox in stepBoxes:
        for T in sbox.textObjects:
            T.AddText(forceUpdate=True)
        for B in sbox.boxObjects:
            B.update()
        for Bn in sbox.buttonObjects:
            Bn.DrawButton()
    Ant.Ant.KillAllAnts()
    pygame.display.update()
    

    


#Set up Simulation for setup
ResetSim()

#Main loop
while True:
    #Check for Button interaction
    mouse = pygame.mouse.get_pos()
    mouseOverMenu = MenuX+MenuW > mouse[0] > MenuX and MenuY+MenuH > mouse[1] > MenuY
    if mouseOverMenu:
        for button in buttons:
            button.Update()
        for sbox in stepBoxes:
            for Bn in sbox.buttonObjects:
                Bn.Update()

    for event in pygame.event.get():
        for box in input_boxes:
            box.handle_event(event)

        for sbox in stepBoxes:
            for B in sbox.boxObjects:
                B.handle_event(event)

        #Quit Game
        if event.type == pygame.QUIT: QuitSim()
            
        #Timer for spawn rate
        elif event.type == spawn_Event:
            Spawn = True
            pygame.time.set_timer(spawn_Event, 0)
        
        #Left Click Spwn an ant
        elif not mouseOverMenu and event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] == 1 and Ant.Ant.GetAntCount() < allowedAntNum:
            PlaceTool()

        #Hold down right click to spawn ants
        elif not mouseOverMenu and pygame.mouse.get_pressed()[2] == 1 and Spawn and Ant.Ant.GetAntCount() < allowedAntNum:
            #Reset Cooldown
            Spawn = False
            pygame.time.set_timer(spawn_Event, SpawnRate)
            # #Used for drawing a block on screen
            # gameDisplay.fill(Colors.A_black, ((mouse[0],mouse[1]), (50,50)))
            # pygame.display.update()

            PlaceTool()


        #Press 'C' to clear ants and screen
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c: clearSim()
            if event.key == pygame.K_p:
                togglePause()
                bPause.ForceUpdate(isPaused)
            if event.key == pygame.K_z:
                #print(Ant.Ant.GetAntCount())
                print(clock.get_fps())

    # Move every ant if not paused
    if not isPaused:
        Ant.Ant.UpdateAllAnts()
        pygame.display.update(Ant.Ant.GetRectUpdates())    #Update ants on screen only
        
    clock.tick(baseSpeed//userSpeed)    #Control the framerate of the simulation (Simulation speed)



















"""
Other:

#b_LUp = Button.Button("<", 1,screenH+3-16-75,15,25, Colors.clearN, gameDisplay, lambda : AntStep(stepUp, T_AntStepUp, False))
#b_RUp = Button.Button(">", 1+75,screenH+3-16-75,15,25, Colors.clearN, gameDisplay, lambda : AntStep(stepUp, T_AntStepUp, True))

# def AntStep(var, textVar, shouldIncrease, stepValue=1):
#     var.UpdateValue(shouldIncrease,stepValue)
#     textVar.ForceUpdate(str(var.GetValue()),Colors.optionsBg)

#T_AntStepUp = Text.Text("1",BNFont,20,Colors.white,1+25,screenH+3-16-50,gameDisplay,True,"bottomleft")

#input_box1 = InputBox.InputBox(1, 300, 50, 25,pygame.Color(255,255,255),pygame.Color(48,48,48),gameDisplay,BNFont,text="1",action=lambda x: UpdateStepVar(stepUp, x))

"""






"""
Other:

#b_LUp = Button.Button("<", 1,screenH+3-16-75,15,25, Colors.clearN, gameDisplay, lambda : AntStep(stepUp, T_AntStepUp, False))
#b_RUp = Button.Button(">", 1+75,screenH+3-16-75,15,25, Colors.clearN, gameDisplay, lambda : AntStep(stepUp, T_AntStepUp, True))

# def AntStep(var, textVar, shouldIncrease, stepValue=1):
#     var.UpdateValue(shouldIncrease,stepValue)
#     textVar.ForceUpdate(str(var.GetValue()),Colors.optionsBg)

#T_AntStepUp = Text.Text("1",BNFont,20,Colors.white,1+25,screenH+3-16-50,gameDisplay,True,"bottomleft")

#input_box1 = InputBox.InputBox(1, 300, 50, 25,pygame.Color(255,255,255),pygame.Color(48,48,48),gameDisplay,BNFont,text="1",action=lambda x: UpdateStepVar(stepUp, x))

"""