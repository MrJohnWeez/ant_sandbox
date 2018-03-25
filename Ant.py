import pygame
import Colors
import random

class Ant:
    """Base ant that contains all the general moving functions and varibles"""
    updateArray = []
    antArray = []
    antLimit = 0
    maxSpeed = 6000
    def __init__(self, x, y, box, facing, display, step=(1,1,1,1), speed=0):
        """Define a basic ant. Moves by step when on black"""
        #pos
        self.box = box
        self.x = x
        self.y = y
        self.facing = facing # 0 = up, 1 = right, 2 = down, 3 = left
        self.stepUp = step[0]
        self.stepDown = step[1]
        self.stepLeft = step[2]
        self.stepRight = step[3]

        #display
        self.display = display
        self.TempScreenColor = self.display.get_at((self.x,self.y))

        #properties
        self.isAlive = True

        #speed
        self.speed = speed
        self.speedScalar = Ant.maxSpeed-1000+1
        self.TicksLeft = self.speedScalar-speed
        self.lifeSpan = 1000 #Number of steps ant can walk through acid before diying (Unless otherwise noted)
        
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
        i = 0
        tempMax = Ant.GetAntLimit()
        for a in temp:
            if i == tempMax:
                break
            a.Update()
            i += 1
            
    @classmethod
    def GetAntCount(cls):
        """Returns the number of ants that are alive"""
        return len(cls.antArray)

    @classmethod
    def KillAllAnts(cls):
        """Kills all living ants"""
        cls.antArray.clear()

    @classmethod
    def KillAntsInRect(cls, givenRect=pygame.Rect(1,1,1,1)):
        """Kills all living ants within the given Rect"""
        assert type(givenRect) == pygame.Rect
        for a in cls.antArray:
            if givenRect.x+givenRect.w > a.x >= givenRect.x and givenRect.y+givenRect.h > a.y >= givenRect.y:
                a.isAlive = False

    @classmethod
    def SetAntLimit(cls, value=0):
        """Limits how many ants are allowed to live at a time"""
        cls.antLimit = value
    @classmethod
    def GetAntLimit(cls):
        """Limits how many ants are allowed to live at a time"""
        return cls.antLimit

    def Spawn(self):
        """Places an ant on screen"""
        if len(Ant.antArray) < Ant.antLimit:
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

    def MoveZombie(self):
        r = random.randint(0,9)
        if r == 0 or (self.facing == 1 and r == 8): 
            self.x += 1
            self.y += 1
        elif r == 1 or (self.facing == 3 and r == 8): 
            self.x -= 1
            self.y += 1
        elif r == 2 or (self.facing == 1 and r == 9): 
            self.x += 1
            self.y -= 1
        elif r == 3 or (self.facing == 3 and r == 9): 
            self.x -= 1
            self.y -= 1
        elif r == 4: 
            self.x += 1
        elif r == 5 or (self.facing == 2 and r == 8): 
            self.y += 1
        elif r == 6: 
            self.x -= 1
        elif r == 7 or (self.facing == 0 and r == 8): 
            self.y -= 1

    def Update(self, AutoUpdate=True):
        """A normal black ant path"""
        if self.isAlive and AutoUpdate:
            Ant.antArray.append(self)
        self.TicksLeft -= 1
        if self.TicksLeft <= 0:
            #print(self.speedScalar,"     ", self.speed, "      ", self.speedScalar-self.speed)
            self.TicksLeft = self.speedScalar-self.speed
            pix = self.display.get_at((self.x,self.y))
            if pix == Colors.A_black:
                # set current tile to white
                Ant.updateArray.append(pygame.Rect(self.x,self.y,1,1))
                self.display.set_at((self.x,self.y), Colors.A_white)
                # turn left and move
                self.MoveLeftStep()
            elif pix == Colors.A_Fire:
                self.isAlive = False
            else:
                if pix == Colors.A_Crazy:
                    self.lifeSpan -= 1
                    if(self.lifeSpan <= 0):
                        self.isAlive = False
                # set current tile to white
                Ant.updateArray.append(pygame.Rect(self.x,self.y,1,1))
                self.display.fill(Colors.A_black, ((self.x,self.y), (1,1)))
                # turn right and move
                self.MoveRightStep()
            
            

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
    """Randomly moves about placing down water as it goes"""
    def __init__(self, x, y, box, facing, display, step=(1,1,1,1), speed=0):
        super().__init__(x, y, box, facing, display, step, speed)

    def Update(self, AutoUpdate=True):
        """Moves in a random direction if not on a white square"""
        if self.isAlive and AutoUpdate:
             Ant.antArray.append(self)
        self.TicksLeft -= 1
        if self.TicksLeft <= 0:
            self.TicksLeft = self.speedScalar-self.speed
            pix = self.display.get_at((self.x,self.y))
            if pix == Colors.A_white or pix == Colors.A_Fire or pix == Colors.A_Plant or pix == Colors.A_Zombie:
                Ant.updateArray.append(pygame.Rect(self.x,self.y,1,1))
                self.display.fill(Colors.A_Water, ((self.x,self.y), (1,1)))
                self.MoveLeftStep()
            else:
                if pix == Colors.A_Crazy:
                    self.lifeSpan -= 1
                    if(self.lifeSpan <= 0):
                        self.isAlive = False
                    Ant.updateArray.append(pygame.Rect(self.x,self.y,1,1))
                    self.display.fill(Colors.A_Water, ((self.x,self.y), (1,1)))
                self.MoveRandom()

    def Spawn(self):
        """Spawns ant in game and turns the current mouse pos to color of ant"""
        if len(Ant.antArray) < Ant.antLimit:
            Ant.antArray.append(self)
            self.display.set_at((self.x,self.y), Colors.A_Water)
            pygame.display.update(pygame.Rect(self.x,self.y,1,1))

