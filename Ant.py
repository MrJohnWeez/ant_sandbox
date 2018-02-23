class Ant:
    def __init__(self, inx, iny, inleft, intop, inwidth, inheight, infacing):
        self.width = inwidth
        self.height = inheight
        self.left = inleft
        self.top = intop
        self.x = inx
        self.y = iny
        self.facing = infacing # 0 = up, 1 = right, 2 = down, 3 = left


    def __get_x(self):
        return self.__x

    def __set_x(self, x):
        if(x > self.width-1):
            x = self.left
        if(x < self.left):
            x = self.width-1
        self.__x = x

    x = property(__get_x, __set_x)

    def __get_y(self):
        return self.__y


    def __set_y(self, y):
        if(y > self.height-1):
            y = self.top
        if(y < self.top):
            y = self.height-1
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