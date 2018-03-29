
import pygame
import Colors

class ImageType:
    def __init__(self,path,display,xScale=1, yScale=1):
        self.image = pygame.image.load(path)
        self.display = display
        self.imgRect = self.image.get_rect()
        self.currScale = (xScale,yScale)
        self.Scale(xScale, yScale)

    def Draw(self,pos):
        self.display.blit(self.image, (pos[0]-self.imgRect.w//2,pos[1]-self.imgRect.h//2))
        pygame.display.update(pygame.Rect(pos[0]-self.imgRect.w//2,pos[1]-self.imgRect.h//2,self.imgRect.w,self.imgRect.h))

    def Scale(self, xScale=1, yScale=1):
        r = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (int(r.w*xScale),int(r.h*yScale)))
        self.currScale = (xScale,yScale)
        self.imgRect = self.image.get_rect()

    def AutoScale(self, width, height, xOffSet=0, yOffSet=0, keepAspect=True):
        if keepAspect:
            if width > height:
                offSetx = 1+xOffSet
                offSety = 1+yOffSet
                self.Scale(width/(self.imgRect.w*offSetx),width/(self.imgRect.w*offSetx))
            else:
                self.Scale(height/(self.imgRect.h*offSety),(height/self.imgRect.h*offSety))
        else:
            self.Scale(width/(self.imgRect.w*offSetx),height/(self.imgRect.h*offSety))


    def getH(self):
        return self.imgRect.h
    def getW(self):
        return self.imgRect.w
    def getX(self):
        return self.imgRect.x
    def getY(self):
        return self.imgRect.y
    def getScale(self):
        return self.currScale