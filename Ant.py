class Ant:
    def __init__(self, inx, iny, inboundx, inboundy, infacing):
        self.boundx = inboundx
        self.boundy = inboundy
        self.x = inx
        self.y = iny
        self.facing = infacing # 0 = up, 1 = right, 2 = down, 3 = left
        


    def __get_x(self):
        return self.__x

    def __set_x(self, x):
        if(x > self.boundx-1):
            x = 0
        if(x < 0):
            x = self.boundx-1
        self.__x = x

    x = property(__get_x, __set_x)

    def __get_y(self):
        return self.__y


    def __set_y(self, y):
        if(y > self.boundy-1):
            y = 0
        if(y < 0):
            y = self.boundy-1
        self.__y = y

    y = property(__get_y, __set_y)


    def move_black(self):
        if self.facing == 0:
            self.facing = 3
            self.x -= 1
        elif self.facing == 1:
            self.facing = 0
            self.y -= 1
        elif self.facing == 2:
            self.facing = 1
            self.x += 1
        elif self.facing == 3:
            self.facing = 2
            self.y += 1

    def move_white(self):
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