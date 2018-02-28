import pygame

import CustomPath
import Colors

def text_objects(text, font):
    textSurf = font.render(text,True,Colors.black)
    return textSurf, textSurf.get_rect()


class ButtonToggle:
    def __init__(self, msg, x, y, w, h, normalColor, display, action=None):
        self.msg = msg
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.gameDisplay = display
        self.action = action
        self.state = 0
        self.toggled = False

        self.normalColor = normalColor
        self.clickColor = Colors.shade(normalColor, 0.2)
        self.hoverColor = Colors.shade(normalColor, -0.2)

        self.prevClick = -1
        
    def ToggleOn(self):
        self.state = 1
        self.toggled = True
        pygame.draw.rect(self.gameDisplay, self.clickColor, (self.x,self.y,self.w,self.h))
        self.AddText()
        if self.action != None:
            self.action()

    def ToggleOff(self, ignoreFunction=False):
        self.toggled = False
        self.state = 0
        pygame.draw.rect(self.gameDisplay, self.normalColor, (self.x,self.y,self.w,self.h))
        self.AddText()
        if self.action != None and not ignoreFunction:
            self.action()

    #Adds text to a button
    def AddText(self):
        smallText = pygame.font.Font(CustomPath.Path("assets\BebasNeue-Regular.ttf"),20)
        TextSurf, TextRect = text_objects(self.msg, smallText)
        TextRect.center = ((self.x+(self.w/2)),(self.y+(self.h/2)))
        self.gameDisplay.blit(TextSurf, TextRect)
        pygame.display.update(pygame.Rect(self.x, self.y, self.w, self.h))

    def Update(self, mouseX, mouseY):
        #If not hovered
        
        mouseOver = self.x+self.w > mouseX > self.x and self.y+self.h > mouseY > self.y
        if mouseOver: 
            click = pygame.mouse.get_pressed()
            if self.prevClick == 1 and click[0] == 0:
                if not self.toggled:
                    self.ToggleOn()
                else:
                    self.ToggleOff()
            self.prevClick = click[0]
        else:
            self.prevClick = -1


    #Draws initual button state
    def DrawButton(self):
        self.ToggleOff(True)

    

    