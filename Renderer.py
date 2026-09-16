from PIL import Image
from ursina import Entity, Texture, mouse

## My renderer just uses Ursina for letting me put pixels on the screen,
## All of the rendering capabilities I have implemented myself

## Hierdie is die dimesnsions van die "effective pixels" wat ek kan render ->
## Die design van die program is dat die Window dimensions = 1200 x 676,
## Maar die effective rendering size is net 600 x 338.
## Hierdie hou performance baie hoog, terwyl die actual window nie te klein op die screen is nie
## Lets name the 600 x 338 the EFFFontImageWidthIDTH, and EFF_HEIGHT (eff = effective)


## `n Paar Design Choices ->
## As jy 'n Top-menu bar wil he, doen dit met die PrintString wat Bo-op
## 'n LIGHT_GRAY rectangle is aan due bokant van jou screen
## Dit is in Ursina met my eie graphics Lib
## Maar SODRA jy klik op een van die opsies bv. "File" of "Options",
## Maak ASB dadelik `n nuwe venster oop met TKinter  (400x400)
## 'n Nuwe OS-venster — 'n aparte blokkie op jou taskbar, met sy eie titelbalk, wat jy kan rondskuif

EFF_WIDTH = 600
EFF_HEIGHT = 338

WIN_WIDTH = 1000
WIN_HEIGHT = 563

FOV = 9 ## Ursina distinguishes between "World scale" and "Screen scale". FOV of 9 just makes
## sure that our "img" is rendered on the full window Width and Height

# Pixel buffer (RAM)
## Ons begin deur die hele pixelBuffer swart te maak


## Hierdie is Die image wat die hele screen se texture hou
img = Image.new('RGBA', (EFF_WIDTH, EFF_HEIGHT), (0, 0, 0, 255))

## Die Screen variable in die main Program gaan hierdie aanvaar
def NewScreen():

    return Entity(
        model='quad',
        texture=Texture(img),
        scale=(16,9), ## Because 600 x 338 is 16:9, combined with the FOV of 9 , makes my program
        ## Actually render "full-window"
        z=0
    )



def ClearBuff():
    ## Maak die hele framebuffer swart, in die "img" wat die screen image variable is
    img.paste((0, 0, 0, 255), [0, 0, EFF_WIDTH, EFF_HEIGHT])


def DrawPixelInBuff(x, y, color):
    ## Teken 'n enkele pixel in die framebuffer
    ## Ons alter die "img" / Framebuffer variable deur individual pixels te oorskryf met putpixel
    if 0 <= x < EFF_WIDTH and 0 <= y < EFF_HEIGHT:
        img.putpixel((x, EFF_HEIGHT - y - 1), color)



def DrawRectInBuff(TopLeftX, TopLeftY, XExtends, YExtends, color):
    ## Ons kan `n reghoek maak as ons repeatedly die DrawPixelInBuff() roep
    BottomLeftY = TopLeftY - YExtends ## Die Parameter is "TopLeftY", maar Die for loops
    ## werk van die bottom-left aan, want range() + die heeltyd 1, nie -1 nie.
    ## Vir x is dit fine, maar vir Y beteken dit dit gaan die Bottom-left wees
    for y in range(YExtends):
        for x in range(XExtends):
            DrawPixelInBuff(TopLeftX + x, BottomLeftY + y, color)


def DrawCircleInBuff(cx, cy, r, color):

    ## Teken 'n gevulde sirkel met:
    ## - Midpoint Circle Algorithm
    ## - 8-way symmetry
    ## - Horisontale scanlines

    x = r
    y = 0
    d = 1 - r

    while x >= y:

        ## 8-Way simmetries

        ## Teken 'n horisontale lyn deur die boonste en onderste
        ## helftes van die sirkel met die huidige x-waarde.
        for ix in range(cx - x, cx + x + 1):
            DrawPixelInBuff(ix, cy + y, color)
            DrawPixelInBuff(ix, cy - y, color)

        ## Gebruik dieselfde simmetrie, maar wissel x en y om.
        ## Dit vul die linker en regter dele van die sirkel
        for ix in range(cx - y, cx + y + 1):
            DrawPixelInBuff(ix, cy + x, color)
            DrawPixelInBuff(ix, cy - x, color)


        ## Beweeg na die volgende punt in die Midpoint-algoritme.
        y += 1


        ## Bepaal of x dieselfde moet bly of met 1 verminder.
        if d <= 0:
            d += 2 * y + 1
        else:
            x -= 1
            d += 2 * (y - x) + 1


def UpdateScreen():
    ## Gee 'n Texture-compatibele PIL -> bytes -> image terug
    return Texture(Image.frombytes('RGBA', (EFF_WIDTH, EFF_HEIGHT), img.tobytes()))


def XCoordToScreen(Px): ## Hierdie is `n Helper function, Intern in die renderer is
    ## die 0, 0 (Oorsprong) by Bottom-left, maar In Main.py gebruik ek die 4-kwadrant
    ## approach waar 0, 0 in die middel van die skerm is
    return Px + EFF_WIDTH // 2

def YCoordToScreen(Py):
    ## Dieselfde as vir die XCoordToScreen funksie, net met Height
    return Py + EFF_HEIGHT // 2


# Font loading
# Load the font image once when this module is imported.
#
# The font.png image contains a 16x16 grid of characters.
# Each character occupies a 9x9 cell:
#
#   - 8x8 pixels  -> actual glyph
#   - 1 pixel      -> spacing/border around the glyph
#
# This means the entire font image is 144x144 pixels.
# ============================================================

FontImage = Image.open("font.png").convert("RGB")

