import pygame
import CustomPath



pygame.init()
screen=pygame.display.set_mode((500,500),pygame.RESIZABLE)
pic=pygame.image.load(CustomPath.Path("assets\AntSimMenuBackground.jpg")) #You need an example picture in the same folder as this file!

screen.blit(pygame.transform.scale(pic,(500,500)),(0,0))
pygame.display.flip()
while True:
    pygame.event.pump() #Not nesisary
    event=pygame.event.wait()
    if event.type==pygame.QUIT: pygame.display.quit()
    elif event.type==pygame.VIDEORESIZE:
        newWidth, newHeight = event.dict['size']
        if newWidth < 600:
            newWidth = 600
        if newHeight < 600:
            newHeight = 600
        
        screen=pygame.display.set_mode((newWidth,newHeight),pygame.RESIZABLE)
        screen.blit(pygame.transform.scale(pic,(newWidth,newHeight)),(0,0))
        pygame.display.flip()