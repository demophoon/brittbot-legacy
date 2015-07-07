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


def save_to_url(img):
    imagefile = "%s.jpg" % str(uuid.uuid4()).replace('-', '')[0:8]
    img.save(imagepath + imagefile, 'jpeg', quality=1)
    return imagefile


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
    return save_to_url(img)