#####################################################################################################################################################################
class AntWood(Ant):
    """Ant that will leave its trail only with-in a water ant's trail."""
    def __init__(self, x, y, box, facing, display, step=(1,1,1,1), speed=0):
        super().__init__(x, y, box, facing, display, step, speed)
        self.speedScalar += 150

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
            if pix == Colors.A_Water:
                randBlue.append(i)
            elif pix == Colors.A_Wood:
                randBrown.append(i)
            elif pix == Colors.A_Fire or pix == Colors.A_Crazy:
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


    def Update(self, AutoUpdate=True):
        """Turns blue pixels to brown and fills any connected blue squares to brown"""
        if self.isAlive and AutoUpdate:
             Ant.antArray.append(self)
        self.TicksLeft -= 1
        if self.TicksLeft <= 0:
            self.TicksLeft = self.speedScalar-self.speed
            pix = self.display.get_at((self.x,self.y))
            if pix == Colors.A_Water:
                Ant.updateArray.append(pygame.Rect(self.x,self.y,1,1))
                self.display.fill(Colors.A_Wood, ((self.x,self.y), (1,1)))
                self.Grow()
            self.Grow()


    def Spawn(self):
        """Spawns ant in game and turns the current mouse pos to color of ant"""
        if len(Ant.antArray) < Ant.antLimit:
            Ant.antArray.append(self)
            self.display.set_at((self.x,self.y), Colors.A_Wood)
            pygame.display.update(pygame.Rect(self.x,self.y,1,1))

#####################################################################################################################################################################
class AntFire(Ant):
    """Kills any ant that touches its path. Will die on contact of water"""
    def __init__(self, x, y, box, facing, display, step=(1,1,1,1), speed=0):
        super().__init__(x, y, box, facing, display, step, speed)
        self.speedScalar += 30

    def Update(self, AutoUpdate=True):
        if self.isAlive and AutoUpdate:
             Ant.antArray.append(self)
        self.TicksLeft -= 1
        if self.TicksLeft <= 0:
            self.TicksLeft = self.speedScalar-self.speed
            pix = self.display.get_at((self.x,self.y))
            if pix == Colors.A_Water:
                self.isAlive = False
            else:
                if pix == Colors.A_Crazy:
                    self.lifeSpan -= 1
                    if(self.lifeSpan <= 0):
                        self.isAlive = False
                Ant.updateArray.append(pygame.Rect(self.x,self.y,1,1))
                self.display.fill(Colors.A_Fire, ((self.x,self.y), (1,1)))

                # The following lines of code make an ant move in a spiral like pattern"""
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
        if len(Ant.antArray) < Ant.antLimit:
            Ant.antArray.append(self)
            self.display.set_at((self.x,self.y), Colors.A_Fire)
            pygame.display.update(pygame.Rect(self.x,self.y,1,1))


