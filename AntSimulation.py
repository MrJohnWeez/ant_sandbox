#Built in
import random
import time
import pygame
import subprocess
import webbrowser
import sys

"""
ToDo List:
-Create Short Color buttons for: (1.5 hours)
    -LightGray
    -White
    -Darker blue
    -LightBrown
    -Lava like
    -Rich Green
    -lightPurple
    -Yellow
-Convert all ant buttons to image buttons and reposition them (2 hours)
-Slightly adjust AntSteps box (30 min)
-Add Sounds (When you place an ant,  hit clear, ect) (4 hours)
202 noraml ants ~= 500 fps
"""

#Custom
import Ant
import AntStepVar
import Colors
import CustomPath
import ImageManager
import Interactive
import Text

#Globals
global BNFont,screenH,screenW
global MenuX,MenuY,MenuW,MenuH
global gameDisplay

#TextPaths
BNFont = CustomPath.Path("assets\BebasNeue-Regular.ttf")
Rubik = CustomPath.Path("assets\Rubik-Regular.ttf")

AspectLong = 480/110
AspectShort = 242/107
AspectMini = 154/104

#Image Paths
temp1 = CustomPath.Path("assets\Buttons\BNLongBlue.png")
temp2 = CustomPath.Path("assets\Buttons\BLLongBlue.png")
temp3 = CustomPath.Path("assets\Buttons\BDLongBlue.png")
IBLongBlue = [temp2,temp1,temp3]

temp1 = CustomPath.Path("assets\Buttons\BNLongRed.png")
temp2 = CustomPath.Path("assets\Buttons\BLLongRed.png")
temp3 = CustomPath.Path("assets\Buttons\BDLongRed.png")
IBLongRed = [temp2,temp1,temp3]

temp1 = CustomPath.Path("assets\Buttons\BNShortRed.png")
temp2 = CustomPath.Path("assets\Buttons\BLShortRed.png")
temp3 = CustomPath.Path("assets\Buttons\BDShortRed.png")
IBShortRed = [temp2,temp1,temp3]

temp1 = CustomPath.Path("assets\Buttons\BNShortBlue.png")
temp2 = CustomPath.Path("assets\Buttons\BLShortBlue.png")
temp3 = CustomPath.Path("assets\Buttons\BDShortBlue.png")
IBShortBlue = [temp2,temp1,temp3]

temp1 = CustomPath.Path("assets\Buttons\BNShortLightGreen.png")
temp2 = CustomPath.Path("assets\Buttons\BLShortLightGreen.png")
temp3 = CustomPath.Path("assets\Buttons\BDShortLightGreen.png")
IBShortLightGreen = [temp2,temp1,temp3]

Test1 = CustomPath.Path("assets\Buttons\ButtonBackgroundShort1.png")
Test2 = CustomPath.Path("assets\Buttons\ButtonBackgroundShort2.png")

#Define Screen
screenH = 600
screenW = 800
MenuX,MenuY = 0,0
MenuW,MenuH = 200,screenH

#Set up pygame screen
pygame.init()
gameDisplay = pygame.display.set_mode((screenW,screenH))
clock = pygame.time.Clock()

def clamp(n, smallest, largest): return max(smallest, min(n, largest))

