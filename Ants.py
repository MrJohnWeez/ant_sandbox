
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




antList = []
coolDown = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] == 1:
            mouse = pygame.mouse.get_pos()
            parray[mouse[0]][mouse[1]] = Colors.black
            antList.append(Ant.Ant((mouse[0]),(mouse[1]),screenW,screenH,0))
        elif pygame.mouse.get_pressed()[2] == 1:
            mouse = pygame.mouse.get_pos()
            parray[mouse[0]][mouse[1]] = Colors.white
            antList.append(Ant.Ant((mouse[0]),(mouse[1]),screenW,screenH,0))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                antList.clear()
                gameDisplay.fill(Colors.white)
                pygame.display.update()

    r = [] #Pixels to render list

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















































    
# import pygame
# import os
# import time
# import random

# white = (255,255,255)
# black = (0,0,0)
# red = (255,0,0)
# green = (0,255,0)
# blue = (0,0,255)

# screenH = 200
# screenW = 200

# gameDisplay = pygame.display.set_mode((screenW,screenH))
# gameDisplay.fill(white)

# parray = pygame.PixelArray(gameDisplay)

# parray[screenW//2][screenH//2] = black
# class Ant:
#     def __init__(self, inx=0, iny=0, infacing=0, inboundx=-1, inboundy=-1):
#         self.x = inx
#         self.y = iny
#         self.facing = infacing # 0 = up, 1 = right, 2 = down, 3 = left
#         self.boundx = inboundx
#         self.boundy = inboundy

#     def get_x(self):
#         return self.__x

#     def set_x(self, x):
#         self.__x = x

#     def get_y(self):
#         return self.__x

#     def set_y(self, y):
#         self.__y = y

#     def move_black():
#         if direction == 0:
#             direction = 3
#             antx -= 1
#         elif direction == 1:
#             direction = 0
#             anty -= 1
#         elif direction == 2:
#             direction = 1
#             antx += 1
#         elif direction == 3:
#             direction = 2
#             anty += 1

#     def move_white():
#         if direction == 0:
#             direction = 1
#             antx += 1
#         elif direction == 1:
#             direction = 2
#             anty += 1
#         elif direction == 2:
#             direction = 3
#             antx -= 1
#         elif direction == 3:
#             direction = 0
#             anty -= 1
        
# def toColor(in_Color):
#     return (in_Color//(256*256), in_Color//256%256, in_Color%256)

# direction = 0 # 0 = up, 1 = right, 2 = down, 3 = left

# ant1 = Ant(screenW//2,screenH//2,screenW,screenH)

# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             quit()

#     #print("Ant: ", antx, "   ", anty)
#     pix = parray[ant1.x][ant1.y]
#     if toColor(pix) == black:
#         # set current tile to white
#         parray[antx][anty] = white
#         # turn left and move
#         if direction == 0:
#             direction = 3
#             antx -= 1
#         elif direction == 1:
#             direction = 0
#             anty -= 1
#         elif direction == 2:
#             direction = 1
#             antx += 1
#         elif direction == 3:
#             direction = 2
#             anty += 1

#     elif toColor(pix) == white:
#         # set current tile to white
#         parray[antx][anty] = black
#         # turn left and move
#         if direction == 0:
#             direction = 1
#             antx += 1
#         elif direction == 1:
#             direction = 2
#             anty += 1
#         elif direction == 2:
#             direction = 3
#             antx -= 1
#         elif direction == 3:
#             direction = 0
#             anty -= 1

#     if(antx > screenW-1):
#         antx = 0
#     if(antx < 0):
#         antx = screenW-1
#     if(anty > screenH-1):
#         anty = 0
#     if(anty < 0):
#         anty = screenH-1


#     pygame.display.update()