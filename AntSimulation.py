"""
MrJohnWeez©2018 all rights reserved.
This File contains all functions to generate the ant simulation game/sandbox.
"""

#3rd party imports
import random
import time
import pygame
import subprocess
import webbrowser
import sys
import os

#Self Custom imports
import Ant
import AntStepVar
import Colors
import CustomPath
import ImageManager as IM
import Interactive
import Text
import CustomMath

#Globals
global BNFont,screenH,screenW,DefualtScreenH,DefualtScreenW
global MenuX,MenuY,MenuW,MenuH
global gameDisplay,effectVolume,musicVolume

#TextPaths
BNFont = CustomPath.Path("assets\BebasNeue-Regular.ttf")
Rubik = CustomPath.Path("assets\Rubik-Regular.ttf")

#Define Screen constraints
DefualtScreenH = 600
DefualtScreenW = 800
screenH = DefualtScreenH
screenW = DefualtScreenW
MenuX,MenuY = 0,0
MenuW,MenuH = 200,screenH

#Set up pygame
pygame.init()
pygame.mixer.init()
gameDisplay = pygame.display.set_mode((screenW,screenH),pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
pygame.display.set_caption('Ant Simulation')
pygame.display.set_icon(pygame.image.load(CustomPath.Path("assets\GameIcon.png")))


if not os.path.exists(CustomPath.Path("ScreenShots")):
    os.makedirs(CustomPath.Path("ScreenShots"))
    
#Game sounds
buttonHoverSound1 = pygame.mixer.Sound(CustomPath.Path("assets\Sounds\\ButtonHoverOverSound1.ogg"))
buttonClickedSound = pygame.mixer.Sound(CustomPath.Path("assets\Sounds\\ButtonClickedSound1.ogg"))
clearWipeSound1 = pygame.mixer.Sound(CustomPath.Path("assets\Sounds\\ClearWipeSound1.ogg"))
clearWipeSound2 = pygame.mixer.Sound(CustomPath.Path("assets\Sounds\\clearWipeSound2.ogg"))
clearCanvasSound = pygame.mixer.Sound(CustomPath.Path("assets\Sounds\\ClearCanvasSound.ogg"))
killAntsSound = pygame.mixer.Sound(CustomPath.Path("assets\Sounds\\KillAntsSound.ogg"))
zombieAntSound = pygame.mixer.Sound(CustomPath.Path("assets\Sounds\\ZombieSound1.ogg"))
specialSound = pygame.mixer.Sound(CustomPath.Path("assets\Sounds\\secret.ogg"))
btSoundPack1 = [buttonHoverSound1,buttonClickedSound]

soundList = [buttonHoverSound1,buttonClickedSound,clearWipeSound1,clearWipeSound2,clearCanvasSound,killAntsSound,zombieAntSound,specialSound]

#Ant Sounds
antSound = pygame.mixer.Sound(CustomPath.Path("assets\Sounds\\BasicAntSound.ogg"))
plantAntSound = pygame.mixer.Sound(CustomPath.Path("assets\Sounds\\PlantAntSound.ogg"))
fireAntSound = pygame.mixer.Sound(CustomPath.Path("assets\Sounds\\FireAntSound.ogg"))
crazyAntSound = pygame.mixer.Sound(CustomPath.Path("assets\Sounds\\CrazyAntSound.ogg"))
woodAntSound = pygame.mixer.Sound(CustomPath.Path("assets\Sounds\\WoodAntSound.ogg"))
waterAntSound  = pygame.mixer.Sound(CustomPath.Path("assets\Sounds\\WaterAntSound.ogg"))

soundList += [antSound,plantAntSound,fireAntSound,crazyAntSound,woodAntSound,waterAntSound]

#Music
mainMenuMusic = CustomPath.Path("assets\Music\\PixelPuppies.mp3")
simulationMusic = CustomPath.Path("assets\Music\\BlueWorld.mp3")
creditsMusic = CustomPath.Path("assets\Music\\Pixelville.mp3")

#Sound Volumes
musicVolume = 5
effectVolume = 5
pygame.mixer.music.set_volume(musicVolume/10)
for s in soundList:
    s.set_volume(effectVolume/10) 


#Classes:
class StepBoxes:
    """Creates a set of interactive text boxes that executes functions based on given args. NOT A DEPENDENT CLASS but more like a c++ Struct!"""
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
        menuBG = Colors.A_black

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
        
        #Reset and random buttons
        relX, relY = (IB_UpStep.getTopRight()[0]+2,IB_UpStep.getTopRight()[1])
        T_random = Text.Text("R",BNFont,20,Colors.A_black,relX,relY,self.Gdisplay)
        B_random = Interactive.Button(relX,relY,15,self.h, Colors.A_clearN, self.Gdisplay, T_random, lambda: self.randomFunction(self.updateVars,self.boxObjects),sound=btSoundPack1)
        T_resetAntStep = Text.Text("C",BNFont,20,Colors.A_black,B_random.getTopRight()[0],relY,self.Gdisplay)
        B_resetAntStep = Interactive.Button(B_random.getTopRight()[0]+5,relY,15,self.h, Colors.A_clearN, self.Gdisplay, T_resetAntStep, lambda: self.clearFunction(self.updateVars,self.boxObjects),sound=btSoundPack1)

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
    """Loads MrJohnWeez website"""
    url = 'https://mrjohnweez.weebly.com'
    if sys.platform == 'darwin':    # in case of OS X
        subprocess.Popen(['open', url])
    else:
        webbrowser.open_new_tab(url)

def LoadMusicWebsite():
    """Loads website from where music was downloaded from"""
    url = 'http://soundimage.org/'
    if sys.platform == 'darwin':    # in case of OS X
        subprocess.Popen(['open', url])
    else:
        webbrowser.open_new_tab(url)

def LoadHelpLink():
    """Load Ant sim help on MrJohnWeez website"""
    url = 'https://mrjohnweez.weebly.com/ant-simulation.html'
    if sys.platform == 'darwin':    # in case of OS X
        subprocess.Popen(['open', url])
    else:
        webbrowser.open_new_tab(url)
    
def LoadSecret(playSound = False):
    """Does a secret thing"""
    pygame.mixer.music.pause()

    if playSound:
        spacing = 0
        fontSize = 25
        T_S1 = Text.Text("For the brave souls who found this link: Thou Art the chosen ones.",Rubik,fontSize,Colors.A_white,screenW//2,screenH//2,gameDisplay,pos="center",backgroundColor=Colors.A_black)
        T_S2 = Text.Text("For programming is a way of life, a journey, a quest, but without rest",Rubik,fontSize,Colors.A_white,T_S1.getBottomCenter()[0],T_S1.getBottomCenter()[1]+spacing,gameDisplay,pos="topcenter",backgroundColor=Colors.A_black)
        T_S3 = Text.Text("and unsolved puzzles. To you, true survivors, kings of men, I say this:",Rubik,fontSize,Colors.A_white,T_S2.getBottomCenter()[0],T_S2.getBottomCenter()[1]+spacing,gameDisplay,pos="topcenter",backgroundColor=Colors.A_black)
        T_S4 = Text.Text("Never gonna give you up, never gonna let you down,",Rubik,fontSize,Colors.A_white,T_S3.getBottomCenter()[0],T_S3.getBottomCenter()[1]+spacing,gameDisplay,pos="topcenter",backgroundColor=Colors.A_black)
        T_S5 = Text.Text("never gonna run around and desert you. Never gonna make you cry,",Rubik,fontSize,Colors.A_white,T_S4.getBottomCenter()[0],T_S4.getBottomCenter()[1]+spacing,gameDisplay,pos="topcenter",backgroundColor=Colors.A_black)
        T_S6 = Text.Text("never gonna say goodbye. Never gonna tell a lie and hurt you.",Rubik,fontSize,Colors.A_white,T_S5.getBottomCenter()[0],T_S5.getBottomCenter()[1]+spacing,gameDisplay,pos="topcenter",backgroundColor=Colors.A_black)
        
        TextList = [T_S1,T_S2,T_S3,T_S4,T_S5,T_S6]

        #Update text to screen
        for i in TextList: i.AddText(forceUpdate=True)
        
        specialSound.play()
    else:
        specialSound.stop()

def LoadSecret2():
    """Takes user to a YouTube video"""
    url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
    if sys.platform == 'darwin':    # in case of OS X
        subprocess.Popen(['open', url])
    else:
        webbrowser.open_new_tab(url)


def MusicToggle(isOn):
    """Turns music on or off when given a value"""
    if isOn:
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()
        
#Simulation Functions
def QuitSim():
    """Closes Ant simulation game"""
    pygame.quit()
    sys.exit()
    
class ToggleVar:
    """A basic toggle varible class"""
    def __init__(self, state=False):
        self.state = state

    def ToggleState(self):
        """Toggles the state of the bool value"""
        self.state = not self.state
        
class SimSpeed:
    """Given a starting value, when the value is increased 
    passed the max value it returns back to the min value"""
    def __init__(self, startValue, minValue, maxValue):
        self.value = startValue
        self.minValue = minValue
        self.maxValue = maxValue

    def Increase(self):
        """Value multiplies by two every time increase is called"""
        if self.value >= self.maxValue: self.value = self.minValue
        else: self.value = self.value*2

class AntSpeed:
    """Sets how frequently an ant will update thus changing its speed"""
    def __init__(self, startValue, minValue, maxValue):
        self.value = startValue
        self.default = startValue
        self.minValue = minValue
        self.maxValue = maxValue

    def UpdateAntSpeed(self, textBox):
        """Updates the value of the ant speed if given a string or int value.
        Also updates its given textbox on screen"""
        self.value = textBox.getText()
        if self.value.isdigit():
            self.value = int(self.value)
        elif len(self.value) > 0 and self.value[0] == "-":
            self.value = self.minValue
        else:
            self.value = self.default
        
        self.value = CustomMath.Clamp(self.value,self.minValue,self.maxValue)
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
        """Use the user's active tool"""
        mouse = pygame.mouse.get_pos()
        newStep = self.antSteps.GetGroupValues()
        def HelperAdd():
            """Spawns the ant type then updates the count text"""
            tempAnt.Spawn()         
            self.T_AntCount.AddText(str(Ant.Ant.GetAntCount())+"/"+str(Ant.Ant.antLimit),True)
        
        if len(Ant.Ant.antArray) < Ant.Ant.antLimit:
            if self.activeTool == "Ant":
                tempAnt = Ant.Ant((mouse[0]),(mouse[1]),pygame.Rect(MenuW,0,screenW,screenH),0,gameDisplay,newStep, self.antSpeed.value)
                HelperAdd()
                antSound.play()
            elif self.activeTool == "WaterAnt":
                tempAnt = Ant.AntWater((mouse[0]),(mouse[1]),pygame.Rect(MenuW,0,screenW,screenH),0,gameDisplay,newStep, self.antSpeed.value)
                HelperAdd()
                waterAntSound.play()
            elif self.activeTool == "WoodAnt":
                tempAnt = Ant.AntWood((mouse[0]),(mouse[1]),pygame.Rect(MenuW,0,screenW,screenH),0,gameDisplay,newStep, self.antSpeed.value)
                HelperAdd()
                woodAntSound.play()
            elif self.activeTool == "FireAnt":
                newList = []
                for i in newStep:
                    i += 14 #Step offset of fire ant type
                    if i > screenH:
                        i = (i - screenH)
                    elif i < 0:
                        i = screenH + i
                    newList += [i]
                tempAnt = Ant.AntFire((mouse[0]),(mouse[1]),pygame.Rect(MenuW,0,screenW,screenH),0,gameDisplay,newList, self.antSpeed.value)
                HelperAdd()
                fireAntSound.play()
            elif self.activeTool == "PlantAnt":
                tempAnt = Ant.AntPlant((mouse[0]),(mouse[1]),pygame.Rect(MenuW,0,screenW,screenH),0,gameDisplay,newStep, self.antSpeed.value)
                HelperAdd()
                plantAntSound.play()
            elif self.activeTool == "ZombieAnt":
                tempAnt = Ant.AntZombie((mouse[0]),(mouse[1]),pygame.Rect(MenuW,0,screenW,screenH),0,gameDisplay,newStep, self.antSpeed.value)
                HelperAdd()
                zombieAntSound.play()
            elif self.activeTool == "CrazyAnt":
                tempAnt = Ant.AntCrazy((mouse[0]),(mouse[1]),pygame.Rect(MenuW,0,screenW,screenH),0,gameDisplay,newStep, self.antSpeed.value)
                HelperAdd()
                crazyAntSound.play()
                
        if self.activeTool == "RemovePath":
            """Places a white rectange on screen with the user's cusor being in the center"""
            cubeSize = 15
            x = mouse[0] - cubeSize
            y = mouse[1] - cubeSize
            x = CustomMath.Clamp(x,MenuW,screenW)
            y = CustomMath.Clamp(y,0,screenH)
            gameDisplay.fill(Colors.A_white, ((x,y), (cubeSize*2,cubeSize*2)))
            pygame.display.update((x,y), (cubeSize*2,cubeSize*2))
        elif self.activeTool == "RemoveAnt":
            """Kills all ant within a square radius of the user's cursor"""
            cubeSize = 15
            x = mouse[0] - cubeSize
            y = mouse[1] - cubeSize
            x = CustomMath.Clamp(x,MenuW,screenW)
            y = CustomMath.Clamp(y,0,screenH)
            Ant.Ant.KillAntsInRect(pygame.Rect(x,y,cubeSize*2,cubeSize*2))
            if self.isPaused.state:
                Ant.Ant.UpdateAllAnts()
                #Update ant count if ants die
                if self.T_AntCount.GetText() != str(Ant.Ant.GetAntCount())+"/"+str(Ant.Ant.antLimit):
                    self.T_AntCount.AddText(str(Ant.Ant.GetAntCount())+"/"+str(Ant.Ant.antLimit),True)

    def ChangeTool(self, newTool):
        """Sets the active tool to the new given string"""
        self.activeTool = newTool
    



def AntSimulation():
    """Main ant simulation loop"""
    global screenW,screenH,MenuH    #Not 100% sure why these needed to be re-declared

    pygame.mixer.music.load(simulationMusic)
    pygame.mixer.music.play(-1)

    #Clears screen
    gameDisplay.fill(Colors.A_black)
    pygame.display.update()

    #Custom Event Handling for timers
    Spawn = True
    SpawnRate = 1
    spawn_Event  = pygame.USEREVENT + 1
    coolDown = 0

    #Simulation Vars
    r = [] #Ants pixels to render list
    Ant.Ant.SetAntLimit(500)
    Ant.Ant.maxSpeed = 6000
    input_boxes = []    #All input boxe objects in ant simulation game
    buttons = []        #All button objects in ant simulation game
    texts = []          #All single text objects in ant simulation game
    simulationSpeed = SimSpeed(1,1,4096)
    TicksLeft = simulationSpeed.value   #How many ticks are left before the next ant update
    antSteps = AntStepVar.AntStepGroup(1,screenH)
    antSpeed = AntSpeed(Ant.Ant.maxSpeed-1000,1,Ant.Ant.maxSpeed)
    isPaused = ToggleVar()

    #Button Functions
    def togglePause():
        """Changes the pause state of the game"""
        isPaused.ToggleState()
        MusicToggle(isPaused.state)
        bPause.ChangeMsg("Play") if isPaused.state else bPause.ChangeMsg("Pause")
        bPause.Update()
        bPause.DrawButton()

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

    def SpeedButton():
        """Decreases the simulation speed by a factor of double the prevous value"""
        simulationSpeed.Increase()
        B_Speed.ChangeMsg("x"+str(simulationSpeed.value))
        B_Speed.Update()
        B_Speed.DrawButton()

    #Plain texts on screen
    T_Copyright = Text.Text("MrJohnWeez™2018",Rubik,12,Colors.A_white,0,screenH,gameDisplay,pos="bottomleft",backgroundColor=Colors.A_black)
    T_AntCount = Text.Text("0/"+str(Ant.Ant.antLimit),BNFont,20,Colors.A_white,MenuW,screenH,gameDisplay,True,"bottomright",Colors.A_black)
    texts += [T_Copyright,T_AntCount]

    #Define Buttons

    #Low Left of menu
    T_mainmenu = Text.Text("Back",Rubik,21,Colors.A_white,T_Copyright.getTopLeft()[0],T_Copyright.getTopLeft()[1],gameDisplay)
    textHeight = T_mainmenu.GetHieght()+4
    B_mainmenu = Interactive.ButtonImage(T_mainmenu.GetX(),T_mainmenu.GetY(),int(textHeight*IM.AspectShort),textHeight,IM.IBShortBlue[1],IM.IBShortBlue[0],IM.IBShortBlue[2],gameDisplay,T_mainmenu,MainMenu,pos="bottomleft",sound=btSoundPack1)
    
    #High Right of menu
    T_reset = Text.Text("Reset",Rubik,20,Colors.A_white,MenuW,MenuY,gameDisplay)
    B_reset = Interactive.ButtonImage(T_reset.GetX(),T_reset.GetY(),int(textHeight*IM.AspectShort),textHeight,IM.IBShortRed[1],IM.IBShortRed[0],IM.IBShortRed[2],gameDisplay,T_reset,ClearSim,pos="topright",sound=[buttonHoverSound1,clearWipeSound1])
    
    T_kill = Text.Text("Kill",Rubik,20,Colors.A_white,B_reset.getBottomRight()[0],B_reset.getBottomRight()[1],gameDisplay)
    B_kill = Interactive.ButtonImage(T_kill.GetX(),T_kill.GetY(),int(textHeight*IM.AspectShort),textHeight,IM.IBShortRed[1],IM.IBShortRed[0],IM.IBShortRed[2],gameDisplay,T_kill,Ant.Ant.KillAllAnts,pos="topright",sound=[buttonHoverSound1,killAntsSound]) 
    
    T_clearPath = Text.Text("Clear",Rubik,20,Colors.A_white,B_kill.getBottomRight()[0],B_kill.getBottomRight()[1],gameDisplay)
    B_clearPath = Interactive.ButtonImage(T_clearPath.GetX(),T_clearPath.GetY(),int(textHeight*IM.AspectShort),textHeight,IM.IBShortRed[1],IM.IBShortRed[0],IM.IBShortRed[2],gameDisplay,T_clearPath,ClearPaths,pos="topright",sound=[buttonHoverSound1,clearCanvasSound])
    
    #High Left of menu
    T_pause = Text.Text("Pause",Rubik,20,Colors.A_white,MenuX,MenuY,gameDisplay)
    bPause = Interactive.ButtonImage(T_pause.GetX(),T_pause.GetY(),int(textHeight*IM.AspectShort),textHeight,IM.IBShortLightGreen[1],IM.IBShortLightGreen[0],IM.IBShortLightGreen[2],gameDisplay,T_pause,togglePause,pos="topleft",sound=btSoundPack1)

    T_speedLabel1 = Text.Text("Times",Rubik,18,Colors.A_white,bPause.getBottomRight()[0]-15,bPause.getBottomRight()[1]+5,gameDisplay,pos="topcenter")
    T_speedLabel2 = Text.Text("Slower:",Rubik,18,Colors.A_white,T_speedLabel1.getBottomCenter()[0],T_speedLabel1.getBottomCenter()[1],gameDisplay,pos="topcenter")

    T_Speed = Text.Text("x"+str(simulationSpeed.value),Rubik,19,Colors.A_white,T_speedLabel2.getBottomCenter()[0]+7,T_speedLabel2.getBottomCenter()[1],gameDisplay,pos="topcenter")
    B_Speed = Interactive.ButtonImage(T_Speed.GetX(),T_Speed.GetY(),int(textHeight*IM.AspectShort),textHeight,IM.IBShortGray[1],IM.IBShortGray[0],IM.IBShortGray[2],gameDisplay,T_Speed,SpeedButton,pos="topcenter",sound=btSoundPack1)

    texts += [T_speedLabel1,T_speedLabel2]
    buttons += [B_mainmenu,B_reset,B_kill,B_clearPath,bPause,B_Speed]

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
    StepBox1 = StepBoxes(MenuW//2.6,screenH-180,BNFont, 20, gameDisplay, UpdateStepVar, ResetStepVars, RandomStepVars, antSteps.GetGroup(), antSpeed.UpdateAntSpeed)
    stepBoxesList = [StepBox1]

    #aTB_ = Ant Type Buttons
    aTB_x = MenuW//2
    aTB_y = MenuH//4
    aTB_Color = Colors.A_white
    aTB_fontSize = 20
    aTB_BtnH = int(21*1.5)
    aTB_BtnW = int(textHeight*IM.AspectShort)+17
    aTB_spacing = 2

    #Left Side of menu
    T_Ant = Text.Text("Ant",Rubik,aTB_fontSize,aTB_Color,aTB_x,aTB_y,gameDisplay)
    B_Ant = Interactive.ButtonImage(T_Ant.GetX(),T_Ant.GetY(),aTB_BtnW,aTB_BtnH,IM.IBShortGray[1],IM.IBShortGray[0],IM.IBShortGray[2],gameDisplay,T_Ant,lambda: tool.ChangeTool("Ant"),pos="topright",sound=btSoundPack1)
    
    T_AntWater = Text.Text("Water",Rubik,aTB_fontSize,aTB_Color,B_Ant.getBottomRight()[0],B_Ant.getBottomRight()[1]+aTB_spacing,gameDisplay)
    B_AntWater = Interactive.ButtonImage(T_AntWater.GetX(),T_AntWater.GetY(),aTB_BtnW,aTB_BtnH,IM.IBShortDarkBlue[1],IM.IBShortDarkBlue[0],IM.IBShortDarkBlue[2],gameDisplay,T_AntWater,lambda: tool.ChangeTool("WaterAnt"),pos="topright",sound=btSoundPack1)
    
    T_AntWood = Text.Text("Wood",Rubik,aTB_fontSize,aTB_Color,B_AntWater.getBottomRight()[0],B_AntWater.getBottomRight()[1]+aTB_spacing,gameDisplay)
    B_AntWood = Interactive.ButtonImage(T_AntWood.GetX(),T_AntWood.GetY(),aTB_BtnW,aTB_BtnH,IM.IBShortLightBrown[1],IM.IBShortLightBrown[0],IM.IBShortLightBrown[2],gameDisplay,T_AntWood,lambda: tool.ChangeTool("WoodAnt"),pos="topright",sound=btSoundPack1)
    
    T_AntFire = Text.Text("Fire",Rubik,aTB_fontSize,aTB_Color,B_AntWood.getBottomRight()[0],B_AntWood.getBottomRight()[1]+aTB_spacing,gameDisplay)
    B_AntFire = Interactive.ButtonImage(T_AntFire.GetX(),T_AntFire.GetY(),aTB_BtnW,aTB_BtnH,IM.IBShortLava[1],IM.IBShortLava[0],IM.IBShortLava[2],gameDisplay,T_AntFire,lambda: tool.ChangeTool("FireAnt"),pos="topright",sound=btSoundPack1)
    
    #Right side of menu
    T_AntPlant = Text.Text("Plant",Rubik,aTB_fontSize,aTB_Color,aTB_x,aTB_y,gameDisplay)
    B_AntPlant = Interactive.ButtonImage(T_AntPlant.GetX(),T_AntPlant.GetY(),aTB_BtnW,aTB_BtnH,IM.IBShortLightGreen[1],IM.IBShortLightGreen[0],IM.IBShortLightGreen[2],gameDisplay,T_AntPlant,lambda: tool.ChangeTool("PlantAnt"),pos="topleft",sound=btSoundPack1)
    
    T_AntZombie = Text.Text("Zombie",Rubik,aTB_fontSize,aTB_Color,B_AntPlant.getBottomLeft()[0],B_AntPlant.getBottomLeft()[1]+aTB_spacing,gameDisplay)
    B_AntZombie = Interactive.ButtonImage(T_AntZombie.GetX(),T_AntZombie.GetY(),aTB_BtnW,aTB_BtnH,IM.IBShortPurple[1],IM.IBShortPurple[0],IM.IBShortPurple[2],gameDisplay,T_AntZombie,lambda: tool.ChangeTool("ZombieAnt"),pos="topleft",sound=btSoundPack1)
    
    T_AntCrazy = Text.Text("Crazy",Rubik,aTB_fontSize,aTB_Color,B_AntZombie.getBottomLeft()[0],B_AntZombie.getBottomLeft()[1]+aTB_spacing,gameDisplay)
    B_AntCrazy = Interactive.ButtonImage(T_AntCrazy.GetX(),T_AntCrazy.GetY(),aTB_BtnW,aTB_BtnH,IM.IBShortYellow[1],IM.IBShortYellow[0],IM.IBShortYellow[2],gameDisplay,T_AntCrazy,lambda: tool.ChangeTool("CrazyAnt"),pos="topleft",sound=btSoundPack1)
    
    #Tools (middle of menu)
    spacingFromTop = 20
    toolSpacing = 2
    toolFontSize = 18
    T_ClearMouse = Text.Text("Remove Path",Rubik,toolFontSize,aTB_Color,B_AntFire.getBottomRight()[0],B_AntFire.getBottomRight()[1]+spacingFromTop,gameDisplay)
    B_ClearMouse = Interactive.ButtonImage(T_ClearMouse.GetX(),T_ClearMouse.GetY(),int(textHeight*IM.AspectLong),aTB_BtnH,IM.IBLongYellow[1],IM.IBLongYellow[0],IM.IBLongYellow[2],gameDisplay,T_ClearMouse,lambda: tool.ChangeTool("RemovePath"),pos="topcenter",sound=btSoundPack1)
    
    T_KillMouse = Text.Text("Remove Ant",Rubik,toolFontSize,aTB_Color,B_ClearMouse.getBottomCenter()[0],B_ClearMouse.getBottomCenter()[1]+toolSpacing,gameDisplay)
    B_KillMouse = Interactive.ButtonImage(T_KillMouse.GetX(),T_KillMouse.GetY(),int(textHeight*IM.AspectLong),aTB_BtnH,IM.IBLongRedFade[1],IM.IBLongRedFade[0],IM.IBLongRedFade[2],gameDisplay,T_KillMouse,lambda: tool.ChangeTool("RemoveAnt"),pos="topcenter",sound=btSoundPack1)
    
    buttons += [B_Ant,B_AntWater,B_AntWood,B_AntFire,B_AntPlant,B_AntZombie,B_AntCrazy,B_ClearMouse,B_KillMouse]


    def ResetSim():
        """Make the state of the simulation new."""
        pygame.draw.rect(gameDisplay, Colors.A_white, pygame.Rect(MenuW,0,screenW,screenH))
        pygame.draw.rect(gameDisplay, Colors.A_black, (0,0,MenuW,MenuH))

        #Reset buttons
        for button in buttons:
            button.DrawButton()
        for box in input_boxes:
            box.update()
        for text in texts:
            text.AddText(forceUpdate=True)
        for sbox in stepBoxesList:
            for T in sbox.textObjects:
                T.AddText(forceUpdate=True)
            for B in sbox.boxObjects:
                B.update()
            for Bn in sbox.buttonObjects:
                Bn.DrawButton()
        Ant.Ant.KillAllAnts()
        pygame.display.update()
        

    #Set up Simulation for setup
    class ButtonRect:
        def __init__(self, bRect, mouseOver=False):
            self.bRect = bRect
            self.mouseOver = mouseOver
        
    ResetSim()
    buttonRects = []
    buttonRects2 = []
    for button in buttons:
        buttonRects += [ButtonRect(button.getRect())]

    for sbox in stepBoxesList:
        for Bn in sbox.buttonObjects:
            buttonRects2 += [ButtonRect(Bn.getRect())]
            
    #Main loop
    while True:
        
        mouse = pygame.mouse.get_pos()
        
        #Highly optimized GUI Button interaction
        mouseOverMenu = MenuX+MenuW > mouse[0] > -1000 and MenuY+MenuH > mouse[1] > -1000
        if mouseOverMenu:
            for i in range(len(buttons)):
                mouseOverBox = buttonRects[i].bRect.x+buttonRects[i].bRect.w > mouse[0] > buttonRects[i].bRect.x and buttonRects[i].bRect.y+buttonRects[i].bRect.h > mouse[1] > buttonRects[i].bRect.y
                if mouseOverBox:
                    buttonRects[i].mouseOver = False
                    buttons[i].Update()
                elif not mouseOverBox and not buttonRects[i].mouseOver:
                    buttonRects[i].mouseOver = True
                    buttons[i].Update()

            for i in range(len(sbox.buttonObjects)):
                mouseOverBox = buttonRects2[i].bRect.x+buttonRects2[i].bRect.w > mouse[0] > buttonRects2[i].bRect.x and buttonRects2[i].bRect.y+buttonRects2[i].bRect.h > mouse[1] > buttonRects2[i].bRect.y
                if mouseOverBox:
                    buttonRects2[i].mouseOver = False
                    sbox.buttonObjects[i].Update()
                elif not mouseOverBox and not buttonRects2[i].mouseOver:
                    buttonRects2[i].mouseOver = True
                    sbox.buttonObjects[i].Update()

        #Check all events in python (IO inputs)
        for event in pygame.event.get():
            

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

            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                #Handle input box events in the stepboxes (Text box interaction)
                for box in input_boxes:
                    box.handle_event(event)

                #Handle reset and clear button in the stepboxes
                for sbox in stepBoxesList:
                    for B in sbox.boxObjects:
                        B.handle_event(event)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p or event.key == pygame.K_LSHIFT:
                        togglePause()
                    elif event.key == pygame.K_e:
                        Ant.Ant.KillAllAnts()
                    elif event.key == pygame.K_SPACE:
                        ClearSim()
                    elif event.key == pygame.K_q:
                        AntSimulation()
                    elif event.key == pygame.K_s:
                        SpeedButton()
                    elif event.key == pygame.K_ESCAPE:
                        MainMenu()
                    elif event.key == pygame.K_w:
                        rect = pygame.Rect(25, 25, 100, 50)
                        screenshot = pygame.Surface((100, 50))
                        screenshot.blit(gameDisplay, (0,0), area=rect)
                        path = CustomPath.Path("ScreenShots")
                        time_taken = time.asctime(time.localtime(time.time()))
                        time_taken = time_taken.replace(" ", "_")
                        time_taken = time_taken.replace(":", "-")
                        path = path + "\\" + time_taken + ".jpg"
                        pygame.image.save(gameDisplay, path)
                        print("A Screen shot has been taken and saved as ", path)

            #If window has been resized
            elif event.type==pygame.VIDEORESIZE:
                newWidth, newHeight = event.dict['size']
                if newWidth < DefualtScreenW:
                    newWidth = DefualtScreenW
                if newHeight < DefualtScreenH:
                    newHeight = DefualtScreenH
                
                screen=pygame.display.set_mode((newWidth,newHeight),pygame.RESIZABLE)
                screenW = newWidth
                screenH = newHeight
                MenuH = newHeight
                antSteps.SetMaxValue(screenH)
                AntSimulation()
                    

        
        TicksLeft -= 1
        # Move every ant, if correct simulation timing and if not paused 
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
    global screenW,screenH,MenuH    #Not 100% sure why these needed to be re-declared

    pygame.mixer.music.load(mainMenuMusic)
    pygame.mixer.music.set_volume((musicVolume/10)*0.4)
    pygame.mixer.music.play(-1)

    mainMenuTitle = IM.ImageType(CustomPath.Path("assets\AntSimTitle.png"),gameDisplay)
    buttons = []
    TextList = []

    #Draw background images
    gameDisplay.fill(Colors.A_black)
    pygame.display.update()
    mainMenuTitle.AutoScale(screenW,screenH,0.1,0.1)
    mainMenuTitle.Draw((screenW//2,screenH//8))
    
    def UpdateMusicVolume(shouldIncrease = True):
        """Increase the music volume by a factor of %10"""
        global musicVolume
        if shouldIncrease:
            musicVolume += 1
        if musicVolume > 10:
            musicVolume = 0
        pygame.mixer.music.set_volume((musicVolume/10)*0.4)
        B_MusicVol.ChangeMsg(str(musicVolume*10)+"%")

    def UpdateEffectVolume(shouldIncrease = True):
        """Increase the effects volume by a factor of %10"""
        global effectVolume
        if shouldIncrease:
            effectVolume += 1
        if effectVolume > 10:
            effectVolume = 0
        for s in soundList: s.set_volume(effectVolume/10)
        B_EffectVol.ChangeMsg(str(effectVolume*10)+"%")


    #Setup 4 main buttons in middle of screen
    spacing = 30
    T_Play = Text.Text("Play",Rubik,30,Colors.A_white,screenW//2,int(screenH*.4),gameDisplay)
    B_Play = Interactive.ButtonImage(T_Play.GetX(),T_Play.GetY(),int(50*IM.AspectLong),50,IM.IBLongBlue[1],IM.IBLongBlue[0],IM.IBLongBlue[2],gameDisplay,T_Play,AntSimulation,pos="center",sound=btSoundPack1)

    T_Credits = Text.Text("Credits",Rubik,30,Colors.A_white,B_Play.getCenter()[0],B_Play.getBottomLeft()[1]+spacing,gameDisplay)
    B_Credits = Interactive.ButtonImage(T_Credits.GetX(),T_Credits.GetY(),int(50*IM.AspectLong),50,IM.IBLongBlue[1],IM.IBLongBlue[0],IM.IBLongBlue[2],gameDisplay,T_Credits,CreditsMenu,pos="center",sound=btSoundPack1)

    T_Help = Text.Text("Help",Rubik,30,Colors.A_white,B_Credits.getCenter()[0],B_Credits.getBottomLeft()[1]+spacing,gameDisplay)
    B_Help  = Interactive.ButtonImage(T_Help.GetX(),T_Help.GetY(),int(50*IM.AspectLong),50,IM.IBLongBlue[1],IM.IBLongBlue[0],IM.IBLongBlue[2],gameDisplay,T_Help,LoadHelpLink,pos="center",sound=btSoundPack1)

    T_Quit = Text.Text("Quit",Rubik,30,Colors.A_white,B_Help.getCenter()[0],B_Help.getBottomLeft()[1]+spacing,gameDisplay)
    B_Quit = Interactive.ButtonImage(T_Quit.GetX(),T_Quit.GetY(),int(50*IM.AspectLong),50,IM.IBLongBlue[1],IM.IBLongBlue[0],IM.IBLongBlue[2],gameDisplay,T_Quit,QuitSim,pos="center",sound=btSoundPack1)

    buttons += [B_Play,B_Quit,B_Help,B_Credits]

    #Include copyright in lower left
    T_Copyright = Text.Text("MrJohnWeez™2018",Rubik,12,Colors.A_white,0,screenH,gameDisplay,pos="bottomleft")
    TextList += [T_Copyright]

    #Set up volume buttons in lower left
    buttonSize = 20
    T_MusicLabel = Text.Text("Music:",Rubik,buttonSize,Colors.A_white,T_Copyright.getTopLeft()[0],T_Copyright.getTopLeft()[1],gameDisplay,pos="bottomleft")
    T_MusicVol = Text.Text(str(musicVolume*10)+"%",Rubik,buttonSize,Colors.A_white,T_MusicLabel.getBottomRight()[0],T_MusicLabel.getBottomRight()[1],gameDisplay)
    B_MusicVol = Interactive.ButtonImage(T_MusicVol.GetX(),T_MusicVol.GetY(),int(T_MusicLabel.GetHieght()*IM.AspectLong),T_MusicLabel.GetHieght(),IM.IBLongBlue[1],IM.IBLongBlue[0],IM.IBLongBlue[2],gameDisplay,T_MusicVol,UpdateMusicVolume,pos="bottomleft",sound=btSoundPack1)
    
    T_EffectLabel = Text.Text("Effects:",Rubik,buttonSize,Colors.A_white,T_MusicLabel.getTopLeft()[0],T_MusicLabel.getTopLeft()[1],gameDisplay,pos="bottomleft")
    T_EffectVol = Text.Text(str(effectVolume*10)+"%",Rubik,buttonSize,Colors.A_white,T_EffectLabel.getBottomRight()[0],T_EffectLabel.getBottomRight()[1],gameDisplay)
    B_EffectVol = Interactive.ButtonImage(T_EffectVol.GetX(),T_EffectVol.GetY(),int(T_EffectLabel.GetHieght()*IM.AspectLong),T_EffectLabel.GetHieght(),IM.IBLongBlue[1],IM.IBLongBlue[0],IM.IBLongBlue[2],gameDisplay,T_EffectVol,UpdateEffectVolume,pos="bottomleft",sound=btSoundPack1)

    #Music button in lower right
    T_MusicKnowledge = Text.Text("Music By Eric Matyas",Rubik,14,Colors.A_white,screenW,screenH,gameDisplay)
    B_MusicKnowledge = Interactive.Button(T_MusicKnowledge.GetX(),T_MusicKnowledge.GetY(),T_MusicKnowledge.GetWidth(),T_MusicKnowledge.GetHieght(), Colors.A_black, gameDisplay, T_MusicKnowledge, LoadMusicWebsite,pos="bottomright",sound=btSoundPack1)
    
    TextList += [T_MusicLabel,T_EffectLabel]
    buttons += [B_MusicVol,B_EffectVol,B_MusicKnowledge]

    for i in TextList: i.AddText(forceUpdate=True)

    while True:
        #Check for Button interaction
        for button in buttons: button.Update()
        
        for event in pygame.event.get():
            #Quit Game
            if event.type == pygame.QUIT: QuitSim()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    QuitSim()

            #If window has been resized
            elif event.type==pygame.VIDEORESIZE:
                newWidth, newHeight = event.dict['size']
                if newWidth < DefualtScreenW:
                    newWidth = DefualtScreenW
                if newHeight < DefualtScreenH:
                    newHeight = DefualtScreenH
                
                pygame.display.set_mode((newWidth,newHeight),pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
                screenW = newWidth
                screenH = newHeight
                MenuH = newHeight
                pygame.mixer.music.stop()
                MainMenu()


def CreditsMenu():
    """Credis menu"""
    global screenW,screenH,MenuH,loadSECRET    #Not 100% sure why these needed to be re-declared

    pygame.mixer.music.set_volume((musicVolume/10)*0.35)
    pygame.mixer.music.load(creditsMusic)
    pygame.mixer.music.play(-1)

    credisMenuTitle = IM.ImageType(CustomPath.Path("assets\CreditsTitle.png"),gameDisplay)
    buttons = []

    gameDisplay.fill(Colors.A_black)
    pygame.display.update()
    credisMenuTitle.AutoScale(screenW,screenH,2,0.7)
    credisMenuTitle.Draw((screenW//2,screenH//8))

    loadSECRET = False
    def _main_menu():
        global loadSECRET
        if loadSECRET: 
            LoadSecret2()
            LoadSecret()
        MainMenu()
        
    def _helper():
        global loadSECRET
        loadSECRET = True
        LoadSecret(True)
    
    #Display all text
    T_About1 = Text.Text("Game created by: John Wiesner ",Rubik,25,Colors.A_white,screenW//2,screenH//2,gameDisplay,pos="center")

    T_ClickBait = Text.Text("MrJohnWeez",Rubik,22,Colors.A_RichBlueGreen,T_About1.getBottomCenter()[0],T_About1.getBottomCenter()[1],gameDisplay)
    B_ClickBait = Interactive.Button(T_About1.getBottomCenter()[0],T_About1.getBottomCenter()[1],T_ClickBait.GetWidth()+2,T_ClickBait.GetHieght(), Colors.A_black, gameDisplay, T_ClickBait, LoadMJWLink,pos="topcenter",sound=btSoundPack1)
   
    T_About2 = Text.Text("Special thanks to Chuck Conner for game testing",Rubik,20,Colors.A_white,B_ClickBait.getBottomCenter()[0],B_ClickBait.getBottomCenter()[1]+10,gameDisplay,pos="topcenter")
    T_Copyright = Text.Text("MrJohnWeez™2018",Rubik,12,Colors.A_white,0,screenH,gameDisplay,pos="bottomleft")

    T_Back = Text.Text("Back",Rubik,30,Colors.A_white,screenW//2,screenH-5,gameDisplay)
    B_Back = Interactive.ButtonImage(T_Back.GetX(),T_Back.GetY(),int(50*4.3),50,IM.IBLongBlue[1],IM.IBLongBlue[0],IM.IBLongBlue[2],gameDisplay,T_Back,_main_menu,pos="bottomcenter",sound=btSoundPack1)

    T_Secret = Text.Text("",Rubik,14,Colors.A_black,0,0,gameDisplay)
    B_Secret = Interactive.Button(0,0,screenW,40, Colors.A_black, gameDisplay, T_Secret, _helper,sound=[buttonHoverSound1,buttonClickedSound])
    
    TextList = [T_About1,T_About2,T_Copyright]
    buttons += [B_Back,B_ClickBait,B_Secret]

    for i in TextList: i.AddText(forceUpdate=True)
    
    while True:
        #Check for Button interaction
        for button in buttons:
            button.Update()

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: QuitSim()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    MainMenu()

            #If window has been resized
            elif event.type==pygame.VIDEORESIZE:
                newWidth, newHeight = event.dict['size']
                if newWidth < DefualtScreenW:
                    newWidth = DefualtScreenW
                if newHeight < DefualtScreenH:
                    newHeight = DefualtScreenH
                
                screen=pygame.display.set_mode((newWidth,newHeight),pygame.RESIZABLE)
                screenW = newWidth
                screenH = newHeight
                MenuH = newHeight
                CreditsMenu()

MainMenu()  #launch game