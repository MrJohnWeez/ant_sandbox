
import pygame

#Custom
import Ant
import Colors
import Button
import CustomPath

#Define Screen
screenH = 600
screenW = 800
MenuX = 0
MenuY = 0
MenuW = (screenW//4)
MenuH = screenH

pygame.init()
gameDisplay = pygame.display.set_mode((screenW,screenH))


#Custom Event Handling
Spawn = True
SpawnRate = 1
spawn_Event  = pygame.USEREVENT + 1
coolDown = 0

antList = []

def QuitSim():
    pygame.quit()
    quit()

def ResetSim():
    gameDisplay.fill(Colors.white)
    pygame.draw.rect(gameDisplay, Colors.optionsBg, (0,0,MenuW,MenuH))
    pygame.display.update()
    antList.clear()

def text_objects(text, font):
    textSurf = font.render(text,True,Colors.black)
    return textSurf, textSurf.get_rect()


ResetSim()
r = [] #Pixels to render list
isPaused = False


def clearSim():
    antList.clear()
    gameDisplay.fill(Colors.white)
    pygame.display.update(pygame.Rect(MenuW,0,screenW,screenH))


#Define Buttons
b1 = Button.Button("Clear", MenuX,MenuY,100,50, Colors.clearN, gameDisplay, clearSim)

buttons = [b1]
for button in buttons:
    button.DrawButton()


#Main Simulation loop
while True:
    mouse = pygame.mouse.get_pos()
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
        elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] == 1:
            mouse = pygame.mouse.get_pos()
            gameDisplay.set_at((mouse[0],mouse[1]), Colors.black)
            antList.append(Ant.Ant((mouse[0]),(mouse[1]),MenuW,0,screenW,screenH,0))

        #Hold down right click to spawn ants
        elif pygame.mouse.get_pressed()[2] == 1 and Spawn:
            Spawn = False
            pygame.time.set_timer(spawn_Event, SpawnRate)

            mouse = pygame.mouse.get_pos()
            gameDisplay.set_at((mouse[0],mouse[1]), Colors.white)
            antList.append(Ant.Ant((mouse[0]),(mouse[1]),MenuW,0,screenW,screenH,0))


        #Press 'C' to clear ants and screen
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c: clearSim()
            if event.key == pygame.K_p: isPaused = not isPaused
            if event.key == pygame.K_z: print(len(antList))

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