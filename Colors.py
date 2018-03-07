# Class defines common colors

#Colors with Alpha
A_white = (255,255,255,255)
A_black = (0,0,0,255)
A_red = (255,0,0,255)
A_green = (0,255,0,255)
A_blue = (0,0,255,255)

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

#convert screen color to rgb value
def toColor(in_Color):
    return (in_Color//(256*256), in_Color//256%256, in_Color%256)

def shadeAlpha(inColor, shade_factor):
    newR = inColor[0] * (1 - shade_factor)
    newG = inColor[1] * (1 - shade_factor)
    newB = inColor[2] * (1 - shade_factor)
    return (newR,newG,newB,inColor[3])

def shade(inColor, shade_factor):
    newR = inColor[0] * (1 - shade_factor)
    newG = inColor[1] * (1 - shade_factor)
    newB = inColor[2] * (1 - shade_factor)
    return (newR,newG,newB)