#Classes:
class StepBoxes:
    """Creates a set of interactive text boxes that executes functions based on given args. NOT A DEPENDENT CLASS!"""
    def __init__(self, x, y, fontPath, fontSize, display, runFunction, clearFunction, randomFunction, updateVars, speedFunction):
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
        self.speedFunction = speedFunction

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
        T_AntSpeed = Text.Text("Slower:",self.fontPath,17,labelColor,self.x,T_LeftStep.GetY()+T_LeftStep.GetHieght(),self.Gdisplay,True,"topright")
        self.textObjects = [T_UpStep,T_DownStep,T_RightStep,T_LeftStep,T_Title,T_AntSpeed]

        #Text objects for input boxes
        T_upStep = Text.Text("1",BNFont,20,boxTextColor,self.xBox, self.y,self.Gdisplay)
        T_downStep = Text.Text("1",BNFont,20,boxTextColor,self.xBox, T_UpStep.GetY()+T_UpStep.GetHieght(),self.Gdisplay)
        T_rightStep = Text.Text("1",BNFont,20,boxTextColor,self.xBox, T_DownStep.GetY()+T_DownStep.GetHieght(),self.Gdisplay)
        T_leftStep = Text.Text("1",BNFont,20,boxTextColor,self.xBox, T_RightStep.GetY()+T_RightStep.GetHieght(),self.Gdisplay)
        T_antSpeed = Text.Text(str(Ant.Ant.maxSpeed-1000),BNFont,20,boxTextColor,self.xBox, T_leftStep.GetY()+T_leftStep.GetHieght(),self.Gdisplay)
        #Clickable input boxes
        IB_UpStep = Interactive.InputBox(self.xBox, self.y, 50, fontSize,boxColor,menuBG,self.Gdisplay,T_upStep,lambda x: self.runFunction(self.updateVars[0], x),1)
        IB_DownStep = Interactive.InputBox(self.xBox, T_UpStep.GetY()+T_UpStep.GetHieght(), 50, fontSize,boxColor,menuBG,self.Gdisplay,T_downStep,lambda x: self.runFunction(self.updateVars[1], x),1)
        IB_RightStep = Interactive.InputBox(self.xBox, T_DownStep.GetY()+T_DownStep.GetHieght(), 50, fontSize,boxColor,menuBG,self.Gdisplay,T_rightStep,lambda x: self.runFunction(self.updateVars[2], x),1)
        IB_LeftStep = Interactive.InputBox(self.xBox, T_RightStep.GetY()+T_RightStep.GetHieght(), 50, fontSize,boxColor,menuBG,self.Gdisplay,T_leftStep,lambda x: self.runFunction(self.updateVars[3], x),1)
        IB_AntSpeed = Interactive.InputBox(self.xBox, T_leftStep.GetY()+T_leftStep.GetHieght(), 50, fontSize,boxColor,menuBG,self.Gdisplay,T_antSpeed,lambda x: speedFunction(x),1)
        self.boxObjects = [IB_UpStep,IB_DownStep,IB_RightStep,IB_LeftStep,IB_AntSpeed]
        self.h = abs(IB_AntSpeed.getBottomRight()[1]-IB_UpStep.getTopRight()[1])
        
        #Reset Button
        relX, relY = (IB_UpStep.getTopRight()[0]+2,IB_UpStep.getTopRight()[1])
        T_random = Text.Text("R",BNFont,20,Colors.A_black,relX,relY,self.Gdisplay)
        B_random = Interactive.Button(relX,relY,15,self.h, Colors.A_clearN, self.Gdisplay, T_random, lambda: self.randomFunction(self.updateVars,self.boxObjects))
        T_resetAntStep = Text.Text("C",BNFont,20,Colors.A_black,B_random.getTopRight()[0],relY,self.Gdisplay)
        B_resetAntStep = Interactive.Button(B_random.getTopRight()[0]+5,relY,15,self.h, Colors.A_clearN, self.Gdisplay, T_resetAntStep, lambda: self.clearFunction(self.updateVars,self.boxObjects))

        self.buttonObjects = [B_resetAntStep,B_random]
        self.w = abs(max(T_UpStep.GetX(),T_DownStep.GetX(),T_RightStep.GetX(),T_LeftStep.GetX(),T_Title.GetX())-(B_resetAntStep.x+B_resetAntStep.w))


    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getW(self):
        return self.w
    def getH(self):
        return self.h
    def getTopLeft(self):
        return (self.getX(), self.getY())
    def getTopRight(self):
        return (self.getX()+self.getW(), self.getY())
    def getBottomLeft(self):
        return (self.getX(), self.getY()+self.getH())
    def getBottomRight(self):
        return (self.getX()+self.getW(), self.getY()+self.getH())


def LoadMJWLink():
    url = 'https://mrjohnweez.weebly.com'
    if sys.platform == 'darwin':    # in case of OS X
        subprocess.Popen(['open', url])
    else:
        webbrowser.open_new_tab(url)
    
#Simulation Functions
def QuitSim():
    """Quits game"""
    pygame.quit()
    quit()
    
class ToggleVar:
    """A basic toggle varible class"""
    def __init__(self, state=False):
        self.state = state

    def ToggleState(self):
        """Toggles the state of the bool value"""
        self.state = not self.state
        