#####################################################################################################################################################################
class AntPlant(Ant):
    """Ant that will leave its trail only with-in a water ant's trail. 
    A water ant can overwrite the trail of the plant ant"""
    def __init__(self, x, y, box, facing, display, step=(1,1,1,1), speed=0):
        super().__init__(x, y, box, facing, display, step, speed)
        self.speedScalar += 25

    def Grow(self):
        """Ant will only stay on connected blue areas and will turn blue to green"""
        oldx = self.x
        oldy = self.y
        randBlue = []
        randGreen = []

        # Randomly move around
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
            if pix == Colors.A_Water:
                randBlue.append(i)
            elif pix == Colors.A_Plant:
                randGreen.append(i)
            elif pix == Colors.A_Fire:
                self.isAlive = False
            elif pix == Colors.A_Crazy:
                self.isAlive = False
            self.x = oldx
            self.y = oldy
        
        # Move to any water spaces else try to move to a green space. If all fails, don't move
        if len(randBlue) != 0:
            r = random.randint(0,len(randBlue)-1)
            self.facing = randBlue[r]
            self.MoveCurrentSpace()
        elif len(randGreen) != 0:
            r = random.randint(0,len(randGreen)-1)
            self.facing = randGreen[r]
            self.MoveCurrentSpace()


    def Update(self, AutoUpdate=True):
        """Turns blue pixels to green and fills any connected blue squares to green"""
        if self.isAlive and AutoUpdate:
             Ant.antArray.append(self)
        self.TicksLeft -= 1
        if self.TicksLeft <= 0:
            self.TicksLeft = self.speedScalar-self.speed
            pix = self.display.get_at((self.x,self.y))
            if pix == Colors.A_blue:
                Ant.updateArray.append(pygame.Rect(self.x,self.y,1,1))
                self.display.fill(Colors.A_Plant, ((self.x,self.y), (1,1)))
            self.Grow()
            


    def Spawn(self):
        """Spawns ant in game and turns the current mouse pos to color of ant"""
        if len(Ant.antArray) < Ant.antLimit:
            Ant.antArray.append(self)
            self.display.set_at((self.x,self.y), Colors.A_Plant)
            pygame.display.update(pygame.Rect(self.x,self.y,1,1))


