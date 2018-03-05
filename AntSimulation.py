
import pygame
import time


"""
ToDo List:
-Multiply and scale the ant step boxes




"""

#Custom
import Ant
import Colors
import Button
import ButtonToggle
import CustomPath
import Text
import AntStepVar
import InputBox


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

#Simulation speed vars
startMultipler = 512     #Must be a number 2^
baseSpeed = 10000
userSpeed = 1
isPaused = False

#Ant step vars
stepUp = AntStepVar.AntStepVar(0,screenH,1)



def text_objects(text, font):
    textSurf = font.render(text,True,Colors.black)
    return textSurf, textSurf.get_rect()

def AddText():
    smallText = pygame.font.Font(CustomPath.Path("assets\BebasNeue-Regular.ttf"),20)
    TextSurf, TextRect = text_objects(self.msg, smallText)
    TextRect.center = ((self.x+(self.w/2)),(self.y+(self.h/2)))
    self.gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update(pygame.Rect(self.x, self.y, self.w, self.h))




#TextBoxes
T_Watermark = Text.Text("By: MrJohnWeez",CustomPath.Path("assets\BebasNeue-Regular.ttf"),16,Colors.white,1,screenH+3,gameDisplay,True,"bottomleft")
T_AntCount = Text.Text("0/"+str(allowedAntNum),CustomPath.Path("assets\BebasNeue-Regular.ttf"),20,Colors.white,1,screenH+3-16,gameDisplay,True,"bottomleft")
T_AntStepUp = Text.Text("1",CustomPath.Path("assets\BebasNeue-Regular.ttf"),20,Colors.white,1+25,screenH+3-16-50,gameDisplay,True,"bottomleft")

texts = [T_Watermark,T_AntCount,T_AntStepUp]


#Button Functions
def togglePause():
    global isPaused
    isPaused = not isPaused

    if isPaused:
        bPause.ChangeMsg("Play")
    else:
        bPause.ChangeMsg("Pause")


def clearSim():
    antList.clear()
    gameDisplay.fill(Colors.white)
    pygame.display.update(pygame.Rect(MenuW,0,screenW,screenH))
    T_AntCount.ForceUpdate(str(len(antList))+"/"+str(allowedAntNum),Colors.optionsBg)


def speedButton():
    global userSpeed
    global startMultipler

    if userSpeed < startMultipler:
        userSpeed = int(userSpeed*2)
    else:
        userSpeed = 1

    global b3
    bSpeed.ChangeMsg("x"+str(startMultipler//userSpeed))
    print("Speed: ", startMultipler//userSpeed)






#Define Buttons
bClear = Button.Button("Clear", MenuX,MenuY,100,50, Colors.clearN, gameDisplay, clearSim)
bPause = ButtonToggle.ButtonToggle("Pause",  MenuX,MenuY+60,100,50, Colors.clearN, gameDisplay, togglePause)
bSpeed = Button.Button("x"+str(startMultipler//userSpeed), MenuX,MenuY+120,100,50, Colors.clearN, gameDisplay, speedButton)



buttons = [bClear,bPause,bSpeed]

def UpdateStepVar(var, textBox):
    var.UpdateByString(textBox.getText())
    textBox.updateText(str(var.GetValue()))


input_box1 = InputBox.InputBox(1, 300, 50, 25,pygame.Color(255,255,255),pygame.Color(48,48,48),gameDisplay,CustomPath.Path("assets\BebasNeue-Regular.ttf"),text="1",action=lambda x: UpdateStepVar(stepUp, x))
input_boxes = [input_box1]

#Simulation Functions
def QuitSim():
    pygame.quit()
    quit()

def ResetSim():
    gameDisplay.fill(Colors.white)
    pygame.draw.rect(gameDisplay, Colors.optionsBg, (0,0,MenuW,MenuH))

    #Reset buttons
    global buttons
    for button in buttons:
        button.DrawButton()
    input_box1.update()

    pygame.display.update()
    antList.clear()

    for text in texts:
        text.ForceUpdate()


#Set up Simulation
ResetSim()


#Main loop
while True:
    #Check for Button interaction
    mouse = pygame.mouse.get_pos()
    mouseOverMenu = MenuX+MenuW > mouse[0] > MenuX and MenuY+MenuH > mouse[1] > MenuY
    if mouseOverMenu:
        for button in buttons:
            button.Update(mouse[0],mouse[1])

    for event in pygame.event.get():
        for box in input_boxes:
            box.handle_event(event)

        #Quit Game
        if event.type == pygame.QUIT: QuitSim()
            
        #Timer for spawn rate
        elif event.type == spawn_Event:
            Spawn = True
            pygame.time.set_timer(spawn_Event, 0)
        
        #Left Click Spwn an ant
        elif not mouseOverMenu and event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] == 1 and len(antList) < allowedAntNum:
            gameDisplay.set_at((mouse[0],mouse[1]), Colors.black)
            pygame.display.update(pygame.Rect(mouse[0],mouse[1],1,1))

            tempAnt = Ant.Ant((mouse[0]),(mouse[1]),MenuW,0,screenW,screenH,0)
            tempAnt.ChangeStep(stepUp.GetValue(),stepUp.GetValue(),stepUp.GetValue(),stepUp.GetValue())
            antList.append(tempAnt)
            T_AntCount.ForceUpdate(str(len(antList))+"/"+str(allowedAntNum),Colors.optionsBg)

        #Hold down right click to spawn ants
        elif not mouseOverMenu and pygame.mouse.get_pressed()[2] == 1 and Spawn and len(antList) < allowedAntNum:
            Spawn = False
            pygame.time.set_timer(spawn_Event, SpawnRate)
            gameDisplay.set_at((mouse[0],mouse[1]), Colors.black)
            pygame.display.update(pygame.Rect(mouse[0],mouse[1],1,1))

            tempAnt = Ant.Ant((mouse[0]),(mouse[1]),MenuW,0,screenW,screenH,0)
            tempAnt.ChangeStep(stepUp.GetValue(),stepUp.GetValue(),stepUp.GetValue(),stepUp.GetValue())
            antList.append(tempAnt)

            T_AntCount.ForceUpdate(str(len(antList))+"/"+str(allowedAntNum),Colors.optionsBg)


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
                gameDisplay.set_at((ant.x,ant.y), Colors.white)
                # turn left and move
                ant.move_black()

            elif pix == Colors.white:
                # set current tile to white
                gameDisplay.set_at((ant.x,ant.y), Colors.black)
                # turn right and move
                ant.move_white()
            
            r.append(pygame.Rect(ant.x,ant.y,1,1)) # add pixel to render
    

    pygame.display.update(r)    #Update ants on screen only
    clock.tick(baseSpeed//userSpeed)    #Control the framerate of the simulation (Simulation speed)




























"""
Other:

#b_LUp = Button.Button("<", 1,screenH+3-16-75,15,25, Colors.clearN, gameDisplay, lambda : AntStep(stepUp, T_AntStepUp, False))
#b_RUp = Button.Button(">", 1+75,screenH+3-16-75,15,25, Colors.clearN, gameDisplay, lambda : AntStep(stepUp, T_AntStepUp, True))

# def AntStep(var, textVar, shouldIncrease, stepValue=1):
#     var.UpdateValue(shouldIncrease,stepValue)
#     textVar.ForceUpdate(str(var.GetValue()),Colors.optionsBg)

"""