class SimSpeed:
    """Contains the global varible for the simulation speed"""
    def __init__(self, startValue, minValue, maxValue):
        self.value = startValue
        self.minValue = minValue
        self.maxValue = maxValue

    def Increase(self):
        """Increase the scalar by two"""
        if self.value >= self.maxValue: self.value = self.minValue
        else: self.value = self.value*2

class AntSpeed:
    """Contains the global varible for ant speed"""
    def __init__(self, startValue, minValue, maxValue):
        self.value = startValue
        self.default = startValue
        self.minValue = minValue
        self.maxValue = maxValue

    def UpdateAntSpeed(self, textBox):
        """Updates the value of the ant speed if given a string or int value.
        Also updates its textbox on screen"""
        self.value = textBox.getText()
        if self.value.isdigit():
            self.value = int(self.value)
        elif len(self.value) > 0 and self.value[0] == "-":
            self.value = self.minValue
        else:
            self.value = self.default
        
        if self.value > self.maxValue:
            self.value = self.maxValue
        elif self.value < self.minValue:
            self.value = self.minValue

        textBox.updateText(str(self.value))


class ToolType:
    """Class for all the different interactive tools within this ant simulation game"""
    def __init__(self, activeTool, antSteps, antSpeed,T_AntCount,isPaused):
        self.activeTool = activeTool
        self.antSteps = antSteps
        self.antSpeed = antSpeed
        self.T_AntCount = T_AntCount
        self.isPaused = isPaused

    def UseTool(self):
        """Active the tool the user has selected"""
        mouse = pygame.mouse.get_pos()
        newStep = self.antSteps.GetGroupValues()
        def HelperAdd():
            """Spawns the ant type then updates the count text"""
            tempAnt.Spawn()         
            self.T_AntCount.AddText(str(Ant.Ant.GetAntCount())+"/"+str(Ant.Ant.antLimit),True)
        
        if self.activeTool == "Ant":
            tempAnt = Ant.Ant((mouse[0]),(mouse[1]),pygame.Rect(MenuW,0,screenW,screenH),0,gameDisplay,newStep, self.antSpeed.value)
            HelperAdd()
        elif self.activeTool == "WaterAnt":
            tempAnt = Ant.AntWater((mouse[0]),(mouse[1]),pygame.Rect(MenuW,0,screenW,screenH),0,gameDisplay,newStep, self.antSpeed.value)
            HelperAdd()
        elif self.activeTool == "WoodAnt":
            tempAnt = Ant.AntWood((mouse[0]),(mouse[1]),pygame.Rect(MenuW,0,screenW,screenH),0,gameDisplay,newStep, self.antSpeed.value)
            HelperAdd()
        elif self.activeTool == "FireAnt":
            newList = []
            for i in newStep:
                i += 14
                if i > screenH:
                    i = (i - screenH)
                elif i < 0:
                    i = screenH + i
                newList += [i]
            tempAnt = Ant.AntFire((mouse[0]),(mouse[1]),pygame.Rect(MenuW,0,screenW,screenH),0,gameDisplay,newList, self.antSpeed.value)
            HelperAdd()
        elif self.activeTool == "PlantAnt":
            tempAnt = Ant.AntPlant((mouse[0]),(mouse[1]),pygame.Rect(MenuW,0,screenW,screenH),0,gameDisplay,newStep, self.antSpeed.value)
            HelperAdd()
        elif self.activeTool == "ZombieAnt":
            tempAnt = Ant.AntZombie((mouse[0]),(mouse[1]),pygame.Rect(MenuW,0,screenW,screenH),0,gameDisplay,newStep, self.antSpeed.value)
            HelperAdd()
        elif self.activeTool == "CrazyAnt":
            tempAnt = Ant.AntCrazy((mouse[0]),(mouse[1]),pygame.Rect(MenuW,0,screenW,screenH),0,gameDisplay,newStep, self.antSpeed.value)
            HelperAdd()
        elif self.activeTool == "Fill":
            cubeSize = 15
            x = mouse[0] - cubeSize
            y = mouse[1] - cubeSize
            x = clamp(x,MenuW,screenW)
            y = clamp(y,0,screenH)
            gameDisplay.fill(Colors.A_white, ((x,y), (cubeSize*2,cubeSize*2)))
            pygame.display.update((x,y), (cubeSize*2,cubeSize*2))
            Ant.Ant.KillAntsInRect(pygame.Rect(x,y,cubeSize*2,cubeSize*2))
            if self.isPaused.state:
                Ant.Ant.UpdateAllAnts()
                #Update ant count if ants die
                if self.T_AntCount.GetText() != str(Ant.Ant.GetAntCount())+"/"+str(Ant.Ant.antLimit):
                    self.T_AntCount.AddText(str(Ant.Ant.GetAntCount())+"/"+str(Ant.Ant.antLimit),True)

    def ChangeTool(self, newTool):
        """Sets the active tool to the new given string"""
        self.activeTool = newTool

    def GetTool(self):
        """Returns the active tool"""
        return self.activeTool
    



