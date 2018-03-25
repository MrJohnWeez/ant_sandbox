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
        self.prevTextLength = len(str(text))
        self.AddText()  #Update Text
        
    
    def text_objects(self, font):
        """ Returns the new rendered text surface and its Rect """
        # Make a text object and return its surface and rectangle
        if self.backgroundColor == None:
            textSurf = font.render(self.text,True,self.color)
        else:
            textSurf = font.render(self.text,True,self.color,self.backgroundColor)
        return textSurf, textSurf.get_rect()

    def UpdateTextPos(self):
        """Make the text positioned based on given args"""
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

    def AddText(self, newText=None, forceUpdate=False):
        """Changes and updates the text object"""
        #If string value is shorter then prevous remove extra chars on screen
        if newText != None and len(newText) < self.prevTextLength:
            tempstr = " "
            tempstr = tempstr * self.prevTextLength * 3
            self.prevTextLength = 0
            self.text = tempstr
            self.AddText(tempstr,True)
            self.text = newText
            self.prevTextLength = len(newText)
        elif newText != None:
            self.text = newText
            self.prevTextLength = len(newText)
            
        self.TextSurf, self.TextRect = self.text_objects(pygame.font.Font(self.font,self.size))
        self.UpdateTextPos()

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
    def GetText(self):
        return self.text



