
import pygame
import time


"""
ToDo List:
-Change Color Shading values in classes
-Change Ant class to update the ant given the display 


202 = 250 fps

"""

#Custom
import Ant
import Colors
import CustomPath
import Text
import AntStepVar
import Interactive

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
antList = []
isPaused = False
r = [] #Pixels to render list
allowedAntNum = 500
input_boxes = []
buttons = []
texts = []

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



#Classes:
class StepBoxes:
    """Creates a set of interactive text boxes that executes functions based on given args. NOT A DEP CLASS!"""
    def __init__(self, x, y, fontPath, fontSize, display, runFunction, clearFunction, updateVars):
        self.x = x
        self.y = y
        self.fontPath = fontPath
        self.fontSize = fontSize
        self.Gdisplay = display
        self.runFunction = runFunction
        self.clearFunction = clearFunction
        self.updateVars = updateVars
        self.xBox = self.x+6

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
        IB_UpStep = Interactive.InputBox(self.xBox, self.y, 50, fontSize,boxColor,menuBG,self.Gdisplay,T_upStep,lambda x: self.runFunction(self.updateVars[0], x))
        IB_DownStep = Interactive.InputBox(self.xBox, T_UpStep.GetY()+T_UpStep.GetHieght(), 50, fontSize,boxColor,menuBG,self.Gdisplay,T_downStep,lambda x: self.runFunction(self.updateVars[1], x))
        IB_RightStep = Interactive.InputBox(self.xBox, T_DownStep.GetY()+T_DownStep.GetHieght(), 50, fontSize,boxColor,menuBG,self.Gdisplay,T_rightStep,lambda x: self.runFunction(self.updateVars[2], x))
        IB_LeftStep = Interactive.InputBox(self.xBox, T_RightStep.GetY()+T_RightStep.GetHieght(), 50, fontSize,boxColor,menuBG,self.Gdisplay,T_leftStep,lambda x: self.runFunction(self.updateVars[3], x))
        self.boxObjects = [IB_UpStep,IB_DownStep,IB_RightStep,IB_LeftStep]
        self.h = abs(IB_LeftStep.getBottomRight()[1]-IB_UpStep.getTopRight()[1])
        
        #Reset Button
        relX, relY = (IB_UpStep.getTopRight()[0]+2,IB_UpStep.getTopRight()[1])
        T_reset = Text.Text("R",BNFont,20,Colors.A_black,relX,relY,self.Gdisplay)
        B_reset = Interactive.Button(relX,relY,15,self.h, Colors.A_clearN, self.Gdisplay, T_reset, lambda: self.clearFunction(self.updateVars,self.boxObjects))

        self.buttonObjects = [B_reset]
        self.w = abs(max(T_UpStep.GetX(),T_DownStep.GetX(),T_RightStep.GetX(),T_LeftStep.GetX(),T_Title.GetX())-(B_reset.x+B_reset.w))


#TextBoxes
T_Watermark = Text.Text("By: MrJohnWeez",BNFont,16,Colors.A_white,1,screenH+3,gameDisplay,True,"bottomleft",Colors.A_optionsBg)
T_AntCount = Text.Text("0/"+str(allowedAntNum),BNFont,20,Colors.A_white,1,screenH+3-16,gameDisplay,True,"bottomleft",Colors.A_optionsBg)
texts += [T_Watermark,T_AntCount]


#Button Functions
def togglePause():
    global isPaused
    isPaused = not isPaused
    if isPaused: bPause.ChangeMsg("Play")
    else: bPause.ChangeMsg("Pause")

def clearSim():
    """Clears the entire ant screen of any ants and their paths"""
    antList.clear()
    pygame.draw.rect(gameDisplay, Colors.A_white, pygame.Rect(MenuW,0,screenW,screenH))
    pygame.display.update(pygame.Rect(MenuW,0,screenW,screenH))
    T_AntCount.AddText(str(len(antList))+"/"+str(allowedAntNum),True)

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


def UpdateStepVar(var, textBox):
    var.UpdateByString(textBox.getText())
    textBox.updateText(str(var.GetValue()))

def ResetStepVars(varList, boxVars):
    for i in range(len(varList)):
        varList[i].Reset()
        boxVars[i].updateText(str(varList[i].GetValue()))

#Ant step boxes module
StepBox1 = StepBoxes(50,screenH+3-200,BNFont, 20, gameDisplay, UpdateStepVar, ResetStepVars, AntStepVars)
stepBoxes = [StepBox1]

#Simulation Functions
def QuitSim():
    """Quits game"""
    pygame.quit()
    quit()

