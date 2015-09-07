#!/usr/bin/env python
# encoding: utf-8

import uuid
import random
import io
import urllib

from PIL import (
    Image,
    ImageSequence,
    ImageEnhance,
    ImageOps,
)

from modules.brittbot.pil.images2gif import writeGif

imagepath = '/var/www/htdocs/brittbot/'


def image_from_url(url):
    path = io.BytesIO(urllib.urlopen(url).read())
    img = Image.open(path)
    return img


def enhance(url):
    img = image_from_url(url)
    enhancements = [
        ImageEnhance.Color,
        ImageEnhance.Contrast,
        ImageEnhance.Brightness,
        ImageEnhance.Sharpness,
    ]
    if hasattr(img, 'format') and img.format.lower() == 'gif':
        edits = [random.choice(enhancements) for _ in range(random.randint(2, 6))]
        intensities = [random.random() * 3 for _ in range(len(edits))]
        frames = [frame.copy() for frame in ImageSequence.Iterator(img)]
        if len(frames) > 200:
            raise Exception("Gif too large: {}".format(len(frames)))
        original_duration = img.info['duration']
        final_frames = []
        shitty_image = random.choice([True] + ([False] * 3))
        for i, f in enumerate(frames):
            im = f.convert('RGBA')
            for edit, intensity in zip(edits, intensities):
                im = edit(im).enhance(intensity)
                pass
            if shitty_image:
                image_num = i % 3
            else:
                image_num = i
            im.save('/tmp/frame{}.jpg'.format(image_num), 'jpeg', quality=random.randint(0, 7))
            im = Image.open('/tmp/frame{}.jpg'.format(image_num))
            im = im.convert('P')
            final_frames.append(im)
        if random.choice([True] + ([False] * 3)):
            random.shuffle(final_frames)
        imagefile = "%s.gif" % str(uuid.uuid4()).replace('-', '')[0:8]
        writeGif(imagepath + imagefile, final_frames, duration=original_duration/1000.0, dither=0)
    else:
        img = img.convert('RGBA')
        for _ in range(random.randint(2, 6)):
            img = random.choice(enhancements)(img).enhance(random.random() * 3)
        imagefile = "%s.jpg" % str(uuid.uuid4()).replace('-', '')[0:8]
        img.save(imagepath + imagefile, 'jpeg', quality=random.randint(0, 15))
    return imagefile


def to_jpg(url):
    img = image_from_url(url)
    img = img.convert('RGBA')
    imagefile = "%s.jpg" % str(uuid.uuid4()).replace('-', '')[0:8]
    img.save(imagepath + imagefile, 'jpeg', quality=100)
    return imagefile


def zoom(url):
    img = image_from_url(url)
    img = img.convert('RGBA')
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
