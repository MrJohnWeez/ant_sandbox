import pygame

import CustomPath
import Colors

class ButtonToggle:
    def __init__(self, x, y, w, h, normalColor, display, textObject, action=None):
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
        self.textObject = textObject
        self.prevClick = -1
        
    def ChangeMsg(self,newMsg):
        """ Changes the text over the button """
        self.textObject.AddText(newMsg)
        if self.toggled:
            self.ToggleOn(True)
        else:
            self.ToggleOff(True)

    def ToggleOn(self, ignoreFunction=False):
        self.state = 1
        self.toggled = True
        self.UpdateToScreen(self.clickColor)
        if self.action != None and not ignoreFunction:
            self.action()

    def ToggleOff(self, ignoreFunction=False):
        self.toggled = False
        self.state = 0
        self.UpdateToScreen(self.normalColor)
        if self.action != None and not ignoreFunction:
            self.action()
        

    #Adds text to a button
    def UpdateToScreen(self, buttonColor):
        """Draw button on screen"""
        #Update the text object and update the whole button on the game screen
        pygame.draw.rect(self.gameDisplay, buttonColor, (self.x,self.y,self.w,self.h))
        self.textObject.TextRect.center = ((self.x+(self.w/2)),(self.y+(self.h/2)))
        self.textObject.ForceBlit()
        pygame.display.update(pygame.Rect(self.x, self.y, self.w, self.h))

    def Update(self):
        #If not hovered
        mouse = pygame.mouse.get_pos()
        mouseOver = self.x+self.w > mouse[0] > self.x and self.y+self.h > mouse[1] > self.y
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

    def ForceUpdate(self, ToggleOn):
        if ToggleOn:
            self.ToggleOn(True)
        else:
            self.ToggleOff(True)
            

    #Draws initual button state
    def DrawButton(self):
        self.ToggleOff(True)

    

    