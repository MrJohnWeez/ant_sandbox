import pygame
import Button
import Text


class AntStepButton:
    def __init__(self, x, y, buttonColor, Display):
        self.x = x
        self.y = y
        self.buttonColor = buttonColor
        self.Display = Display
        self.b1 = Button.Button("<<<", x,y,30,25, buttonColor, Display, print("Hello"))
        self.b2 = Button.Button("<<", x+30,y,20,25, buttonColor, Display, print("Hello"))
        self.b3 = Button.Button("<", x+50,y,10,25, buttonColor, Display, print("Hello"))
        self.b4 = Button.Button(">", x+100,y,10,25, buttonColor, Display, print("Hello"))
        self.b5 = Button.Button(">>", x+110,y,20,25, buttonColor, Display, print("Hello"))
        self.b6 = Button.Button(">>>", x+130,y,30,25, buttonColor, Display, print("Hello"))
        self.buttonArray = [self.b1,self.b2,self.b3,self.b4,self.b5,self.b6]

    def draw(self):
        for b in self.buttonArray:
            b.DrawButton()

    def update(self, mousex, mousey):
        for b in self.buttonArray:
            b.Update(mousex, mousey)