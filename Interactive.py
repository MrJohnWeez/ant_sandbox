import pygame
import Colors
import Text
import ImageManager



######################################################################################################################################################################
######################################################################################################################################################################
#BUTTONS            BUTTONS            BUTTONS            BUTTONS            BUTTONS            BUTTONS            BUTTONS            BUTTONS            BUTTONS
######################################################################################################################################################################
######################################################################################################################################################################

class ButtonBase:
    """Button Base class that all buttons most likey use"""
    def __init__(self, x, y, w, h, normalColor, display, textObject, action=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
        self.gameDisplay = display
        self.action = action
        self.textObject = textObject

        self.normalColor = normalColor
        self.clickColor = Colors.shadeAlpha(normalColor, -0.2)
        self.hoverColor = Colors.shade(normalColor, 0.1)

    def ChangeMsg(self,newMsg):
        """ Changes the text over the button """
        self.textObject.AddText(newMsg)

    def UpdateToScreen(self, buttonColor):
        """Draw button on screen"""
        #Update the text object and update the whole button on the game screen
        pygame.draw.rect(self.gameDisplay, buttonColor, (self.x,self.y,self.w,self.h))
        self.textObject.TextRect.center = ((self.x+(self.w/2)),(self.y+(self.h/2)))
        self.textObject.ForceBlit()
        pygame.display.update(pygame.Rect(self.x, self.y, self.w, self.h))
    def AutoFont(self):
        self.textObject.size = self.h
        self.textObject.AddText(forceUpdate=True)
        while self.textObject.GetWidth() > self.w:
            self.textObject.size -= 1
            self.textObject.AddText(forceUpdate=True)

    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getW(self):
        return self.w
    def getH(self):
        return self.h
    def getTopLeft(self):
        """Returns top left cornner cordinate"""
        return (self.getX(), self.getY())
    def getTopRight(self):
        """Returns top right cornner cordinate"""
        return (self.getX()+self.getW(), self.getY())
    def getBottomLeft(self):
        """Returns bottom left cornner cordinate"""
        return (self.getX(), self.getY()+self.getH())
    def getBottomRight(self):
        """Returns bottom right cornner cordinate"""
        return (self.getX()+self.getW(), self.getY()+self.getH())
    def getCenter(self):
        return (self.getX()+self.getW()//2,self.getY()+self.getH()//2)
    def getBottomCenter(self):
        return (self.getX()+self.getW()//2,self.getY()+self.getH())
    def getTopCenter(self):
        return (self.getX()+self.getW()//2,self.getY())  
    def getRect(self):
        return pygame.Rect(self.x,self.y,self.w,self.h)

######################################################################################################################################################################

class Button(ButtonBase):
    """Creates a button object that can be clicked"""
    def __init__(self, x, y, w, h, normalColor, display, textObject, action=None, autoFontSize=False,pos='topleft'):
        self.pos = pos
        if self.pos == 'topright':
            x = x - w
        elif self.pos == 'bottomright':
            x = x - w
            y = y - h
        elif self.pos == 'bottomleft':
            y = y - h
        elif self.pos == 'center':
            x = x - (w//2)
            y = y - (h//2)
        elif self.pos == 'bottomcenter':
            x = x - (w//2)
            y = y - h
        elif self.pos == 'topcenter':
            x = x - (w//2)
        super().__init__(x, y, w, h, normalColor, display, textObject, action)
        if autoFontSize:
            self.AutoFont()
        
        self.state = 1
        self.UpdateToScreen(self.normalColor)
        
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
                
        elif self.state == 2 and pygame.mouse.get_pressed()[0] == 0:
            #Mouse has stopped holding down click so turn button to normal color
            self.UpdateToScreen(self.normalColor)
            self.state = 0
            self.action()

    #Draws initual button state
    def DrawButton(self):
        """ Draws button on command"""
        self.UpdateToScreen(self.normalColor)
        self.Update()
    

    
######################################################################################################################################################################

class ButtonImage(ButtonBase):
    """Creates a button object that can be clicked with an image as the button"""
    def __init__(self, x, y, w, h, normalImagePath, hoverImagePath, clickedImagePath, display, textObject, action=None, autoFontSize=False, pos='topleft'):
        normalColor = Colors.A_black
        self.pos = pos

        #Set realitive Rect position depending on what the user wants
        if self.pos == 'topright': 
            x = x - w
        elif self.pos == 'bottomright':
            x = x - w
            y = y - h
        elif self.pos == 'bottomleft':
            y = y - h
        elif self.pos == 'center':
            x = x - (w//2)
            y = y - (h//2)
        elif self.pos == 'bottomcenter':
            x = x - (w//2)
            y = y - h
        elif self.pos == 'topcenter':
            x = x - (w//2)

        super().__init__(x, y, w, h, normalColor, display, textObject, action)
        if autoFontSize:
            self.AutoFont()

        self.image = pygame.Surface((self.w,self.h))  # Create image surface
        self.UpdateBackground()
        
           
        self.state = 1
        self.normalImage = ImageManager.ImageType(normalImagePath,display)
        self.hoverImage = ImageManager.ImageType(hoverImagePath,display)
        self.clickedImage = ImageManager.ImageType(clickedImagePath,display)
        self.UpdateImageScales()
        self.normalTextSize = self.textObject.size
        self.UpdateToScreenImage("Normal")

    def UpdateImageScales(self):
        """Updates the scales of hover,normal,clicked images based on the button box size"""
        self.normalImage.Scale((self.w/self.normalImage.getW())*0.9,(self.h/self.normalImage.getH())*0.9)
        self.hoverImage.Scale(self.w/self.hoverImage.getW(),self.h/self.hoverImage.getH())
        self.clickedImage.Scale(self.w/self.clickedImage.getW(),self.h/self.clickedImage.getH())

    def UpdateBackground(self):
        self.image.blit(self.gameDisplay,(0,0),((self.x,self.y),(self.w,self.h)))  # Blit portion of the display to the image

    def UpdateToScreenImage(self, buttonImageType):
        """Draw image button on screen"""
        imageType = self.normalImage
        if buttonImageType == "Hover":
            self.textObject.size = int(self.normalTextSize*1.1)
            self.textObject.AddText(forceUpdate=False)
            imageType = self.hoverImage
        elif buttonImageType == "Clicked":
            self.textObject.size = self.normalTextSize
            self.textObject.AddText(forceUpdate=False)
            imageType = self.clickedImage
        else:
            self.textObject.size = self.normalTextSize
            self.textObject.AddText(forceUpdate=False)

        self.gameDisplay.blit(self.image,(self.x,self.y))
        imageType.Draw(self.getCenter())
            
        #Update the text object and update the whole button on the game screen
        self.textObject.TextRect.center = self.getCenter()
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
            self.UpdateToScreenImage("Hover")
            
        elif not moveOver and (self.state == 1 or self.state == 2):
            #Mouse no longer over button change color state to normal
            self.state = 0
            self.UpdateToScreenImage("Normal")

        elif moveOver and self.state == 1:
            #Mouse is over button and it is ready to be clicked
            click = pygame.mouse.get_pressed()
            if click[0] == 1 and self.action != None:
                self.state = 2
                self.UpdateToScreenImage("Clicked")
                

        elif self.state == 2 and pygame.mouse.get_pressed()[0] == 0:
            #Mouse has stopped holding down click so turn button to normal color
            self.UpdateToScreenImage("Normal")
            self.state = 0
            self.action()

    #Draws initual button state
    def DrawButton(self):
        """ Draws button on command"""
        self.Update()
        self.UpdateToScreenImage("Normal")

######################################################################################################################################################################

class ButtonToggle(ButtonBase):
    """A button that toggles. Turns darker when clicked"""
    def __init__(self, x, y, w, h, normalColor, display, textObject, action=None, Toggled=False):
        super().__init__(x, y, w, h, normalColor, display, textObject, action)
        self.state = 0
        self.toggled = Toggled
        self.prevClick = -1
        
    def ChangeMsg(self,newMsg):
        """ Changes the text over the button """
        self.textObject.AddText(newMsg)
        if self.toggled:
            self.ToggleOn(True)
        else:
            self.ToggleOff(True)

    def ToggleOn(self, ignoreFunction=False):
        """Button will be toggled"""
        self.state = 1
        self.toggled = True
        self.UpdateToScreen(self.clickColor)
        if self.action != None and not ignoreFunction:
            self.action()

    def ToggleOff(self, ignoreFunction=False):
        """Button will not be toggled"""
        self.toggled = False
        self.state = 0
        self.UpdateToScreen(self.normalColor)
        if self.action != None and not ignoreFunction:
            self.action()
        
    def Update(self):
        """Update the toggle box depending on the mouse location and input"""
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
        """Force the state of the button"""
        if ToggleOn:
            self.ToggleOn(True)
        else:
            self.ToggleOff(True)
            
    #Draws initual button state
    def DrawButton(self):
        """Draw the button in its off state"""
        self.ToggleOff(True)







######################################################################################################################################################################
######################################################################################################################################################################
#USER INPUTS            #USER INPUTS                #USER INPUTS            #USER INPUTS            #USER INPUTS            #USER INPUTS               #USER INPUTS
######################################################################################################################################################################
######################################################################################################################################################################

class InputBox:
    """Creates an input box that allows the user to enter any text and if they text is a number they are
        able to scroll with the mouse wheel"""
    def __init__(self, x, y, w, h, boxColor, bgColor, display, textObject, action=None, boarderSize=2):
        self.textObject = textObject
        self.rect = pygame.Rect(x, y, w, h)
        self.boxColorN = boxColor
        self.boxColorA = Colors.shadeAlpha(boxColor, -0.5)
        self.color = boxColor
        self.bgColor = bgColor
        self.active = False
        self.display = display
        self.boarderSize = boarderSize
        self.action = action

    def handle_event(self, event):
        """Set the box active and run the action if the user has clicked putside box or pressed
        enter"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                if self.textObject.text.isdigit() and (event.button == 4 or event.button == 5) and self.textObject.text != '':
                    if event.button == 4: self.textObject.text = str(int(self.textObject.text)+1)
                    elif event.button == 5: self.textObject.text = str(int(self.textObject.text)-1)
                    self.active = False
                    self.updateText()
                    if self.action != None:
                        self.action(self)
                else:
                    self.active = not self.active
                    self.updateText("")
                    if not self.active:
                        if self.action != None:
                            self.action(self)
            elif self.active:
                if self.action != None:
                    self.action(self)
                self.active = False
                self.updateText()
            # Change the current color of the input box.
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    if self.action != None:
                        self.action(self)
                    self.active = not self.active
                elif event.key == pygame.K_BACKSPACE:
                    self.textObject.text = self.textObject.text[:-1]
                else:
                    self.textObject.text += event.unicode
                # Re-render the text.
                self.updateText()

    def update(self):
        """Update entire box to screen"""
        self.color = self.boxColorA if self.active else self.boxColorN
        pygame.draw.rect(self.display, self.bgColor, pygame.Rect(self.rect.x,self.rect.y,self.rect.w+self.boarderSize,self.rect.h+self.boarderSize))
        pygame.draw.rect(self.display, self.color, self.rect, self.boarderSize)
        self.display.blit(self.textObject.TextSurf, (self.rect.x+4, int(self.rect.y+(self.rect.h/2)-self.textObject.GetHieght()/2)+2))
        pygame.display.update(pygame.Rect(self.rect.x,self.rect.y,self.rect.w+self.boarderSize,self.rect.h+self.boarderSize))
        
        
    def updateText(self, newText=None):
        """Update text object first then update to screen"""
        if newText != None:
            self.textObject.AddText(newText,True)
        else:
            self.textObject.AddText()
        # self.txt_surface = self.FONT.render(self.textObject.text, True, pygame.Color(255,255,255))
        self.update()

    def getText(self):
        """Returns the text in the box"""
        return self.textObject.text
    def getX(self):
        return self.rect.x
    def getY(self):
        return self.rect.y
    def getW(self):
        return self.rect.w
    def getH(self):
        return self.rect.h
    def getTopLeft(self):
        return (self.getX(), self.getY())
    def getTopRight(self):
        return (self.getX()+self.getW(), self.getY())
    def getBottomLeft(self):
        return (self.getX(), self.getY()+self.getH())
    def getBottomRight(self):
        return (self.getX()+self.getW(), self.getY()+self.getH())




######################################################################################################################################################################