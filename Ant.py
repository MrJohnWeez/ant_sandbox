import pygame
import Colors
import random

class Ant:
    updateArray = []
    antArray = []
    def __init__(self, x, y, box, facing, display, step=(1,1,1,1), speed=0):
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
        self.speed = speed
        self.currSpeed = 0
        
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
        """Returns the number of ants that are alive"""
        return len(cls.antArray)

    @classmethod
    def KillAllAnts(cls):
        """Kills all living ants"""
        cls.antArray.clear()
        

    def Spawn(self):
        """Places a black pixel where a normal ant would spawn"""
        Ant.antArray.append(self)
        self.display.set_at((self.x,self.y), Colors.A_black)
        
        pygame.display.update(pygame.Rect(self.x,self.y,1,1))
        

    def __get_x(self):
        return self.__x

    def ChangeStep(self, up=1, down=1, left=1, right=1):
        """Changes the varibles for the ant steps"""
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


    #Ant Move Functions
    def MoveLeftStep(self):
        """Ant turns left and moves its current step that direction"""
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

    def MoveRightStep(self):
        """Ant turns right and moves its current step that direction"""
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

    def MoveBasicRight(self):
        """Ant turns Right but only moves one space"""
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

    def MoveCurrentSpace(self):
        """Moves one space in the current ant direction facing"""
        if self.facing == 0:
            self.y -= 1
        elif self.facing == 1:
            self.x += 1
        elif self.facing == 2:
            self.y += 1
        elif self.facing == 3:
            self.x -= 1

    def MoveRandom(self):
        """Ant will move a random direction by one space"""
        r = random.randint(0,3)
        if r == 0: self.x += 1
        elif r == 1: self.y += 1
        elif r == 2: self.x -= 1
        elif r == 3: self.y -= 1

    def Move180(self):
        """Ant turns 180 degrees and moves one step"""
        if self.facing == 0:
            self.facing = 1
            self.x -= self.stepLeft
        elif self.facing == 1:
            self.facing = 2
            self.y -= self.stepUp
        elif self.facing == 2:
            self.facing = 3
            self.x += self.stepRight
        elif self.facing == 3:
            self.facing = 0
            self.y += self.stepDown



    def Update(self):
        """A normal black ant path"""
        self.currSpeed += 1
        if self.isAlive:
             Ant.antArray.append(self)
        if self.currSpeed >= self.speed:
            self.currSpeed = 0
            pix = self.display.get_at((self.x,self.y))
            if pix == Colors.A_black:
                # set current tile to white
                Ant.updateArray.append(pygame.Rect(self.x,self.y,1,1))
                self.display.set_at((self.x,self.y), Colors.A_white)
                # turn left and move
                self.MoveLeftStep()

            elif pix == Colors.A_white or pix == Colors.A_blue:
                # set current tile to white
                Ant.updateArray.append(pygame.Rect(self.x,self.y,1,1))
                self.display.set_at((self.x,self.y), Colors.A_black)
                # turn right and move
                self.MoveRightStep()
            elif pix == Colors.A_Fire:
                self.isAlive = False
            

    def ShowAnt(self, ShouldShow):
        """Toggles the ant to show its position with a color"""
        if ShouldShow:
            self.TempScreenColor = self.display.get_at((self.x,self.y))
            Ant.updateArray.append(pygame.Rect(self.x,self.y,1,1))
            self.display.fill(Colors.A_red, ((self.x,self.y), (1,1)))
        elif pix == Colors.A_Fire:
            self.isAlive = False
        else:
            Ant.updateArray.append(pygame.Rect(self.x,self.y,1,1))
            self.display.fill(self.TempScreenColor, ((self.x,self.y), (1,1)))







#####################################################################################################################################################################
class AntWater(Ant):
    def __init__(self, x, y, box, facing, display, step=(1,1,1,1), speed=0):
        super().__init__(x, y, box, facing, display, step, speed)

    def Update(self):
        """Moves in a random direction if not on a white square"""
        if self.isAlive:
            Ant.antArray.append(self)
        pix = self.display.get_at((self.x,self.y))
        if pix == Colors.A_white or pix == Colors.A_Fire:
            # set current tile to white
            # self.display.set_at((self.x,self.y), Colors.A_blue)
            Ant.updateArray.append(pygame.Rect(self.x,self.y,1,1))
            self.display.fill(Colors.A_blue, ((self.x,self.y), (1,1)))
            # turn left and move
            self.MoveLeftStep()
        else:
            self.MoveRandom()

    def Spawn(self):
        """Spawns ant in game and turns the current mouse pos to color of ant"""
        Ant.antArray.append(self)
        self.display.set_at((self.x,self.y), Colors.A_blue)
        pygame.display.update(pygame.Rect(self.x,self.y,1,1))

