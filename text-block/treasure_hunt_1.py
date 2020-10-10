# Level 4 unlocked! The code to generate the treasure hunt is laid bare!
import itertools
import os
import random
import string

import PIL
from PIL import Image, ImageDraw, ImageFont

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

WIDTH = 200
HEIGHT = 200
SPACING = 10
STARTX = (WIDTH - SPACING * 16) / 2
STARTY = (HEIGHT - SPACING * 16) / 2

LEVEL_1 = "Level 1 unlocked! The key is mosaic. Hail, Caesar!"
# "Level 2 unlocked! Look carefully at the pixel colours. Python pillow may help."
LEVEL_2 = "Hivih 2 ukhlsgia! Hllg smqicuhhy mt tdi nexih slhluqr. Nytdlk nehhlw jmy dihn."
LEVEL_3 = "Level 3 unlocked! Congratulations, you win! Unless there's a secret level 4? If there is... you may need to XOR with 'level4secretunlockcode'"

LEVEL_3 += "!" * (256 - len(LEVEL_3))

font = ImageFont.load_default()
img = Image.new("RGBA", (WIDTH, HEIGHT), BLACK)
draw = ImageDraw.Draw(img)
draw.fontmode = "1"  # this sets anti-aliasing off.

message = LEVEL_1 + LEVEL_2
hexes = "".join(hex(ord(i))[2:] for i in message)
chars = hexes


def encode_as_colour(char, dark=False):
    char_value = ord(char)
    c = [255, 255, 255]
    if dark:
        c = [0, 0, 0]
    c[random.randint(0, 2)] = char_value
    return tuple(c)


for row in range(16):
    for col in range(16):
        i = row * 16 + col
        if i >= len(chars):
            break
        draw.text(
            (STARTX + col * SPACING, STARTY + row * SPACING),
            chars[i],
            encode_as_colour(LEVEL_3[i]),
            font=font,
        )
    if i >= len(chars):
        break

# make everything bigger. Pillow's font support isn't great so we do it this way.
img = img.resize((800, 800), resample=PIL.Image.NEAREST)

# for the final trick, read in the contents of this script and then write it out as pixels, starting in the top left corner.
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "treasure_hunt_1.py")
script = open(filename, "r").read()
# do a simple XOR on level 4 to prevent skipping levels :)
xor_script = ""
for i, c in enumerate(script):
    xor_script += chr(ord(c) ^ ord("level4secretunlockcode"[i % 22]))

script = "You're not ready for level 4 yet." + xor_script

for i, c in enumerate(script):
    colour = encode_as_colour(c, dark=True)
    img.putpixel((i % 800, i//800), colour)

img.save("treasure_hunt_1.png")