#####################################################################################################################################################################
class AntZombie(Ant):
    """Ant that starts off purple but then turns to the color of the first non 
    white/purple place it runs into. The ant then turns into that type of ant and
     begins to move and behave just like the new ant. After an x number of steps 
     the ant will randomly generate 4 ants of that type around itself. Once a zombie ant
      converts it cannot convert again and will die."""

    def __init__(self, x, y, box, facing, display, step=(1,1,1,1), speed=0):
        super().__init__(x, y, box, facing, display, step, speed)
        self.speedScalar += 200
        self.zombieStage = 0 #0=looking for host type, 1=Found host type, 2=Fired spreading now a normal ant
        self.antType = None
        self.hostAntSpeed = Ant.maxSpeed
        self.firstAnt = None
        self.miliLeft = 2000 # number of miliseconds that the zombie ant will wait to spawn 4 ants
        self.preTicks = pygame.time.get_ticks()


    def Update(self, AutoUpdate=True):
        if self.isAlive and AutoUpdate:
             Ant.antArray.append(self)
        self.TicksLeft -= 1
        if self.TicksLeft <= 0:
            self.TicksLeft = self.speedScalar-self.speed
            pix = self.display.get_at((self.x,self.y))
            if self.zombieStage == 0 and (pix == Colors.A_white or pix == Colors.A_Zombie or pix == Colors.A_Crazy):
                # Ant zombie is looking for a host
                Ant.updateArray.append(pygame.Rect(self.x,self.y,1,1))
                self.display.fill(Colors.A_Zombie, ((self.x,self.y), (1,1)))
                if pix == Colors.A_Crazy:
                    self.lifeSpan -= 1
                    if(self.lifeSpan <= 0):
                        self.isAlive = False
                # turn left and move
                self.MoveZombie()
            elif self.zombieStage == 0:
                self.speed = 1
                # Ant is now a zombie and found a host type
                self.zombieStage = 1
                if pix == Colors.A_Water:
                    self.hostAntSpeed = Ant.maxSpeed
                    self.antType = AntWater
                elif pix == Colors.A_Fire:
                    self.hostAntSpeed = Ant.maxSpeed
                    self.antType = AntFire
                elif pix == Colors.A_Plant:
                    self.hostAntSpeed = Ant.maxSpeed
                    self.antType = AntPlant
                elif pix == Colors.A_Wood:
                    self.hostAntSpeed = Ant.maxSpeed
                    self.antType = AntWood
                elif pix == Colors.A_black:
                    self.hostAntSpeed = Ant.maxSpeed
                    self.antType = Ant

                if self.antType != None:
                    newStep = (self.stepUp,self.stepDown,self.stepLeft,self.stepRight)
                    self.speed = self.hostAntSpeed
                    self.firstAnt = self.antType(self.x,self.y,self.box,self.facing,self.display,newStep,self.hostAntSpeed)
                self.preTicks = pygame.time.get_ticks()
            elif self.zombieStage == 1:
                # Ant moves like the host ant until its life is over then it spawns 4 more similar ants
                if self.miliLeft <= 0:
                    self.isAlive = False
                    self.zombieStage = 2

                    # The following lines of code spawn in 1 ant to replace the zombie ant
                    # Then spawn 4 ants around the center of the first ant
                    newStep = (self.stepUp,self.stepDown,self.stepLeft,self.stepRight)
                    radius = 5 #Square Raduis of the other ants spawn location
                    self.firstAnt.Update()
                    Ant.antArray.append(self.antType(self.x+radius,self.y,self.box,self.facing,self.display,newStep,self.hostAntSpeed))
                    Ant.antArray.append(self.antType(self.x,self.y+radius,self.box,self.facing,self.display,newStep,self.hostAntSpeed))
                    Ant.antArray.append(self.antType(self.x,self.y-radius*2,self.box,self.facing,self.display,newStep,self.hostAntSpeed))
                    Ant.antArray.append(self.antType(self.x-radius*2,self.y,self.box,self.facing,self.display,newStep,self.hostAntSpeed))
                else:
                    gTicks = pygame.time.get_ticks()
                    self.miliLeft -= (gTicks - self.preTicks)
                    self.firstAnt.Update(False)
                    self.preTicks = gTicks
                    

    def Spawn(self):
        """Spawns ant in game and turns the current mouse pos to color of ant"""
        if len(Ant.antArray) < Ant.antLimit:
            Ant.antArray.append(self)
            self.facing = random.randint(0,3)
            self.display.set_at((self.x,self.y), Colors.A_Zombie)
            pygame.display.update(pygame.Rect(self.x,self.y,1,1))



#####################################################################################################################################################################
class AntCrazy(Ant):
    """Randomly moves about killing everything in its way"""
    def __init__(self, x, y, box, facing, display, step=(1,1,1,1), speed=0):
        super().__init__(x, y, box, facing, display, step, speed)
        self.lifeSpan = 10000 #Number of times ant can use its acid

    def Update(self, AutoUpdate=True):
        """Moves in a random direction"""
        if self.isAlive and AutoUpdate:
             Ant.antArray.append(self)
        self.TicksLeft -= 1
        if self.TicksLeft <= 0:
            self.TicksLeft = self.speedScalar-self.speed
            pix = self.display.get_at((self.x,self.y))

            #If ant is not on its own path or white, use its acid
            if pix == Colors.A_white:
                Ant.updateArray.append(pygame.Rect(self.x,self.y,1,1))
                self.display.fill(Colors.A_Crazy, ((self.x,self.y), (1,1)))
            elif not pix == Colors.A_Crazy:
                Ant.updateArray.append(pygame.Rect(self.x,self.y,1,1))
                self.display.fill(Colors.A_white, ((self.x,self.y), (1,1)))
                self.lifeSpan -= 1
                if(self.lifeSpan <= 0):
                    self.isAlive = False
            self.MoveRandom()

    def Spawn(self):
        """Spawns ant in game and turns the current mouse pos to color of ant"""
        if len(Ant.antArray) < Ant.antLimit:
            Ant.antArray.append(self)
            self.display.set_at((self.x,self.y), Colors.A_Crazy)
            pygame.display.update(pygame.Rect(self.x,self.y,1,1))