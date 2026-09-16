
## Color definitions

Colors = {

    "WHITE"    : (255, 255, 255),
    "BLACK"    : (0, 0, 0),
    "RED"      : (255, 0, 0),
    "GREEN"    : (0, 255, 0),
    "BLUE"     : (0, 0, 255),
    "YELLOW"   : (255, 255, 0),
    "CYAN"     : (0, 255, 255),
    "MAGENTA"  : (255, 0, 255),
    "LIME"     : (50, 205, 50),
    "ORANGE"   : (255, 165, 0),
    "PURPLE"   : (128, 0, 128),
    "NAVY"     : (0, 0, 128),
    "MAROON"   : (128, 0, 0),
    "TEAL"     : (0, 128, 128),
    "GOLD"     : (255, 215, 0),
    "PINK"     : (255, 192, 203),
    "SKY_BLUE" : (135, 206, 235),
    "VIOLET"   : (238, 130, 238),
    "LIGHT_GREY" : (100, 100, 100)
}

## Utility functions

ColorNames = {v: k for k, v in Colors.items()}

def getColorName(Color): ## Color kan `n tuple of `n list wees
    return ColorNames.get(tuple(Color))



## Tests debugging
## print(getColorName([0, 128, 128]))
## input()
