from pynput.mouse import Button, Controller
from numpy import *
from PIL import ImageGrab, ImageOps, Image
import os
import time
import random
import mss
import mss.tools

"""
Piano Tiles bot for https://www.silvergames.com/en/piano-tiles

All coordinates assume a screen resolution of 1440x900, and Chrome 
sized to 720x730 to the right with the Bookmarks Toolbar disabled.
The down key is pressed twice.

To terminate the game, place a white screen behind it and move it to
the left of the screen.

Play area  = Offset.x + 1, Offset.y + 1, 1275, 800
"""
class Offset:
    # coordinates to top left corner of play area
    x = 854
    y = 100

class Tile:
    width = 102
    height = 25
    black_tile_thresh = 100
    coords = [(46, 380), (162, 380), (261, 380), (374, 380)]
    count = 4

# -----------------------------------------------
# Globals
# -----------------------------------------------
mouse = Controller()

screen_width = 421
screen_height = 700

lag_y = 70

# -----------------------------------------------
# Helper Functions
# -----------------------------------------------
# PIL appears to work with pixels of half size, hence the need to convert
# between pixels used by the mouse and pixels used by PIL
def coord_PIL(coord):
    return (2 * coord[0], 2 * coord[1])

def box_PIL(a, b, c, d):
    return (2 * a, 2 * b, 2 * c, 2 * d)

def screenshot(save = False):
    with mss.mss() as screen:
        # The screen part to capture
        play_area = {"top": Offset.y + 1, "left": Offset.x + 1, "width": screen_width, "height": screen_height}
        im = screen.grab(play_area)

        # Save image
        if save:
            path = os.getcwd() + '/snaps/snap__' + str(int(time.time())) + '.png'
            mss.tools.to_png(im.rgb, im.size, output=path)
        # Convert to PIL/Pillow Image
        return Image.frombytes('RGB', im.size, im.bgra, 'raw', 'BGRX')

def screenshot_slow(save = False):
    box = box_PIL(Offset.x + 1, Offset.y + 1, Offset.x + 421, Offset.y + 700)
    im = ImageGrab.grab(box)
    if save:
        path = os.getcwd() + '/snaps/snap__' + str(int(time.time())) + '.png'
        im.save(path, 'PNG')
    return im

def value(box, save = False):
    im = ImageGrab.grab(box)
    if save:
        path = os.getcwd() + '/snaps/snap__' + str(int(time.time())) + '.png'
        im.save(path, 'PNG')
    im_gray = ImageOps.grayscale(im)
    a = array(im_gray.getcolors())
    a = a.sum()
    if save:
        im_gray.save(os.getcwd() + '/snaps/grayscale__' + str(int(time.time())) + '.png', 'PNG')    
    return a

# -----------------------------------------------
# Mouse Controls
# -----------------------------------------------
def leftClick(n):
    mouse.click(Button.left, n)

def rightClick(n):
    mouse.click(Button.right, n)

def move(coord):
    x = Offset.x + coord[0]
    y = Offset.y + coord[1]
    mouse.position = (x, y)
    time.sleep(.02)

def getCoords():
    x, y = mouse.position
    x = x - Offset.x
    y = y - Offset.y
    print(x, y)
    return (x,y)

def lag(coord):
    return (coord[0], coord[1] + lag_y)

# -----------------------------------------------
# Main
# -----------------------------------------------
def check_tiles():
    move_made = False
    im = screenshot()
    tiles_rgb = [im.getpixel(coord_PIL(Tile.coords[i])) for i in range(Tile.count)]

    for i in range(Tile.count):
        tile_rgb = tiles_rgb[i]
        if (tile_rgb[0] < Tile.black_tile_thresh):
            move(lag(Tile.coords[i]))
            leftClick(1)
            move_made = True

    return move_made

def main():
    moves_unmade = 0
    while moves_unmade < 10:
        move_made = check_tiles()
        if not move_made:
            moves_unmade += 1
        else:
            moves_unmade = 0

if __name__ == '__main__':
    main()