def ResetSim():
    """Make the state of the simulation new."""
    gameDisplay.fill(Colors.A_white)
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
    pygame.display.update()
    antList.clear()

    


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
        elif not mouseOverMenu and event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] == 1 and len(antList) < allowedAntNum:
            gameDisplay.set_at((mouse[0],mouse[1]), Colors.A_black)
            pygame.display.update(pygame.Rect(mouse[0],mouse[1],1,1))

            tempAnt = Ant.Ant((mouse[0]),(mouse[1]),MenuW,0,screenW,screenH,0)
            tempAnt.ChangeStep(stepUp.GetValue(),stepDown.GetValue(),stepLeft.GetValue(),stepRight.GetValue())
            antList.append(tempAnt)
            T_AntCount.AddText(str(len(antList))+"/"+str(allowedAntNum),True)

        #Hold down right click to spawn ants
        elif not mouseOverMenu and pygame.mouse.get_pressed()[2] == 1 and Spawn and len(antList) < allowedAntNum:
            Spawn = False
            pygame.time.set_timer(spawn_Event, SpawnRate)
            gameDisplay.set_at((mouse[0],mouse[1]), Colors.A_black)
            pygame.display.update(pygame.Rect(mouse[0],mouse[1],1,1))

            tempAnt = Ant.Ant((mouse[0]),(mouse[1]),MenuW,0,screenW,screenH,0)
            tempAnt.ChangeStep(stepUp.GetValue(),stepDown.GetValue(),stepLeft.GetValue(),stepRight.GetValue())
            antList.append(tempAnt)

            T_AntCount.AddText(str(len(antList))+"/"+str(allowedAntNum),True)


        #Press 'C' to clear ants and screen
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c: clearSim()
            if event.key == pygame.K_p:
                togglePause()
                bPause.ForceUpdate(isPaused)
            if event.key == pygame.K_z:
                #print(len(antList))
                print(clock.get_fps())

    r.clear()
    if not isPaused:
        # Move every ant
        for ant in antList:
            #pix = parray[ant.x][ant.y]
            pix = gameDisplay.get_at((ant.x,ant.y))
            pix = (pix[0],pix[1],pix[2])
            if pix == Colors.black:
                # set current tile to white
                gameDisplay.set_at((ant.x,ant.y), Colors.A_white)
                # turn left and move
                ant.move_black()

            elif pix == Colors.white:
                # set current tile to white
                gameDisplay.set_at((ant.x,ant.y), Colors.A_black)
                # turn right and move
                ant.move_white()
            
            r.append(pygame.Rect(ant.x,ant.y,1,1)) # add pixel to render
    

    pygame.display.update(r)    #Update ants on screen only
    clock.tick(baseSpeed//userSpeed)    #Control the framerate of the simulation (Simulation speed)














# class StepBoxes:
#     def __init__(self, x, y, fontPath, fontSize, display, runFunction, clearFunction, updateVars):
#         """Creates an interactive clickable text box that supports number scrolling when 
#         mouse wheel is moved while hovering over the box"""
#         self.x = x
#         self.y = y
#         self.fontPath = fontPath
#         self.fontSize = fontSize
#         self.Gdisplay = display
#         self.runFunction = runFunction
#         self.clearFunction = clearFunction
#         self.updateVars = updateVars
#         self.xBox = self.x+6

#         #Text lables
#         T_Title = Text.Text("Ant Steps",self.fontPath,fontSize,Colors.A_white,self.x,self.y,self.Gdisplay,True,"bottomleft")
#         T_UpStep = Text.Text("Up :",self.fontPath,fontSize,Colors.A_white,self.x,self.y,self.Gdisplay,True,"topright")
#         T_DownStep = Text.Text("Down :",self.fontPath,fontSize,Colors.A_white,self.x,T_UpStep.GetY()+T_UpStep.GetHieght(),self.Gdisplay,True,"topright")
#         T_RightStep =Text.Text("Right :",self.fontPath,fontSize,Colors.A_white,self.x,T_DownStep.GetY()+T_DownStep.GetHieght(),self.Gdisplay,True,"topright")
#         T_LeftStep = Text.Text("Left :",self.fontPath,fontSize,Colors.A_white,self.x,T_RightStep.GetY()+T_RightStep.GetHieght(),self.Gdisplay,True,"topright")
#         self.textObjects = [T_UpStep,T_DownStep,T_RightStep,T_LeftStep,T_Title]

#         #Clickable input boxes
#         IB_UpStep = InputBox.InputBox(self.xBox, self.y, 50, fontSize,Colors.A_white,Colors.A_optionsBg,self.Gdisplay,self.fontPath,text="1",action=lambda x: self.runFunction(self.updateVars[0], x))
#         IB_DownStep = InputBox.InputBox(self.xBox, T_UpStep.GetY()+T_UpStep.GetHieght(), 50, fontSize,Colors.A_white,Colors.A_optionsBg,self.Gdisplay,self.fontPath,text="1",action=lambda x: self.runFunction(self.updateVars[1], x))
#         IB_RightStep = InputBox.InputBox(self.xBox, T_DownStep.GetY()+T_DownStep.GetHieght(), 50, fontSize,Colors.A_white,Colors.A_optionsBg,self.Gdisplay,self.fontPath,text="1",action=lambda x: self.runFunction(self.updateVars[2], x))
#         IB_LeftStep = InputBox.InputBox(self.xBox, T_RightStep.GetY()+T_RightStep.GetHieght(), 50, fontSize,Colors.A_white,Colors.A_optionsBg,self.Gdisplay,self.fontPath,text="1",action=lambda x: self.runFunction(self.updateVars[3], x))
#         self.boxObjects = [IB_UpStep,IB_DownStep,IB_RightStep,IB_LeftStep]
#         self.h = abs(IB_LeftStep.getBottomRight()[1]-IB_UpStep.getTopRight()[1])
        
#         #Reset Button
#         relX, relY = (IB_UpStep.getTopRight()[0]+2,IB_UpStep.getTopRight()[1])
#         T_reset = Text.Text("R",BNFont,20,Colors.A_black,relX,relY,self.Gdisplay)
#         B_reset = Interactive.Button(relX,relY,15,self.h, Colors.A_clearN, self.Gdisplay, T_reset, lambda: self.clearFunction(self.updateVars,self.boxObjects))

#         self.buttonObjects = [B_reset]
#         self.w = abs(max(T_UpStep.GetX(),T_DownStep.GetX(),T_RightStep.GetX(),T_LeftStep.GetX(),T_Title.GetX())-(B_reset.x+B_reset.w))






# #Classes:
# class StepBoxes:
#     def __init__(self, x, y, fontPath, fontSize, display, runFunction, clearFunction, updateVars):
#         """Creates an interactive clickable text box that supports number scrolling when 
#         mouse wheel is moved while hovering over the box"""
#         self.x = x
#         self.y = y
#         self.fontPath = fontPath
#         self.fontSize = fontSize
#         self.Gdisplay = display
#         self.runFunction = runFunction
#         self.clearFunction = clearFunction
#         self.updateVars = updateVars
#         self.xBox = self.x+6

#         #Text lables
#         T_Title = Text.Text("Ant Steps",self.fontPath,fontSize,Colors.A_white,self.x,self.y,self.Gdisplay,True,"bottomleft")
#         T_UpStep = Text.Text("Up :",self.fontPath,fontSize,Colors.A_white,self.x,self.y,self.Gdisplay,True,"topright")
#         T_DownStep = Text.Text("Down :",self.fontPath,fontSize,Colors.A_white,self.x,T_UpStep.GetY()+T_UpStep.GetHieght(),self.Gdisplay,True,"topright")
#         T_RightStep =Text.Text("Right :",self.fontPath,fontSize,Colors.A_white,self.x,T_DownStep.GetY()+T_DownStep.GetHieght(),self.Gdisplay,True,"topright")
#         T_LeftStep = Text.Text("Left :",self.fontPath,fontSize,Colors.A_white,self.x,T_RightStep.GetY()+T_RightStep.GetHieght(),self.Gdisplay,True,"topright")
#         self.textObjects = [T_UpStep,T_DownStep,T_RightStep,T_LeftStep,T_Title]

#         #Clickable input boxes
#         T_upstep = Text.Text("1",BNFont,20,Colors.A_white,self.xBox, self.y,self.Gdisplay)
#         IB_UpStep = InputBox.InputBox(self.xBox, self.y, 50, fontSize, Colors.A_white,Colors.A_optionsBg,self.Gdisplay,T_upstep,action=lambda x: self.runFunction(self.updateVars[0], x))
#         # IB_DownStep = InputBox.InputBox(self.xBox, T_UpStep.GetY()+T_UpStep.GetHieght(), 50, fontSize,Colors.A_white,Colors.A_optionsBg,self.Gdisplay,self.fontPath,text="1",action=lambda x: self.runFunction(self.updateVars[1], x))
#         # IB_RightStep = InputBox.InputBox(self.xBox, T_DownStep.GetY()+T_DownStep.GetHieght(), 50, fontSize,Colors.A_white,Colors.A_optionsBg,self.Gdisplay,self.fontPath,text="1",action=lambda x: self.runFunction(self.updateVars[2], x))
#         # IB_LeftStep = InputBox.InputBox(self.xBox, T_RightStep.GetY()+T_RightStep.GetHieght(), 50, fontSize,Colors.A_white,Colors.A_optionsBg,self.Gdisplay,self.fontPath,text="1",action=lambda x: self.runFunction(self.updateVars[3], x))
#         self.boxObjects = [IB_UpStep] #,IB_DownStep,IB_RightStep,IB_LeftStep]
#         # self.h = abs(IB_LeftStep.getBottomRight()[1]-IB_UpStep.getTopRight()[1])
        
#         #Reset Button
#         relX, relY = (IB_UpStep.getTopRight()[0]+2,IB_UpStep.getTopRight()[1])
#         T_reset = Text.Text("R",BNFont,20,Colors.A_black,relX,relY,self.Gdisplay)
#         # B_reset = Interactive.Button(relX,relY,15,self.h, Colors.A_clearN, self.Gdisplay, T_reset, lambda: self.clearFunction(self.updateVars,self.boxObjects))

#         self.buttonObjects = []#B_reset]
#         # self.w = abs(max(T_UpStep.GetX(),T_DownStep.GetX(),T_RightStep.GetX(),T_LeftStep.GetX(),T_Title.GetX())-(B_reset.x+B_reset.w))



























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