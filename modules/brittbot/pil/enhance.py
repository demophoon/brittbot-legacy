#!/usr/bin/env python
# encoding: utf-8

import uuid
import random
import io
import urllib

from PIL import (
    Image,
    ImageEnhance,
    ImageOps,
)

imagepath = '/var/www/htdocs/brittbot/'


def image_from_url(url):
    path = io.BytesIO(urllib.urlopen(url).read())
    img = Image.open(path)
    img = img.convert('RGBA')
    return img


def enhance(url):
    img = image_from_url(url)
    enhancements = [
        ImageEnhance.Color,
        ImageEnhance.Contrast,
        ImageEnhance.Brightness,
        ImageEnhance.Sharpness,
    ]
    for _ in range(random.randint(2,6)):
        img = random.choice(enhancements)(img).enhance(random.random() * 3)
    imagefile = "%s.jpg" % str(uuid.uuid4()).replace('-', '')[0:8]
    img.save(imagepath + imagefile, 'jpeg', quality=random.randint(0,15))
    return imagefile

def to_jpg(url):
    img = image_from_url(url)
    imagefile = "%s.jpg" % str(uuid.uuid4()).replace('-', '')[0:8]
    img.save(imagepath + imagefile, 'jpeg', quality=100)
    return imagefile


def zoom(url):
    img = image_from_url(url)
    width, height = img.size
    img = ImageOps.fit(
        img,
        (int(random.random() * width * .5), int(random.random() * height * .5)),
        Image.NEAREST,
        0,
        (random.random(), random.random())
    )
    img = img.resize((width, height))

    imagefile = "%s.png" % str(uuid.uuid4()).replace('-', '')[0:8]
    img.save(imagepath + imagefile)
    return imagefile