def AntSimulation():
    """Main ant simulation loop"""
    simulationSpeed = SimSpeed(1,1,4096)
    TicksLeft = simulationSpeed.value

    #Custom Event Handling
    Spawn = True
    SpawnRate = 1
    spawn_Event  = pygame.USEREVENT + 1
    coolDown = 0

    #Simulation Vars
    r = [] #Pixels to render list
    Ant.Ant.SetAntLimit(500)
    Ant.Ant.maxSpeed = 6000
    input_boxes = []
    buttons = []
    texts = []
    antSteps = AntStepVar.AntStepGroup(1,screenH)
    antSpeed = AntSpeed(Ant.Ant.maxSpeed-1000,1,Ant.Ant.maxSpeed)
    isPaused = ToggleVar()


    #Button Functions
    def togglePause():
        """Changes the pause state of the game. Also updates the toggle button"""
        isPaused.ToggleState()
        bPause.ChangeMsg("Play") if isPaused.state else bPause.ChangeMsg("Pause")

    def ClearSim():
        """Clears the entire ant screen of any ants and their paths"""
        Ant.Ant.KillAllAnts()
        pygame.draw.rect(gameDisplay, Colors.A_white, pygame.Rect(MenuW,0,screenW,screenH))
        pygame.display.update(pygame.Rect(MenuW,0,screenW,screenH))
        T_AntCount.AddText(str(Ant.Ant.GetAntCount())+"/"+str(Ant.Ant.antLimit),True)
    def ClearPaths():
        """Clears the entire ant screen of any ant paths"""
        pygame.draw.rect(gameDisplay, Colors.A_white, pygame.Rect(MenuW,0,screenW,screenH))
        pygame.display.update(pygame.Rect(MenuW,0,screenW,screenH))

    def speedButton():
        """Decreases the simulation speed by a factor of double the prevous value"""
        simulationSpeed.Increase()
        bSpeed.ChangeMsg("x"+str(simulationSpeed.value))


    T_Copyright = Text.Text("MrJohnWeez©2018",Rubik,12,Colors.A_white,0,screenH,gameDisplay,pos="bottomleft",backgroundColor=Colors.A_black)
    T_AntCount = Text.Text("0/"+str(Ant.Ant.antLimit),BNFont,20,Colors.A_white,MenuW,screenH,gameDisplay,True,"bottomright",Colors.A_black)
    texts += [T_Copyright,T_AntCount]


    #Define Buttons
    T_mainmenu = Text.Text("Back",Rubik,21,Colors.A_white,T_Copyright.getTopLeft()[0],T_Copyright.getTopLeft()[1],gameDisplay)
    tempHeight = T_mainmenu.GetHieght()+4
    B_mainmenu = Interactive.ButtonImage(T_mainmenu.GetX(),T_mainmenu.GetY(),int(tempHeight*AspectShort),tempHeight,IBShortBlue[1],IBShortBlue[0],IBShortBlue[2],gameDisplay,T_mainmenu,MainMenu,pos="bottomleft")
    
    T_reset = Text.Text("Reset",Rubik,20,Colors.A_white,MenuW,MenuY,gameDisplay)
    tempHeight = T_reset.GetHieght()+4
    B_reset = Interactive.ButtonImage(T_reset.GetX(),T_reset.GetY(),int(tempHeight*AspectShort),tempHeight,IBShortRed[1],IBShortRed[0],IBShortRed[2],gameDisplay,T_reset,ClearSim,pos="topright")
    
    T_kill = Text.Text("Kill",Rubik,20,Colors.A_white,B_reset.getBottomRight()[0],B_reset.getBottomRight()[1],gameDisplay)
    tempHeight = T_kill.GetHieght()+4
    B_kill = Interactive.ButtonImage(T_kill.GetX(),T_kill.GetY(),int(tempHeight*AspectShort),tempHeight,IBShortRed[1],IBShortRed[0],IBShortRed[2],gameDisplay,T_kill,Ant.Ant.KillAllAnts,pos="topright")
    
    T_clearPath = Text.Text("Clear",Rubik,20,Colors.A_white,B_kill.getBottomRight()[0],B_kill.getBottomRight()[1],gameDisplay)
    tempHeight = T_clearPath.GetHieght()+4
    B_clearPath = Interactive.ButtonImage(T_clearPath.GetX(),T_clearPath.GetY(),int(tempHeight*AspectShort),tempHeight,IBShortRed[1],IBShortRed[0],IBShortRed[2],gameDisplay,T_clearPath,ClearPaths,pos="topright")
    
    buttons += [B_mainmenu,B_reset,B_kill,B_clearPath]
    
    
    T_pause = Text.Text("Pause",Rubik,20,Colors.A_white,MenuX,MenuY,gameDisplay)
    tempHeight = T_pause.GetHieght()+7
    bPause = Interactive.ButtonImage(T_pause.GetX(),T_pause.GetY(),int(tempHeight*AspectShort),tempHeight,IBShortLightGreen[1],IBShortLightGreen[0],IBShortLightGreen[2],gameDisplay,T_pause,togglePause,pos="topleft")

    T_speedLabel1 = Text.Text("Times",Rubik,18,Colors.A_white,bPause.getBottomRight()[0]-15,bPause.getBottomRight()[1]+5,gameDisplay,pos="topcenter")
    T_speedLabel2 = Text.Text("Slower:",Rubik,18,Colors.A_white,T_speedLabel1.getBottomCenter()[0],T_speedLabel1.getBottomCenter()[1],gameDisplay,pos="topcenter")

    T_Speed = Text.Text("x"+str(simulationSpeed.value),Rubik,19,Colors.A_white,T_speedLabel2.getBottomCenter()[0]+7,T_speedLabel2.getBottomCenter()[1],gameDisplay,pos="topcenter")
    tempHeight = T_Speed.GetHieght()+8
    bSpeed = Interactive.ButtonImage(T_Speed.GetX(),T_Speed.GetY(),int(tempHeight*AspectShort),tempHeight,Test1,Test1,Test1,gameDisplay,T_Speed,speedButton,pos="topcenter")

    texts += [T_speedLabel1,T_speedLabel2]
    buttons += [bPause,bSpeed]

    tool = ToolType("Ant",antSteps,antSpeed,T_AntCount,isPaused)

    def UpdateStepVar(var, textBox):
        """Updates the varible and the text box for one of the four input boxes"""
        var.UpdateByString(textBox.getText())
        textBox.updateText(str(var.GetValue()))

    def ResetStepVars(varList, boxVars, overrideValue=None):
        """Makes all 4 step boxes 1"""
        for i in range(len(varList)):
            if overrideValue != None:
                varList[i].SetValue(overrideValue[i])
            else:
                varList[i].Reset()
            boxVars[i].updateText(str(varList[i].GetValue()))

    def RandomStepVars(varList, boxVars):
        """Varibles that contain the step values from the input boxes"""
        for i in range(len(varList)):
            r = random.randint(varList[i].GetMin(),varList[i].GetMax())
            varList[i].SetValue(r)
            boxVars[i].updateText(str(varList[i].GetValue()))
        
    #Ant step boxes module
    StepBox1 = StepBoxes(50,screenH+3-200,BNFont, 20, gameDisplay, UpdateStepVar, ResetStepVars, RandomStepVars, antSteps.GetGroup(), antSpeed.UpdateAntSpeed)
    stepBoxes = [StepBox1]


    #Right Side
    T_Ant = Text.Text("Ant",BNFont,20,Colors.A_black,1,200,gameDisplay)
    bAnt = Interactive.Button(1,200,60,20, Colors.A_clearN, gameDisplay, T_Ant, lambda: tool.ChangeTool("Ant"), True)
    T_AntWater = Text.Text("Water",BNFont,20,Colors.A_black,1,bAnt.getBottomLeft()[1]+5,gameDisplay)
    bAntWater = Interactive.Button(1,bAnt.getBottomLeft()[1]+5,60,20, Colors.A_clearN, gameDisplay, T_AntWater, lambda: tool.ChangeTool("WaterAnt"), True)
    T_FillWhite= Text.Text("Delete Ant",BNFont,20,Colors.A_black,1,bAntWater.getBottomLeft()[1]+5,gameDisplay)
    bFillWhite = Interactive.Button(1,bAntWater.getBottomLeft()[1]+5,60,20, Colors.A_clearN, gameDisplay, T_FillWhite, lambda: tool.ChangeTool("Fill"), True)
    T_AntWood = Text.Text("Wood",BNFont,20,Colors.A_black,1,bFillWhite.getBottomLeft()[1]+5,gameDisplay)
    bAntWood = Interactive.Button(1,bFillWhite.getBottomLeft()[1]+5,60,20, Colors.A_clearN, gameDisplay, T_AntWood, lambda: tool.ChangeTool("WoodAnt"), True)
    T_AntFire = Text.Text("Fire",BNFont,20,Colors.A_black,1,bAntWood.getBottomLeft()[1]+5,gameDisplay)
    bAntFire = Interactive.Button(1,bAntWood.getBottomLeft()[1]+5,60,20, Colors.A_clearN, gameDisplay, T_AntFire, lambda: tool.ChangeTool("FireAnt"), True)
    T_AntPlant = Text.Text("Plant",BNFont,20,Colors.A_black,1,bAntFire.getBottomLeft()[1]+5,gameDisplay)
    bAntPlant = Interactive.Button(1,bAntFire.getBottomLeft()[1]+5,60,20, Colors.A_clearN, gameDisplay, T_AntPlant, lambda: tool.ChangeTool("PlantAnt"), True)

    #Left Side
    T_AntZombie = Text.Text("Zombie",BNFont,20,Colors.A_black,1,bAnt.getBottomLeft()[1]+5,gameDisplay)
    bAntZombie = Interactive.Button(bAnt.getTopRight()[0]+5,bAnt.getTopRight()[1],60,20, Colors.A_clearN, gameDisplay, T_AntZombie, lambda: tool.ChangeTool("ZombieAnt"), True)
    T_AntCrazy = Text.Text("Crazy",BNFont,20,Colors.A_black,1,bAntZombie.getBottomLeft()[1]+5,gameDisplay)
    bAntCrazy = Interactive.Button(bAnt.getTopRight()[0]+5,bAntZombie.getBottomLeft()[1]+5,60,20, Colors.A_clearN, gameDisplay, T_AntCrazy, lambda: tool.ChangeTool("CrazyAnt"), True)

    buttons += [bAnt,bAntWater,bFillWhite,bAntWood,bAntFire,bAntPlant,bAntZombie,bAntCrazy]

    def ResetSim():
        """Make the state of the simulation new."""
        pygame.draw.rect(gameDisplay, Colors.A_white, pygame.Rect(MenuW,0,screenW,screenH))
        pygame.draw.rect(gameDisplay, Colors.A_black, (0,0,MenuW,MenuH))

        bSpeed.UpdateBackground()
        #Reset buttons
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
            elif not mouseOverMenu and event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] == 1:
                tool.UseTool()

            #Hold down right click to spawn ants
            elif not mouseOverMenu and pygame.mouse.get_pressed()[2] == 1 and Spawn:
                #Reset Cooldown
                Spawn = False
                pygame.time.set_timer(spawn_Event, SpawnRate)
                tool.UseTool()

            #Press 'C' to clear ants and screen
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c: ClearSim()
                if event.key == pygame.K_p:
                    bPause.action()
                if event.key == pygame.K_z:
                    #print(Ant.Ant.GetAntCount())
                    print(clock.get_fps())
                    

        # Move every ant, if correct simulation timing and if not paused 
        TicksLeft -= 1
        if TicksLeft <= 0:
            TicksLeft = simulationSpeed.value
            if not isPaused.state:
                Ant.Ant.UpdateAllAnts()

                #Update ant count if ants die
                if T_AntCount.GetText() != str(Ant.Ant.GetAntCount())+"/"+str(Ant.Ant.antLimit):
                    T_AntCount.AddText(str(Ant.Ant.GetAntCount())+"/"+str(Ant.Ant.antLimit),True)
                    
                pygame.display.update(Ant.Ant.GetRectUpdates())    #Update ants on screen only



