import codecs
import itertools
import math
import os
import random
import sys

from PIL import Image

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BORDER = WHITE
COLOURS = [RED, GREEN, BLUE]

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'treasure_hunt_2.png')

im = Image.open(filename)

midx = im.size[0] // 2
midy = im.size[1] // 2

count = 0
hits = {}  # dictionary of positions and pixel values
validborders = [BORDER]  # valid outer border colours, white to grey
for i in range(1, 6):
    validborders.append(tuple(i // 2 for i in validborders[-1]))

for y in range(im.size[1]):
    for x in range(im.size[0]):
        # find all the coloured squares, record them into hits
        if all(im.getpixel((xx, yy)) in validborders for xx in range(x, x+10) for yy in range(y, y+10) if xx == x or xx == x + 9 or yy == y or yy == y + 9):
            if any(im.getpixel((xx, yy)) not in [RED, GREEN, BLUE] for xx in range(x+1, x+9) for yy in range(y+1, y+9) if xx == x or xx == x + 8 or yy == y or yy == y + 8):
                continue
            count += 1
            # distance, squared
            r = (midx - x) * (midx - x) + (midy - y) * (midy - y)
            # this returns the index of the first channel whose value is 255
            channel = [i for i, v in enumerate(im.getpixel((x+1, y+1))) if v == 255][0]
            # key is the index of the colour, starting with WHITE, followed by distance.
            # when these are sorted, the white bordered squares will be first.
            key = (validborders.index(im.getpixel((x, y))), r)
            hits[key] = (im.getpixel((x+2, y+2))[channel])

data = b""

# sort the keys by distance from mid-point, and then write out the encoded pixel value
for k in sorted(hits.keys()):
    val = hits[k]
    data += bytes([val])
    sys.stdout.write(chr(val))


print(f"\n\nlen(data): {len(data)}.")

with open("treasure_hunt_2.bin", "wb") as f:
    f.write(data)

data = data[data.index(b"###"):]

data = data.strip(b"#")

print("\n\n\n%s\n\n" % ("*" * 80))

print(codecs.decode(data, "zip").decode("utf-8"))
