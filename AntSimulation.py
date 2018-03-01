
import pygame
import time

#Custom
import Ant
import Colors
import Button
import ButtonToggle
import CustomPath
import Text


#Define Screen
screenH = 600
screenW = 800
MenuX = 0
MenuY = 0
MenuW = (screenW//4)
MenuH = screenH

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

startMultipler = 512     #Must be a number 2^
baseSpeed = 10000
userSpeed = 1


isPaused = False



def text_objects(text, font):
    textSurf = font.render(text,True,Colors.black)
    return textSurf, textSurf.get_rect()

def AddText():
    smallText = pygame.font.Font(CustomPath.Path("assets\BebasNeue-Regular.ttf"),20)
    TextSurf, TextRect = text_objects(self.msg, smallText)
    TextRect.center = ((self.x+(self.w/2)),(self.y+(self.h/2)))
    self.gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update(pygame.Rect(self.x, self.y, self.w, self.h))




#Button Functions
def togglePause():
    global isPaused
    isPaused = not isPaused

    print("Is Game Pause: ", isPaused)
    if isPaused:
        bPause.ChangeMsg("Play")
    else:
        bPause.ChangeMsg("Pause")


def clearSim():
    antList.clear()
    gameDisplay.fill(Colors.white)
    pygame.display.update(pygame.Rect(MenuW,0,screenW,screenH))


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






#Simulation Functions
def QuitSim():
    pygame.quit()
    quit()

def ResetSim():
    gameDisplay.fill(Colors.white)
    pygame.draw.rect(gameDisplay, Colors.optionsBg, (0,0,MenuW,MenuH))
    global buttons
    for button in buttons:
        button.DrawButton()
    pygame.display.update()
    antList.clear()




#Set up Simulation
ResetSim()
Text.Text("By: MrJohnWeez",CustomPath.Path("assets\BebasNeue-Regular.ttf"),16,Colors.white,1,screenH+3,gameDisplay,True,"bottomleft")
Text.Text("0/500",CustomPath.Path("assets\BebasNeue-Regular.ttf"),20,Colors.white,1,screenH+3-16,gameDisplay,True,"bottomleft")

#Main loop
while True:
    #Check for Button interaction
    mouse = pygame.mouse.get_pos()
    mouseOverMenu = MenuX+MenuW > mouse[0] > MenuX and MenuY+MenuH > mouse[1] > MenuY
    if mouseOverMenu:
        for button in buttons:
            button.Update(mouse[0],mouse[1])

    
    
    for event in pygame.event.get():
        
        #Quit Game
        if event.type == pygame.QUIT: QuitSim()
            
        #Timer for spawn rate
        elif event.type == spawn_Event:
            Spawn = True
            pygame.time.set_timer(spawn_Event, 0)
        
        #Left Click Spwn an ant
        elif not mouseOverMenu and event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] == 1:
            mouse = pygame.mouse.get_pos()
            gameDisplay.set_at((mouse[0],mouse[1]), Colors.black)
            pygame.display.update(pygame.Rect(mouse[0],mouse[1],1,1))

            tempAnt = Ant.Ant((mouse[0]),(mouse[1]),MenuW,0,screenW,screenH,0)
            tempAnt.ChangeStep(1,1,1,1)
            antList.append(tempAnt)

        #Hold down right click to spawn ants
        elif not mouseOverMenu and pygame.mouse.get_pressed()[2] == 1 and Spawn:
            Spawn = False
            pygame.time.set_timer(spawn_Event, SpawnRate)

            mouse = pygame.mouse.get_pos()
            gameDisplay.set_at((mouse[0],mouse[1]), Colors.white)
            antList.append(Ant.Ant((mouse[0]),(mouse[1]),MenuW,0,screenW,screenH,0))


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
    

    pygame.display.update(r)
    clock.tick(baseSpeed//userSpeed)