import pygame

class Text:
    def __init__(self, text, font, size, color, x, y, display, shouldUpdate=False, pos='topleft', backgroundColor=None):
        """Creates a text object that can be updated"""
        self.text = text
        self.font = font
        self.size = size
        self.color = color
        self.x = x
        self.y = y
        self.gameDisplay = display
        self.backgroundColor = backgroundColor
        self.TextSurf, self.TextRect = self.text_objects(pygame.font.Font(self.font,self.size))
        self.shouldUpdate = shouldUpdate
        self.pos = pos
        self.AddText()  #Update Text
        self.prevTextLength = len(str(text))
        
        
    
    def text_objects(self, font):
        """ Returns the new rendered text surface and its Rect """
        # Make a text object and return its surface and rectangle
        if self.backgroundColor == None:
            textSurf = font.render(self.text,True,self.color)
        else:
            textSurf = font.render(self.text,True,self.color,self.backgroundColor)
        return textSurf, textSurf.get_rect()

    def AddText(self, newText=None, forceUpdate=False):
        """changes and updates the text object"""
        if newText != None:
            # Make text rect same length as before to clear old text out
            tempstr = " "
            if len(newText) < self.prevTextLength:
                factor = self.prevTextLength - len(newText)
                tempstr = tempstr * factor * 3
            else:
                tempstr = ""
                
            self.prevTextLength = len(newText)
            self.text = newText + tempstr
            
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
            pygame.display.update(self.TextRect)

    def ForceBlit(self):
        """Forces to draw the text to screen but does not update it"""
        self.gameDisplay.blit(self.TextSurf, self.TextRect)

    def GetWidth(self):
        """Returns width of text object"""
        return self.TextRect.w

    def GetHieght(self):
        """Returns hiehgt of text object"""
        return self.TextRect.h
    
    def GetX(self):
        """Returns x position of text object"""
        return self.TextRect.x
    def GetY(self):
        """Returns y position of text object"""
        return self.TextRect.y
    def GetRect(self):
        """Returns whole rect of text object"""
        return self.TextRect



