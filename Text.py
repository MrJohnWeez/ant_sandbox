import pygame
import Colors

class Text:
    def __init__(self, text, font, size, color, x, y, display, shouldUpdate=False, pos='topleft'):
        self.text = text
        self.font = font
        self.size = size
        self.color = color
        self.x = x
        self.y = y
        self.gameDisplay = display
        self.TextSurf, self.TextRect = self.text_objects(pygame.font.Font(self.font,self.size))
        self.shouldUpdate = shouldUpdate
        self.pos = pos
        self.AddText()  #Update Text
        self.prevTextLength = len(str(text))
        
    
    def text_objects(self, font, backgroundColor=None):
        # Make a text object and return its surface and rectangle
        if backgroundColor == None:
            textSurf = font.render(self.text,True,self.color)
        else:
            textSurf = font.render(self.text,True,self.color,backgroundColor)
        return textSurf, textSurf.get_rect()

    def AddText(self, forceUpdate=False,backgroundColor=None):
        self.TextSurf, self.TextRect = self.text_objects(pygame.font.Font(self.font,self.size),backgroundColor)

        # Make the text positioned based on given args
        if self.pos == 'topleft':
            self.TextRect.x = self.x
            self.TextRect.y = self.y
        elif self.pos == 'topright':
            self.TextRect.x = self.x - self.TextRect.w
            self.TextRect.y = self.y
        elif self.pos == 'bottomright':
            self.TextRect.x = self.x - self.TextRect.w
            self.TextRect.y = self.y - self.TextRect.h
        elif self.pos == 'bottomleft':
            self.TextRect.x = self.x
            self.TextRect.y = self.y - self.TextRect.h
        elif self.pos == 'center':
            self.TextRect.center = (self.x,self.y)
        else:
            print("Error: ", self.pos, " is not a valid text position")

        # Update the text on screen
        if self.shouldUpdate or forceUpdate:
            self.gameDisplay.blit(self.TextSurf, self.TextRect)
            pygame.display.update(self.TextRect)

    def ForceUpdate(self, newText=None, backgroundColor=None):
        # Force text to update
        if newText != None:
            tempstr = " "
            if len(newText) < self.prevTextLength:
                factor = self.prevTextLength - len(newText)
                tempstr = tempstr * factor * 3
                
            self.prevTextLength = len(newText)
            self.text = newText + tempstr
            self.AddText(True,backgroundColor)
        else:
            self.gameDisplay.blit(self.TextSurf, self.TextRect)
            pygame.display.update(self.TextRect)