def MainMenu():
    """Main menu"""
    mainMenuTitle = ImageManager.ImageType(CustomPath.Path("assets\AntSimTitle.png"),gameDisplay)
    go = True
    buttons = []

    gameDisplay.fill(Colors.A_black)
    pygame.display.update()
    mainMenuTitle.AutoScale(screenW,screenH,0.1,0.1)
    mainMenuTitle.Draw((screenW//2,screenH//4))
    
    spacing = 25
    T_Play = Text.Text("Play",Rubik,30,Colors.A_white,screenW//2,int(screenH*.5),gameDisplay)
    B_Play = Interactive.ButtonImage(T_Play.GetX(),T_Play.GetY(),int(50*4.3),50,IBLongBlue[1],IBLongBlue[0],IBLongBlue[2],gameDisplay,T_Play,AntSimulation,pos="center")

    T_About = Text.Text("About",Rubik,30,Colors.A_white,B_Play.getCenter()[0],B_Play.getBottomLeft()[1]+spacing,gameDisplay)
    B_About = Interactive.ButtonImage(T_About.GetX(),T_About.GetY(),int(50*4.3),50,IBLongBlue[1],IBLongBlue[0],IBLongBlue[2],gameDisplay,T_About,AboutMenu,pos="center")

    T_Quit = Text.Text("Quit",Rubik,30,Colors.A_white,B_About.getCenter()[0],B_About.getBottomLeft()[1]+spacing,gameDisplay)
    B_Quit = Interactive.ButtonImage(T_Quit.GetX(),T_Quit.GetY(),int(50*4.3),50,IBLongBlue[1],IBLongBlue[0],IBLongBlue[2],gameDisplay,T_Quit,QuitSim,pos="center")

    T_Copyright = Text.Text("MrJohnWeez©2018",Rubik,12,Colors.A_white,0,screenH,gameDisplay,pos="bottomleft")

    buttons += [B_Play,B_Quit,B_About]
    TextList = [T_Copyright]
    for i in TextList: i.AddText(forceUpdate=True)

    

    while go:
        #Check for Button interaction
        for button in buttons: button.Update()

        for event in pygame.event.get():
            #Quit Game
            if event.type == pygame.QUIT: QuitSim()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    QuitSim()


def AboutMenu():
    """About menu"""
    aboutMenuTitle = ImageManager.ImageType(CustomPath.Path("assets\AboutTitle.png"),gameDisplay)
    go = True
    buttons = []

    gameDisplay.fill(Colors.A_black)
    pygame.display.update()
    aboutMenuTitle.AutoScale(screenW,screenH,2,0.7)
    aboutMenuTitle.Draw((screenW//2,screenH//8))
    
    #Display all text
    T_About1 = Text.Text("Game created by: John Wiesner ",Rubik,25,Colors.A_white,screenW//2,screenH//2,gameDisplay,pos="center")

    T_ClickBait = Text.Text("MrJohnWeez",Rubik,22,Colors.A_RichBlueGreen,T_About1.getBottomCenter()[0],T_About1.getBottomCenter()[1],gameDisplay)
    bClickBait = Interactive.Button(T_About1.getBottomCenter()[0],T_About1.getBottomCenter()[1],T_ClickBait.GetWidth()+2,T_ClickBait.GetHieght(), Colors.A_black, gameDisplay, T_ClickBait, LoadMJWLink,pos="topcenter")
   
    T_About2 = Text.Text("Special thanks to Chuck Conner as alpha tester",Rubik,20,Colors.A_white,bClickBait.getBottomCenter()[0],bClickBait.getBottomCenter()[1]+10,gameDisplay,pos="topcenter")
    T_Copyright = Text.Text("MrJohnWeez©2018",Rubik,12,Colors.A_white,0,screenH,gameDisplay,pos="bottomleft")

    T_Back = Text.Text("Back",Rubik,30,Colors.A_white,screenW//2,screenH-5,gameDisplay)
    B_Back = Interactive.ButtonImage(T_Back.GetX(),T_Back.GetY(),int(50*4.3),50,IBLongBlue[1],IBLongBlue[0],IBLongBlue[2],gameDisplay,T_Back,MainMenu,pos="bottomcenter")

    TextList = [T_About1,T_About2,T_Copyright]
    buttons += [B_Back,bClickBait]
    for i in TextList: i.AddText(forceUpdate=True)
    
    while go:
        #Check for Button interaction
        for button in buttons: button.Update()
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: QuitSim()

MainMenu()