#####################################################################################################################################################################
class AntWood(Ant):
    def __init__(self, x, y, box, facing, display, step=(1,1,1,1), speed=0):
        super().__init__(x, y, box, facing, display, step, speed)
        self.shouldMove = False


    def Grow(self):
        """Ant will only stay on connected blue areas and will turn blue to brown"""
        oldx = self.x
        oldy = self.y
        randBlue = []
        randBrown = []
        for i in range(0,4):
            if i == 0:
                self.y -= 1
            elif i == 1:
                self.x += 1
            elif i == 2:
                self.y += 1
            elif i == 3:
                self.x -= 1

            pix = self.display.get_at((self.x,self.y))
            if pix == Colors.A_blue:
                randBlue.append(i)
            elif pix == Colors.A_Wood:
                randBrown.append(i)
            elif pix == Colors.A_Fire:
                self.isAlive = False
            self.x = oldx
            self.y = oldy
        
        if len(randBlue) != 0:
            r = random.randint(0,len(randBlue)-1)
            self.facing = randBlue[r]
            self.MoveCurrentSpace()
        elif len(randBrown) != 0:
            r = random.randint(0,len(randBrown)-1)
            self.facing = randBrown[r]
            self.MoveCurrentSpace()


    def Update(self):
        """Turns blue pixels to brown and fills any connected blue squares to brown"""
        if self.isAlive:
            Ant.antArray.append(self)
        pix = self.display.get_at((self.x,self.y))
        if pix == Colors.A_blue:
            Ant.updateArray.append(pygame.Rect(self.x,self.y,1,1))
            self.display.fill(Colors.A_Wood, ((self.x,self.y), (1,1)))
        self.Grow()


    def Spawn(self):
        """Spawns ant in game and turns the current mouse pos to color of ant"""
        Ant.antArray.append(self)
        self.display.set_at((self.x,self.y), Colors.A_Wood)
        pygame.display.update(pygame.Rect(self.x,self.y,1,1))

#####################################################################################################################################################################
class AntFire(Ant):
    def __init__(self, x, y, box, facing, display, step=(1,1,1,1), speed=0):
        super().__init__(x, y, box, facing, display, step, speed)
        self.shouldMove = False

    def Update(self):
        if self.isAlive:
            Ant.antArray.append(self)
        pix = self.display.get_at((self.x,self.y))
        if pix == Colors.A_blue:
            self.isAlive = False
        else:
            Ant.updateArray.append(pygame.Rect(self.x,self.y,1,1))
            self.display.fill(Colors.A_Fire, ((self.x,self.y), (1,1)))
            oldx = self.x
            oldy = self.y
            if self.facing == 0:
                self.x -= self.stepRight
            elif self.facing == 1:
                self.y -= self.stepUp
            elif self.facing == 2:
                self.x += self.stepLeft
            elif self.facing == 3:
                self.y += self.stepDown

            if self.display.get_at((self.x,self.y)) != Colors.A_Fire:
                r = self.facing-1
                if r == -1:
                    r = 3
                self.facing = r
            else:
                self.x = oldx
                self.y = oldy
                self.MoveCurrentSpace()
                
            

    def Spawn(self):
        """Spawns ant in game and turns the current mouse pos to color of ant"""
        Ant.antArray.append(self)
        self.display.set_at((self.x,self.y), Colors.A_Fire)
        pygame.display.update(pygame.Rect(self.x,self.y,1,1))


#####################################################################################################################################################################
class AntPlant(Ant):
    def __init__(self, x, y, box, facing, display, step=(1,1,1,1), speed=0):
        super().__init__(x, y, box, facing, display, step, speed)
        self.shouldMove = False

    def Grow(self):
        """Ant will only stay on connected blue areas and will turn blue to green"""
        oldx = self.x
        oldy = self.y
        randBlue = []
        randGreen = []
        for i in range(0,4):
            if i == 0:
                self.y -= 1
            elif i == 1:
                self.x += 1
            elif i == 2:
                self.y += 1
            elif i == 3:
                self.x -= 1

            pix = self.display.get_at((self.x,self.y))
            if pix == Colors.A_blue:
                randBlue.append(i)
            elif pix == Colors.A_green:
                randGreen.append(i)
            elif pix == Colors.A_Fire:
                self.isAlive = False
            self.x = oldx
            self.y = oldy
        
        if len(randBlue) != 0:
            r = random.randint(0,len(randBlue)-1)
            self.facing = randBlue[r]
            self.MoveCurrentSpace()
        elif len(randGreen) != 0:
            r = random.randint(0,len(randGreen)-1)
            self.facing = randGreen[r]
            self.MoveCurrentSpace()


    def Update(self):
        """Turns blue pixels to green and fills any connected blue squares to green"""
        if self.isAlive:
            Ant.antArray.append(self)
        pix = self.display.get_at((self.x,self.y))
        if pix == Colors.A_blue:
            Ant.updateArray.append(pygame.Rect(self.x,self.y,1,1))
            self.display.fill(Colors.A_green, ((self.x,self.y), (1,1)))
        self.Grow()


    def Spawn(self):
        """Spawns ant in game and turns the current mouse pos to color of ant"""
        Ant.antArray.append(self)
        self.display.set_at((self.x,self.y), Colors.A_green)
        pygame.display.update(pygame.Rect(self.x,self.y,1,1))





