import pygame

import CustomPath
import Colors

def text_objects(text, font):
    textSurf = font.render(text,True,Colors.black)
    return textSurf, textSurf.get_rect()


class Button:
    def __init__(self, msg, x, y, w, h, normalColor, display, action=None):
        self.msg = msg
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.state = 1
        self.gameDisplay = display
        self.action = action

        self.normalColor = normalColor
        self.clickColor = Colors.shade(normalColor, 0.2)
        self.hoverColor = Colors.shade(normalColor, -0.2)
        
    def ChangeMsg(self,newMsg):
        self.msg = newMsg

    #Adds text to a button
    def AddText(self):
        smallText = pygame.font.Font(CustomPath.Path("assets\BebasNeue-Regular.ttf"),20)
        TextSurf, TextRect = text_objects(self.msg, smallText)
        TextRect.center = ((self.x+(self.w/2)),(self.y+(self.h/2)))
        self.gameDisplay.blit(TextSurf, TextRect)
        pygame.display.update(pygame.Rect(self.x, self.y, self.w, self.h))

    def Update(self, mouseX, mouseY, newMsg=None):
        #If not hovered
        moveOver = self.x+self.w > mouseX > self.x and self.y+self.h > mouseY > self.y
        if newMsg != None:
            self.msg = newMsg

        if moveOver and self.state == 0:
            self.state = 1
            pygame.draw.rect(self.gameDisplay, self.hoverColor, (self.x,self.y,self.w,self.h))
            self.AddText()
            
        elif not moveOver and (self.state == 1 or self.state == 2):
            self.state = 0
            pygame.draw.rect(self.gameDisplay, self.normalColor, (self.x,self.y,self.w,self.h))
            self.AddText()

        elif moveOver and self.state == 1:
            click = pygame.mouse.get_pressed()
            if click[0] == 1 and self.action != None:
                
                self.state = 2
                pygame.draw.rect(self.gameDisplay, self.clickColor, (self.x,self.y,self.w,self.h))
                self.AddText()
                self.action()

        elif self.state == 2 and pygame.mouse.get_pressed()[0] == 0:
            pygame.draw.rect(self.gameDisplay, self.normalColor, (self.x,self.y,self.w,self.h))
            self.AddText()
            self.state = 0


    #Draws initual button state
    def DrawButton(self):
        mouse = pygame.mouse.get_pos()
        self.Update(mouse[0],mouse[1])
        self.AddText()

    

    