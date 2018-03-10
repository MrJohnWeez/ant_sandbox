import pygame
import Colors
import random

class Ant:
    updateArray = []
    antArray = []
    def __init__(self, x, y, box, facing, display, step=(1,1,1,1)):
        """Define a basic ant. Moves by step when on black"""
        self.box = box
        self.x = x
        self.y = y
        self.facing = facing # 0 = up, 1 = right, 2 = down, 3 = left
        self.stepUp = step[0]
        self.stepDown = step[1]
        self.stepLeft = step[2]
        self.stepRight = step[3]
        self.display = display
        self.TempScreenColor = self.display.get_at((self.x,self.y))
        self.isAlive = True
        
    @classmethod
    def GetRectUpdates(cls):
        """Returns all the rects that ants have updated on screen and clears update array. Used for screen update optimization"""
        temp = []
        temp += cls.updateArray
        cls.updateArray.clear()
        return temp


    @classmethod
    def UpdateAllAnts(cls):
        """Move all ants on screen"""
        temp = []
        temp += cls.antArray
        cls.antArray.clear()
        for a in temp:
            a.Update()
    @classmethod
    def GetAntCount(cls):
        return len(cls.antArray)

    @classmethod
    def KillAllAnts(cls):
        cls.antArray.clear()
        

    def Spawn(self):
        Ant.antArray.append(self)
        self.display.set_at((self.x,self.y), Colors.A_black)
        
        pygame.display.update(pygame.Rect(self.x,self.y,1,1))
        

    def __get_x(self):
        return self.__x

    def ChangeStep(self, up=1, down=1, left=1, right=1):
        self.stepUp = up
        self.stepDown = down
        self.stepLeft = left
        self.stepRight = right


    def __set_x(self, x):
        if(x > self.box.w-1):
            x = self.box.x + (x-self.box.w)
        if(x < self.box.x):
            x = self.box.w-1 - (self.box.x - x-1)
        self.__x = x

    x = property(__get_x, __set_x)

    def __get_y(self):
        return self.__y


    def __set_y(self, y):
        if(y > self.box.h-1):
            y = self.box.y + (y-self.box.h)
        if(y < self.box.y):
            y = self.box.h-1 - (self.box.y - y-1)
        self.__y = y

    y = property(__get_y, __set_y)


    def move_main(self):
        if self.facing == 0:
            self.facing = 3
            self.x -= self.stepLeft
        elif self.facing == 1:
            self.facing = 0
            self.y -= self.stepUp
        elif self.facing == 2:
            self.facing = 1
            self.x += self.stepRight
        elif self.facing == 3:
            self.facing = 2
            self.y += self.stepDown

    def move_mainO(self):
        if self.facing == 0:
            self.facing = 1
            self.x += self.stepLeft
        elif self.facing == 1:
            self.facing = 2
            self.y += self.stepUp
        elif self.facing == 2:
            self.facing = 3
            self.x -= self.stepRight
        elif self.facing == 3:
            self.facing = 0
            self.y -= self.stepDown

    def move_basic(self):
        if self.facing == 0:
            self.facing = 1
            self.x += 1
        elif self.facing == 1:
            self.facing = 2
            self.y += 1
        elif self.facing == 2:
            self.facing = 3
            self.x -= 1
        elif self.facing == 3:
            self.facing = 0
            self.y -= 1
    

    def Update(self):
        Ant.antArray.append(self)
        pix = self.display.get_at((self.x,self.y))
        if pix == Colors.A_black:
            # set current tile to white
            Ant.updateArray.append(pygame.Rect(self.x,self.y,1,1))
            self.display.set_at((self.x,self.y), Colors.A_white)
            # turn left and move
            self.move_main()

        elif pix == Colors.A_white or pix == Colors.A_blue:
            # set current tile to white
            Ant.updateArray.append(pygame.Rect(self.x,self.y,1,1))
            self.display.set_at((self.x,self.y), Colors.A_black)
            # turn right and move
            self.move_mainO()
    def ShowAnt(self, ShouldShow):
        if ShouldShow:
            self.TempScreenColor = self.display.get_at((self.x,self.y))
            Ant.updateArray.append(pygame.Rect(self.x,self.y,1,1))
            self.display.fill(Colors.A_red, ((self.x,self.y), (1,1)))
        else:
            Ant.updateArray.append(pygame.Rect(self.x,self.y,1,1))
            self.display.fill(self.TempScreenColor, ((self.x,self.y), (1,1)))






class AntFriendly(Ant):
    def __init__(self, x, y, box, facing, display, step=(1,1,1,1)):
        super().__init__(x, y, box, facing, display, step)

    def move_random(self):
        r = random.randint(0,3)
        if r == 0: self.x += 1
        elif r == 1: self.y += 1
        elif r == 2: self.x -= 1
        elif r == 3: self.y -= 1


    def Update(self):
        Ant.antArray.append(self)
        pix = self.display.get_at((self.x,self.y))
        if pix == Colors.A_white:
            # set current tile to white
            # self.display.set_at((self.x,self.y), Colors.A_blue)
            Ant.updateArray.append(pygame.Rect(self.x,self.y,1,1))
            self.display.fill(Colors.A_blue, ((self.x,self.y), (1,1)))
            # turn left and move
            self.move_main()
        else:
            self.move_random()

    def Spawn(self):
        Ant.antArray.append(self)
        self.display.set_at((self.x,self.y), Colors.A_blue)
        pygame.display.update(pygame.Rect(self.x,self.y,1,1))