# Store the width so we don't have to repeatedly access
# FontImage.width while reading individual pixels.
FontImageWidth = FontImage.width

# Convert the image into a flat list of RGB pixel tuples.
#
# Instead of doing:
#     FontImage.getpixel((x, y))
#
# we can calculate the pixel's index directly:
#     y * FontImageWidth + x
#
# This avoids repeatedly calling getpixel() while rendering text.
FontImagePixels = list(FontImage.getdata())


# Cache previously decoded characters.
#
# GetGlyph() converts a character from the font image into
# eight 8-bit rows. Once a character has been decoded, there
# is no reason to decode it again.
Cache = {}


def GetGlyph(char):
    """
    Convert a character into an 8x8 bitmap.

    The returned list contains 8 integers, one for each row.
    Each bit in an integer represents one pixel:

        1 = pixel should be drawn
        0 = pixel should be skipped

    Example:
        10011000
        10011000
        10011000
        11111111
        ...
    """

    # Check whether this character has already been decoded.
    # If it has, return the cached bitmap immediately.
    m = Cache.get(char)

    if m is not None:
        return m

    # Convert the character into its numeric character code.
    #
    # The font is based on the first 256 character codes.
    # Characters outside that range are replaced with '?'.
    code = ord(char) if ord(char) <= 255 else ord('?')

    # Convert the character code into its position in the
    # 16x16 character grid.
    #
    # For example:
    #     code = 65 ('A')
    #
    #     65 / 16 -> row 4
    #     65 % 16 -> column 1
    #
    # divmod() gives us both values at once.
    fr, fc = divmod(code, 16)

    # This will contain the 8 bitmap rows for the character.
    rows = []

    # Read all 8 rows of the glyph.
    for row in range(8):

        # Each bit of this integer represents one pixel
        # in the current row.
        bits = 0

        # Read all 8 pixels across the glyph.
        for col in range(8):

            # Each character occupies a 9x9 cell in the
            # font image, with the actual 8x8 glyph starting
            # one pixel in from the top-left corner.
            #
            # The +1 skips that border/spacing pixel.
            x = fc * 9 + col + 1
            y = fr * 9 + row + 1

            # Get the RGB value of this font pixel.
            r, g, b = FontImagePixels[y * FontImageWidth + x]

            # Treat bright pixels in the font image as
            # characters and dark pixels as empty space.
            if r + g + b > 128:

                # Set the corresponding bit for this pixel.
                #
                # 7 - col means the first pixel occupies
                # the most-significant bit:
                #
                # col 0 -> bit 7
                # col 7 -> bit 0
                bits |= 1 << (7 - col)

        # Store this completed row.
        rows.append(bits)

    # Save the decoded glyph so the next time this character
    # is requested we can skip all of the image processing.
    Cache[char] = rows

    return rows


def PrintString(Screenx, Screeny, text, spacing=8, color=(255, 255, 255)):
    """
    Draw a string to the framebuffer using the custom font.

    Screenx and Screeny specify the starting position.
    'spacing' controls the horizontal distance between characters.
    """

    # Adjust the starting Y position because the glyph is
    # rendered relative to its lower edge in the framebuffer, and the function expects the "Screen" as the top-left coordinates instead of bottom-left,
    # which is used internally in the function.
    Screeny -= 9

    # Current X position of the character being rendered.
    cx = Screenx

    # Render every character in the string.
    for char in text:

        # Handle newline characters separately.
        #
        # Move back to the original X position and move down
        # by one character height plus one pixel of spacing.
        if char == '\n':
            cx = Screenx
            Screeny += spacing + 1
            continue

        # Convert the character into its 8x8 bitmap.
        rows = GetGlyph(char)

        # Render each of the 8 bitmap rows.
        for row in range(8):

            # Get the bit pattern for this row.
            bits = rows[row]

            # If the entire row is empty, there is nothing
            # to draw, so skip it.
            if not bits:
                continue

            # Convert the font row into the framebuffer's
            # coordinate system.
            sy = Screeny + (8 - row)

            # Check every pixel in this row.
            for col in range(8):

                # Test whether the bit corresponding to this
                # pixel is set.
                if bits & (1 << (7 - col)):

                    # The bit is set, so draw this pixel.
                    DrawPixelInBuff(
                        cx + col,
                        sy,
                        color
                    )

        # Move to the starting X position of the next character.
        cx += spacing

def GetMousePosition():
    ## Die funksie return die mouse position, waar 0,0 By bottom-left corner van
    ## Die skerm is. As EFF_WIDTH nog = 600 en EFF_HEIGHT nog = 338, dan is die max
    ## values 600 en 338.

    MouseX = int((((mouse.x + 0.5) * EFF_WIDTH) + 232) // 1.7717)
    ## +232 was needed because Ursina processed "232" as "0", and (0, 0) as -232, 0
    ## Then then I moved the mouse to the top Right Ursina Processed it as (1063, 338)
    ## while the max value is just 600, 338.

    ## I think The +232 was needed because Ursina processes the mouse coordinates as a SQUARE
    ## Meaning, starting at the center of the screen, if you move the mouse x amount of pixels
    ## you will land at the Max Y value, but if you instead move left that same amount of pixels you wil get 0 at X
    ## But obviously the screen is not square, so thats why I need the +232

    ## // 1.7717 is also the approx. ratio of 16 / 9.

    MouseY = int((mouse.y + 0.5) * EFF_HEIGHT)

    return [MouseX - EFF_WIDTH, MouseY - EFF_HEIGHT] ## Return the mouse position in the 4-quadrant system, where 0,0 is in the middle of the screen

def GetMouseClicked():
    ## Returns True if the mouse is clicked, False otherwise
    return mouse.left
