import pygame

import CustomPath
import Colors

class Button:
    def __init__(self, x, y, w, h, normalColor, display, textObject, action=None):
        """Creates a button object that can be clicked"""
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.state = 1
        self.gameDisplay = display
        self.action = action
        self.textObject = textObject

        self.normalColor = normalColor
        self.clickColor = Colors.shadeAlpha(normalColor, 0.2)
        self.hoverColor = Colors.shadeAlpha(normalColor, -0.2)
        
    def ChangeMsg(self,newMsg):
        """ Changes the text over the button """
        self.textObject.AddText(newMsg)

    #Adds text to a button
    def UpdateToScreen(self, buttonColor):
        """Draw button on screen"""
        #Update the text object and update the whole button on the game screen
        pygame.draw.rect(self.gameDisplay, buttonColor, (self.x,self.y,self.w,self.h))
        self.textObject.TextRect.center = ((self.x+(self.w/2)),(self.y+(self.h/2)))
        self.textObject.ForceBlit()
        pygame.display.update(pygame.Rect(self.x, self.y, self.w, self.h))

    def Update(self, newMsg=None):
        """Update if user has interacted with button"""
        mouse = pygame.mouse.get_pos()
        #If not hovered
        moveOver = self.x+self.w > mouse[0] > self.x and self.y+self.h > mouse[1] > self.y

        #If message has changed
        if newMsg != None: self.textObject.AddText(newMsg)

        if moveOver and self.state == 0:
            #Mouse is over button change the color state
            self.state = 1
            self.UpdateToScreen(self.hoverColor)
            
        elif not moveOver and (self.state == 1 or self.state == 2):
            #Mouse no longer over button change color state to normal
            self.state = 0
            self.UpdateToScreen(self.normalColor)

        elif moveOver and self.state == 1:
            #Mouse is over button and it is ready to be clicked
            click = pygame.mouse.get_pressed()
            if click[0] == 1 and self.action != None:
                self.state = 2
                self.UpdateToScreen(self.clickColor)
                self.action()

        elif self.state == 2 and pygame.mouse.get_pressed()[0] == 0:
            #Mouse has stopped holding down click so turn button to normal color
            self.UpdateToScreen(self.normalColor)
            self.state = 0


    #Draws initual button state
    def DrawButton(self):
        """ Draws button on command"""
        self.Update()
    

    