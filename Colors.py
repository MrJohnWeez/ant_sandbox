"""Defines custom colors that can be used in pygame

Also gives user ablility to create dynamic
color shades of any color"""

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