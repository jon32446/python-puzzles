import itertools
import random
import string
from functools import reduce

import PIL
from PIL import Image, ImageDraw, ImageFont

# block of letters
#
# numbers at top, each one is an index into the block, row-wise. these are general clues for the
# rest of the puzzle
#
# lastly, each letter is a colour. the colour will be 255 in all channels except 1, which will
# contain a byte value. these bytes are the final part of the puzzle.


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

WIDTH = 800
HEIGHT = 600
SPACING = 24
STARTX = (WIDTH - SPACING * 16) / 2
STARTY = (HEIGHT - SPACING * 16) / 2


# these appear at the top as numbers, and are indexes into the main block, row-wise
top_message = [
    "word search",
    "Vigenere",
    "rgbtobin"
]


def encode_vigenere(message, key="mosaic"):
    message = [ord(m) - ord("A") for m in message.upper() if m in string.ascii_uppercase]
    key = [ord(k) - ord("A") for k in key.upper() if k in string.ascii_uppercase]
    print(key, message)
    c = []
    for m, k in zip(message, itertools.cycle(key)):
        c.append((m + k) % 26)  # c = m + k mod 26
    print("".join(chr(ord("A") + i) for i in c))
    return "".join(chr(ord("A") + i) for i in c)


def decode_vigenere(cyphertext, key="mosaic"):
    cyphertext = [ord(m) - ord("A") for m in cyphertext.upper() if m in string.ascii_uppercase]
    key = [ord(k) - ord("A") for k in key.upper() if k in string.ascii_uppercase]
    print(key, cyphertext)
    m = []
    for c, k in zip(cyphertext, itertools.cycle(key)):
        m.append((c - k) % 26)  # m = c - k mod 26
    print("".join(chr(ord("A") + i) for i in m))
    return "".join(chr(ord("A") + i) for i in m)


# the block message must not exceed 256 chars - it will be truncated
block_message = "Paul sensed his own tensions decided to practice one of the mindbody lessons " \
    "his mother had taught him three quick breaths triggered the responses he fell into the " \
    "floating awareness focusing the consciousness aortal dilation avoiding the unfocused " \
    "mechanism of consciousness to be conscious by choice"
chars = "".join(i for i in block_message.upper() if i in string.ascii_uppercase)
if len(chars) < 256:
    chars += "".join(random.choice(string.ascii_uppercase) for i in range(256 - len(chars)))

hint = "MOSAICVIGENERECYPHER"
chars = encode_vigenere(chars)

# place a hint at the start to indicate that there are words in the block (word search)
chars = "HELLO" + chars

# place the decryption hint in plaintext in the middle of the chars after encoding it
midpoint = (16//2) * 16  # place it on the middle line
chars = chars[:midpoint] + "MOSAICVIGENEREXX" + chars[midpoint:]

# another word search hint at the end, and truncate to 256
chars = chars[:256 - len("GOODBYE")] + "GOODBYE"


for i, c in zip(range(len(chars)), chars):
    if i % 16 == 0:
        print("")
    print("{:>3} {}".format(i, c), end="  ##  ")
print("")

# create a lookup table for all the letters, with the positions in the block where the letter can be found
lookup = {}
for c in string.ascii_uppercase:
    lookup[c] = [i for i in range(len(chars)) if chars[i] == c]


def encode_lookup(message):
    return " ".join(str(random.choice(lookup[c]) + 1 if c in lookup.keys() else "") for c in message)


def encode_min(message):
    return " ".join(str(min(lookup[c]) + 1 if c in lookup.keys() else "") for c in message)


top_message = [i.upper() for i in top_message]

top_message_encoded = [encode_lookup(i) for i in top_message]

print(top_message)
print(top_message_encoded)


font = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 25)
img = Image.new("RGBA", (WIDTH, HEIGHT), BLACK)
draw = ImageDraw.Draw(img)
draw.fontmode = "1"  # this sets font anti-aliasing off.
for i, encoded_message in enumerate(top_message_encoded):
    encoded_width = font.getsize(encoded_message)[0]
    draw.text(((WIDTH - encoded_width) / 2, 16 + SPACING * i), encoded_message, WHITE, font=font)


def encode_as_colour(char):
    char_value = ord(char)
    c = [255, 255, 255]
    c[random.randint(0, 2)] = char_value
    return tuple(c)


for row in range(16):
    for col in range(16):
        i = row * 16 + col
        draw.text(
            (STARTX + col * SPACING, STARTY + row * SPACING),
            chars[i],
            encode_as_colour(random.choice(string.ascii_uppercase + string.ascii_lowercase)),
            font=font
        )
draw = ImageDraw.Draw(img)
img.save("text_on_image.png")
