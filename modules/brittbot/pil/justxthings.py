#!/usr/bin/env python
# encoding: utf-8

import sys
import uuid
import glob
import random

from PIL import (
    Image,
    ImageDraw,
    ImageFont,
    ImageFilter,
    ImageChops,
)

# Required apt Packages:
# libjpeg-dev
# libfreetype6-dev
# Required pip Packages:
# pillow


def generate_image(user, quote):
    images = glob.glob('modules/brittbot/pil/images/*.jpg')
    images += glob.glob('modules/brittbot/pil/images/*.png')

    # Initialize Image Object and get sizes
    img = random.choice(images)
    img = Image.open(img)
    imgX, imgY = img.size

    # Initialize Draw Object for drawing all the things
    draw = ImageDraw.Draw(img)

    # Initialize Fonts
    justfontthings = ImageFont.truetype('modules/brittbot/pil/UCU charles script.ttf', 18)
    quotefont = ImageFont.truetype('modules/brittbot/pil/LibreBaskerville-Regular.ttf', 28)

    # What are we going to say?
    justtextthings = "#just%sthings" % user
    quote = quote.strip()
    xpadding = 40

    # Get size of font and set positions for drawing
    x, y = draw.textsize(justtextthings, font=justfontthings)
    draw.text(
        (imgX - x - 25, imgY - y - 20),
        justtextthings,
        (255, 255, 255),
        font=justfontthings
    )

    x, y = draw.textsize(quote, font=quotefont)
    maxy = 0

    lines = []
    words = quote.split(' ')
    currentLine = []
    for word in words:
        testLine = currentLine[:]
        testLine.append(word)
        textx, texty = draw.textsize(' '.join(testLine), font=quotefont)
        if texty > maxy:
            maxy = texty
        if textx + xpadding > imgX:
            lines.append(currentLine)
            currentLine = [word]
        else:
            currentLine.append(word)
    lines.append(currentLine)

    # Create filter for blurring images
    blur = Image.new('RGBA', img.size, (0, 0, 0, 0))
    blurdraw = ImageDraw.Draw(blur)

    for index, line in enumerate(lines):
        line = ' '.join(line)

        lines_offset = 1
        if len(lines) % 2 == 0:
            lines_offset = 0
        ypos = (maxy * (len(lines) - lines_offset) / 2)
        yposmid = (len(lines) - lines_offset) * ypos / 2
        ypos = (index * ypos) - yposmid

        # print len(lines), maxy * len(lines), ypos

        x, y = draw.textsize(line, font=quotefont)
        blurdraw.text(
            ((imgX / 2) - (x / 2), (imgY / 2) - ((maxy * len(lines)) / 2) + ypos),
            line,
            (0, 0, 0),
            font=quotefont
        )
    blur = blur.filter(ImageFilter.GaussianBlur(radius=3))

    crispdraw = ImageDraw.Draw(blur)
    for index, line in enumerate(lines):
        line = ' '.join(line)

        lines_offset = 1
        if len(lines) % 2 == 0:
            lines_offset = 0
        ypos = (maxy * (len(lines) - lines_offset) / 2)
        yposmid = (len(lines) - lines_offset) * ypos / 2
        ypos = (index * ypos) - yposmid

        # print len(lines), maxy * len(lines), ypos

        x, y = draw.textsize(line, font=quotefont)
        crispdraw.text(
            ((imgX / 2) - (x / 2), (imgY / 2) - ((maxy * len(lines)) / 2) + ypos),
            line,
            (255, 255, 255),
            font=quotefont
        )

    img = img.convert('RGBA')
    img = Image.composite(img, blur, ImageChops.invert(blur))
    imagepath = '/var/www/htdocs/brittbot/'
    imagefile = "%s.png" % str(uuid.uuid4()).replace('-', '')[0:8]
    img.save(imagepath + imagefile)
    return imagefile

if __name__ == '__main__':
    user, quote = sys.argv[1:]
    print generate_image(user, quote)
