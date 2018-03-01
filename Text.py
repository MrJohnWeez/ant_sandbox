import pygame

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
        
    
    def text_objects(self, font):
        # Make a text object and return its surface and rectangle
        textSurf = font.render(self.text,True,self.color)
        return textSurf, textSurf.get_rect()

    def AddText(self, forceUpdate=False):
        self.TextSurf, self.TextRect = self.text_objects(pygame.font.Font(self.font,self.size))

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
            pygame.display.update(self.TextRect) #self.TextRect

    def ForceUpdate(self, newText=None):
        # Force text to update
        if newText != None:
            self.text = newText
            AddText(True)
        else:
            self.gameDisplay.blit(self.TextSurf, self.TextRect)
            pygame.display.update(self.TextRect)
