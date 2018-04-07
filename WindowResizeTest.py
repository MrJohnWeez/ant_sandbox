import pygame
import CustomPath


from pygame.locals import *
pygame.init()
screen=pygame.display.set_mode((500,500),RESIZABLE)
pic=pygame.image.load(CustomPath.Path("assets\AntSimMenuBackground.jpg")) #You need an example picture in the same folder as this file!

screen.blit(pygame.transform.scale(pic,(500,500)),(0,0))
pygame.display.flip()
while True:
    pygame.event.pump() #Not nesisary
    event=pygame.event.wait()
    if event.type==QUIT: pygame.display.quit()
    elif event.type==VIDEORESIZE:
        newWidth, newHeight = event.dict['size']
        if newWidth < 600:
            newWidth = 600
        if newHeight < 600:
            newHeight = 600
        
        screen=pygame.display.set_mode((newWidth,newHeight),RESIZABLE)
        screen.blit(pygame.transform.scale(pic,(newWidth,newHeight)),(0,0))
        pygame.display.flip()