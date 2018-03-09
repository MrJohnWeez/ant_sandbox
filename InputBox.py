import pygame
import Text
class InputBox:
    def __init__(self, x, y, w, h, boxColor, bgColor, display, textObject, action=None):
        self.textObject = textObject
        self.rect = pygame.Rect(x, y, w, h)
        self.boxColorN = boxColor
        self.boxColorA = pygame.Color(0,0,0)
        self.color = boxColor
        self.bgColor = bgColor
        self.active = False
        self.display = display
        self.boarderSize = 2
        self.action = action

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                if self.textObject.text.isdigit() and event.button == 4 or event.button == 5 and self.textObject.text != '':
                    if event.button == 4: self.textObject.text = str(int(self.textObject.text)+1)
                    elif event.button == 5: self.textObject.text = str(int(self.textObject.text)-1)
                    self.active = False
                    self.updateText()
                    if self.action != None:
                        self.action(self)

                else:
                    self.active = not self.active
                    self.updateText("")
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
        self.color = self.boxColorA if self.active else self.boxColorN
        pygame.draw.rect(self.display, self.bgColor, pygame.Rect(self.rect.x,self.rect.y,self.rect.w+self.boarderSize,self.rect.h+self.boarderSize))
        pygame.draw.rect(self.display, self.color, self.rect, self.boarderSize)
        self.display.blit(self.textObject.TextSurf, (self.rect.x+4, int(self.rect.y+(self.rect.h/2)-self.textObject.GetHieght()/2)+2))
        pygame.display.update(pygame.Rect(self.rect.x,self.rect.y,self.rect.w+self.boarderSize,self.rect.h+self.boarderSize))
        
        
    def updateText(self, newText=None):
        if newText != None:
            self.textObject.AddText(newText,True)
        else:
            self.textObject.AddText()
        # self.txt_surface = self.FONT.render(self.textObject.text, True, pygame.Color(255,255,255))
        self.update()

    def getText(self):
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