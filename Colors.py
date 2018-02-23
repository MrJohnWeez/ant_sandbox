
# Class defines common colors

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

#convert screen color to rgb value
def toColor(in_Color):
    return (in_Color//(256*256), in_Color//256%256, in_Color%256)