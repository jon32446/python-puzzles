import codecs
import math
import os
import random
import sys
from itertools import product

from PIL import Image

# heading hint, pointing to using zip (smallest thing, most information)
# Excerpts from The Tao of Programming
# ~the smallest thing may hold the most information~
# keyed caeser, key = rickastley. but with spaces replaced with x's to frustrate frequency analysis
heading = """AwcanjpowsnhfwPlawPrhwhswJnhtnrffegt
~plawofrddaopwplegtwfrxwlhdkwplawfhopwegshnfrpehg~
"""

tao = """
0x00
Thus spake the master programmer: Though a program be but three lines long, someday it will have
to be maintained.

0x2E
A manager went to the master programmer and showed him the requirements document for a new
application. The manager asked the master: "How long will it take to design this system if I assign
five programmers to it?"
"It will take one year," said the master promptly.
"But we need this system immediately or even sooner! How long will it take if I assign ten
programmers to it?"
The master programmer frowned. "In that case, it will take two years."
"And what if I assign a hundred programmers to it?"
The master programmer shrugged. "Then the design will never be completed," he said.

0x74
Thus spake the master programmer: A well-written program is its own heaven; a poorly-written program
is its own hell.

0xA1
A novice asked the master: "In the east there is a great tree-structure that men call 'Corporate
Headquarters'. It is bloated out of shape with vice-presidents and accountants. It issues a
multitude of memos, each saying 'Go, Hence!' or 'Go, Hither!' and nobody knows what is meant. Every
year new names are put onto the branches, but all to no avail. How can such an unnatural entity exist?"
The master replies: "You perceive this immense structure and are disturbed that it has no rational
purpose. Can you not take amusement from its endless gyrations? Do you not enjoy the untroubled ease
of programming beneath its sheltering branches? Why are you bothered by its uselessness?"

0xFF
Thus spake the master programmer: Time for you to get back to work.
"""

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BORDER = WHITE
COLOURS = [RED, GREEN, BLUE]

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'wallhaven-611809.jpg')

im = Image.open(filename)
im = im.resize((im.size[0] * 4 // 5, im.size[1] * 4 // 5))


def box(image, colour, left, top, right, bottom):
    """Draw an empty box of given dimensions and colour"""
    for pt in (i for i in product(range(left, right), range(top, bottom)) if i[0] in (left, right-1) or i[1] in (top, bottom-1)):
        image.putpixel(pt, colour)


def putchar(image, colour, left, top, right, bottom, char):
    """Draw a solid coloured box of given dimensions, encoding given character into one of the
    colour channels."""
    channel = [i for i, v in enumerate(colour) if v == 255][0]
    cypher = image.crop((left, top, right, bottom))
    channels = cypher.split()
    out = channels[channel].point(lambda x: char)
    channels[channel].paste(out)
    cypher = Image.merge(image.mode, channels)
    image.paste(cypher, (left, top, right, bottom))


def putcharandboxes(image, left, top, char):
    """Helper function to draw the two outer boxes and then the coloured inside square."""
    random_colour = COLOURS[random.randint(0, len(COLOURS)-1)]
    box(im, BORDER, left, top, left+10, top+10)
    box(im, random_colour, left+1, top+1, left+9, top+9)
    putchar(im, random_colour, left+2, top+2, left+8, top+8, char)


def gospiral(im, data, datai, a, b):
    """Generate a spiral arm in the given image, with co-efficients a and b going into the spiral
    formula. Returns how much of the data was encoded within this spiral arm. Should be called
    multiple times until all the data is encoded into spirals. Increase the 'a' co-efficient on
    each invocation."""
    midx = im.size[0] / 2
    midy = im.size[1] / 2
    i = 666  # for good luck
    while True:
        i += 15  # i is the distance. +15 is basically +15 pixels along the arc of the spiral
        # arc distance calc
        ii = math.log((i * b) / (a * math.sqrt(1 + math.pow(b, 2)))) / b
        # s = (a * math.sqrt(1 + math.pow(b, 2)) * math.exp(b * i))/b
        x = midx + a * math.exp(b * ii) * math.cos(ii)
        y = midy + a * math.exp(b * ii) * math.sin(ii)
        # fit in as much spiral as possible
        if x > 20 and x < im.size[0] - 20 and y > 20 and y < im.size[1] - 20:
            # print as much of the data as possible into this spiral
            putcharandboxes(im, int(x), int(y), data[datai] if datai < len(data) else ord("#"))
            datai += 1
        else:
            break
    return datai  # how far we got


# hint to display to the puzzler, and the rest of the data
data = b"""the following might help you decode the rest: youtu.be/dQw4w9WgXcQ
""" + heading.encode("utf-8") + b"###########" + codecs.encode(tao.encode("utf-8"), "zip")

# go through all the data and encode it into spiral arms
datai = 0
a = math.pi
while datai < len(data):
    datai = gospiral(im, data, datai, a, b=0.15)
    BORDER = tuple(i // 2 for i in BORDER)
    a += math.pi / 4

# save the result
im.save(r".\treasure_hunt_2.png")

# print out how much real data there is vs padding data
print(f"length of data: {len(data)}; length of data including padding: {datai}")  # 958 / 1092
