from pynput.mouse import Button, Controller
from numpy import *
from PIL import ImageGrab, ImageOps, Image
import os
import time
import random
import mss
import mss.tools

"""
https://www.silvergames.com/en/piano-tiles
All coordinates assume a screen resolution of 1440x900, and Chrome 
sized to 720x730 to the right with the Bookmarks Toolbar disabled.
The down key is pressed twice.

Play area  = Offset.x + 1, Offset.y + 1, 1275, 800
"""
class Offset:
    # coordinates to top left corner of play area
    x = 854
    y = 100

    # coordinates of the start button
    start_x = 156
    start_y = 438

    tile_y = 423

class Box:
    one = 856
    two = 961
    three = 1066
    four = 1171

class Tile:
    pass
# -----------------------------------------------
# Globals
# -----------------------------------------------
mouse = Controller()

tile_width = 102
tile_height = 25

black_tile_threshold = 10750
tile_red_val_thresh = 100

tile_coords = [(46, 380), (162, 380), (261, 380), (374, 380)]

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
    with mss.mss() as sct:
        # The screen part to capture
        screen = {"top": Offset.y + 1, "left": Offset.x + 1, "width": 421, "height": 700}
        im = sct.grab(screen)

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
    return (coord[0], coord[1] + 120)
# -----------------------------------------------
# Main
# -----------------------------------------------
def check_tiles_slow():
    box_1 = box_PIL(Box.one, Offset.tile_y, Box.one + tile_width, Offset.tile_y + tile_height)
    box_2 = box_PIL(Box.two, Offset.tile_y, Box.two + tile_width, Offset.tile_y + tile_height)
    box_3 = box_PIL(Box.three, Offset.tile_y, Box.three + tile_width, Offset.tile_y + tile_height)
    box_4 = box_PIL(Box.four, Offset.tile_y, Box.four + tile_width, Offset.tile_y + tile_height)
    
    return (value(box_1), value(box_2), value(box_3), value(box_4))

def check_tiles():
    im = screenshot()
    tiles = [im.getpixel(coord_PIL(tile_coords[i])) for i in range(4)]

    for i in range(4):
        tile = tiles[i]
        if (tile[0] < tile_red_val_thresh):
            move(lag(tile_coords[i]))
            leftClick(1)


def start_game():
    move((Offset.start_x, Offset.start_y))
    leftClick(2)

def main():
    # start_game()

    i = 0
    while i < 500:
        i += 1
        tiles = check_tiles()
        time.sleep(0.1)

if __name__ == '__main__':
    main()
