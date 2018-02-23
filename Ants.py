
import pygame
import os
import time
import random
import sys

#Custom
import Ant
import Colors

if getattr(sys, 'frozen', False):
    # frozen
    script_dir = os.path.dirname(sys.executable)
else:
    # unfrozen
    script_dir = os.path.dirname(os.path.realpath(__file__))

def Path(localPath):
    return os.path.join(script_dir, localPath)



screenH = 600
screenW = 800
MenuX = 0
MenuY = 0
MenuW = (screenW//4)
MenuH = screenH


pygame.init()
gameDisplay = pygame.display.set_mode((screenW,screenH))
# tempRect = gameDisplay.get_rect()
# antDisplay = pygame.Rect(MenuW,MenuY,MenuW*3,MenuH)
parray = pygame.PixelArray(gameDisplay)
coolDown = 0

#Custom Event Handling
Spawn = True
SpawnRate = 1
spawn_Event  = pygame.USEREVENT + 1

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

def button(msg, x, y, w, h, inactive, active, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, active, (x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, inactive, (x,y,w,h))

    smallText = pygame.font.Font(Path("assets\BebasNeue-Regular.ttf"),20)
    TextSurf, TextRect = text_objects(msg, smallText)
    TextRect.center = ((x+(w/2)),(y+(h/2)))
    gameDisplay.blit(TextSurf, TextRect)





ResetSim()
isPaused = False
while True:
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
            parray[mouse[0]][mouse[1]] = Colors.black
            antList.append(Ant.Ant((mouse[0]),(mouse[1]),MenuW,0,screenW,screenH,0))

        #Hold down right click to spawn ants
        elif pygame.mouse.get_pressed()[2] == 1 and Spawn:
            Spawn = False
            pygame.time.set_timer(spawn_Event, SpawnRate)

            mouse = pygame.mouse.get_pos()
            parray[mouse[0]][mouse[1]] = Colors.white
            antList.append(Ant.Ant((mouse[0]),(mouse[1]),MenuW,0,screenW,screenH,0))


        #Press 'C' to clear ants and screen
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                antList.clear()
                gameDisplay.fill(Colors.white)
                
                pygame.display.update(pygame.Rect(MenuW,0,screenW,screenH))
            if event.key == pygame.K_p:
                isPaused = not isPaused
            if event.key == pygame.K_z:
                print(len(antList))

    #Buttons
    # button("Clear", MenuX,MenuY,100,50, Colors.clearN, Colors.clearA)





    r = [] #Pixels to render list
    if not isPaused:
        # Move every ant
        for ant in antList:
            pix = parray[ant.x][ant.y]
            if Colors.toColor(pix) == Colors.black:
                # set current tile to white
                parray[ant.x][ant.y] = Colors.white
                # turn left and move
                ant.move_black()

            elif Colors.toColor(pix) == Colors.white:
                # set current tile to white
                parray[ant.x][ant.y] = Colors.black
                # turn right and move
                ant.move_white()
            
            r.append(pygame.Rect(ant.x,ant.y,1,1)) # add pixel to render

    pygame.display.update(r)