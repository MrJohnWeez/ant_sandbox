
import pygame
import Colors
import CustomPath
class ImageType:
    """Creates an image that can be moved around on the pygame screen"""
    def __init__(self,path,display,xScale=1, yScale=1):
        self.image = pygame.image.load(path)
        self.display = display
        self.imgRect = self.image.get_rect()
        self.currScale = (xScale,yScale)
        self.Scale(xScale, yScale)

    def Draw(self,pos):
        """Draw image to screen and update it"""
        self.display.blit(self.image, (pos[0]-self.imgRect.w//2,pos[1]-self.imgRect.h//2))
        pygame.display.update(pygame.Rect(pos[0]-self.imgRect.w//2,pos[1]-self.imgRect.h//2,self.imgRect.w,self.imgRect.h))

    def Scale(self, xScale=1, yScale=1):
        """Scale the image in the x and y aspect"""
        r = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (int(r.w*xScale),int(r.h*yScale)))
        self.currScale = (xScale,yScale)
        self.imgRect = self.image.get_rect()

    def AutoScale(self, width, height, xOffSet=0, yOffSet=0, keepAspect=True):
        """Scale the image to the width and height constrients"""
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
        """Return height"""
        return self.imgRect.h
    def getW(self):
        """Return width"""
        return self.imgRect.w
    def getX(self):
        """Return x cord"""
        return self.imgRect.x
    def getY(self):
        """Return y cord"""
        return self.imgRect.y
    def getScale(self):
        """Returns the scale of the image class"""
        return self.currScale



####################################################################################################################################################################
####################################################################################################################################################################
####################################################################################################################################################################
####################################################################################################################################################################

#Loading Buttons

AspectLong = 480/110
AspectShort = 242/107
AspectMini = 154/104

buttonFolder = "assets\Buttons\\"
buttonFolderArray = [buttonFolder]*3
buttonPrefix = ["BN","BL","BD"]

buttonPath = [buttonFolderArray[i] + buttonPrefix[i] for i in range(len(buttonFolderArray))]

def CreateButtonArray(buttonName):
    finalPaths = [buttonPath[i] + buttonName for i in range(len(buttonPath))]
    return [CustomPath.Path(finalPaths[1]),CustomPath.Path(finalPaths[0]),CustomPath.Path(finalPaths[2])]


#Image paths for button images
#Long
IBLongBlue = CreateButtonArray("LongBlue.png")
IBLongRed = CreateButtonArray("LongRed.png")
IBLongRedFade = CreateButtonArray("LongRedFade.png")
IBLongYellow = CreateButtonArray("LongYellow.png")
#Short
IBShortRed = CreateButtonArray("ShortRed.png")
IBShortBlue = CreateButtonArray("ShortBlue.png")
IBShortLightGreen = CreateButtonArray("ShortLightGreen.png")
IBShortGray = CreateButtonArray("ShortGray.png")
IBShortWhite = CreateButtonArray("ShortWhite.png")
IBShortDarkBlue = CreateButtonArray("ShortDarkBlue.png")
IBShortLightBrown = CreateButtonArray("ShortLightBrown.png")
IBShortLava = CreateButtonArray("ShortLava.png")
IBShortGreen = CreateButtonArray("ShortGreen.png")
IBShortPurple = CreateButtonArray("ShortPurple.png")
IBShortYellow = CreateButtonArray("ShortYellow.png")

