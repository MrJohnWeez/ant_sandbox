# Class defines common colors
import pygame
AAA = (255,255,255,0)
#Colors with Alpha
A_white = (255,255,255,255)
A_black = (0,0,0,255)
A_red = (255,0,0,255)
A_green = (0,255,0,255) #very light green
A_blue = (0,0,255,255)
A_RichGreen = (33, 160, 69, 255) #darker saturated green
A_RichBlueGreen = (33, 175, 171, 255) #Blue green

A_Water = (0,0,255,255)
A_Fire = (237, 48, 15,255) #Orange Red
A_Wood = (119, 77, 0,255) #Brown
A_Zombie = (142, 9, 232,255) #Purple
A_Plant = (0,255,0,255) #Green
A_Crazy = (233, 237, 42,255) #Yellow

A_optionsBg = (48, 48, 48,255)
A_clearA = (170, 100, 100,255)
A_clearN = (130, 84, 84,255)

#Colors without Alpha
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

optionsBg = (48, 48, 48)
clearA = (170, 100, 100)
clearN = (130, 84, 84)

def clamp(n, smallest, largest): return max(smallest, min(n, largest))
    
#convert screen color to rgb value
def toColor(in_Color):
    """Convert color to a single interger"""
    return (in_Color//(256*256), in_Color//256%256, in_Color%256)

def shadeAlpha(inColor, shade_factor):
    """Returns a shade given a base color with the alpha channel
    shadeFactor: (1 to -1) Negative = Darker, Positive = Lighter
    """
    assert 1 >= shade_factor >= -1
    if shade_factor < 0:
        shade_factor *= -1
        newR = inColor[0] * (1- shade_factor)
        newG = inColor[1] * (1- shade_factor)
        newB = inColor[2] * (1- shade_factor)
    else:
        newR = inColor[0] + ((255 - inColor[0]) * shade_factor)
        newG = inColor[1] + ((255 - inColor[1]) * shade_factor)
        newB = inColor[2] + ((255 - inColor[2]) * shade_factor)
    newR = clamp(newR,0,255)
    newG = clamp(newG,0,255)
    newB = clamp(newB,0,255)
    return (newR,newG,newB,inColor[3])

def shade(inColor, shade_factor):
    """Returns a shade given a base color
    shadeFactor: (1 to -1) Negative = Darker, Positive = Lighter
    """
    assert 1 >= shade_factor >= -1
    if shade_factor < 0:
        shade_factor *= -1
        newR = inColor[0] * (1- shade_factor)
        newG = inColor[1] * (1- shade_factor)
        newB = inColor[2] * (1- shade_factor)
    else:
        newR = inColor[0] + ((255 - inColor[0]) * shade_factor)
        newG = inColor[1] + ((255 - inColor[1]) * shade_factor)
        newB = inColor[2] + ((255 - inColor[2]) * shade_factor)
    newR = clamp(newR,0,255)
    newG = clamp(newG,0,255)
    newB = clamp(newB,0,255)
    return (newR,newG,newB)


#From: https://www.pygame.org/wiki/GradientCode
def fill_gradient(surface, color, gradient, rect=None, vertical=True, forward=True):
    """fill a surface with a gradient pattern
    Parameters:
    color -> starting color
    gradient -> final color
    rect -> area to fill; default is surface's rect
    vertical -> True=vertical; False=horizontal
    forward -> True=forward; False=reverse
    """
    
    if rect is None: rect = surface.get_rect()
    x1,x2 = rect.left, rect.right
    y1,y2 = rect.top, rect.bottom
    if vertical: h = y2-y1
    else:        h = x2-x1
    if forward: a, b = color, gradient
    else:       b, a = color, gradient
    rate = (
        float(b[0]-a[0])/h,
        float(b[1]-a[1])/h,
        float(b[2]-a[2])/h
    )
    fn_line = pygame.draw.line
    if vertical:
        for line in range(y1,y2):
            color = (
                min(max(a[0]+(rate[0]*(line-y1)),0),255),
                min(max(a[1]+(rate[1]*(line-y1)),0),255),
                min(max(a[2]+(rate[2]*(line-y1)),0),255)
            )
            fn_line(surface, color, (x1,line), (x2,line))
    else:
        for col in range(x1,x2):
            color = (
                min(max(a[0]+(rate[0]*(col-x1)),0),255),
                min(max(a[1]+(rate[1]*(col-x1)),0),255),
                min(max(a[2]+(rate[2]*(col-x1)),0),255)
            )
            fn_line(surface, color, (col,y1), (col,y2))