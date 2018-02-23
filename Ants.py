
import pygame
import os
import time
import random

#Custom
import Ant
import Colors

screenH = 600
screenW = 600

gameDisplay = pygame.display.set_mode((screenW,screenH))
gameDisplay.fill(Colors.white)
pygame.display.update()

parray = pygame.PixelArray(gameDisplay)

#Custom Event Handling
Spawn = True
SpawnRate = 1
spawn_Event  = pygame.USEREVENT + 1

antList = []
coolDown = 0

def QuitSim():
    pygame.quit()
    quit()

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
            antList.append(Ant.Ant((mouse[0]),(mouse[1]),screenW,screenH,0))

        #Hold down right click to spawn ants
        elif pygame.mouse.get_pressed()[2] == 1 and Spawn:
            Spawn = False
            pygame.time.set_timer(spawn_Event, SpawnRate)

            mouse = pygame.mouse.get_pos()
            parray[mouse[0]][mouse[1]] = Colors.white
            antList.append(Ant.Ant((mouse[0]),(mouse[1]),screenW,screenH,0))


        #Press 'C' to clear ants and screen
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                antList.clear()
                gameDisplay.fill(Colors.white)
                pygame.display.update()
            if event.key == pygame.K_p:
                isPaused = not isPaused
            if event.key == pygame.K_z:
                print(len(antList))


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