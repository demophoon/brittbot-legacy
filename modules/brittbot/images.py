#!/usr/bin/env python
# encoding: utf-8
# jenni brittbot/images.py - All image generation functions

import time
import re
import random
import urllib
import uuid
import json

import requests
from requests_toolbelt import MultipartEncoder

from modules.brittbot.pil import justxthings
from modules.brittbot.pil import enhance
from modules.find import load_db, save_db

image_filters = [
    'inceptionist_painting',
    'salvia',
    'art_deco',
    'painting',
    'mirage',
    'demonic',
    'facelift',
    'charcoal',
    'trippy',
    'self_transforming_machine_elves',
    'botanical_dimensions',
    'digital_prism',
    'sketchasketch',
    'dead_presidents',
    'digital_weave',
    'mystery_flavor',
]


def img_enhance(jenni, msg):
    url = msg.groups()[0]
    if not url:
        imgs = load_db().get(msg.sender)
        if imgs and 'last_said' in imgs:
            url_regex = "(https?://\S+\.(?:jpg|png|jpeg|gif))"
            for img in reversed(imgs['last_said']):
                urls = re.findall(url_regex, img)
                if urls:
                    url = random.choice(urls)
                    break
    if not url:
        return
    filename = enhance.enhance(url)
    url = "http://brittbot.brittg.com/{}".format(filename)
    msgs = load_db()
    msgs[msg.sender]['last_said'].append(url)
    save_db(msgs)
    jenni.reply(url)
img_enhance.rule = r'^!enhance( \S+)?$'


def img_save_as_jpg(jenni, msg):
    url = msg.groups()[0]
    if not url:
        imgs = load_db().get(msg.sender)
        if imgs and 'last_said' in imgs:
            url_regex = "(https?://\S+\.(?:jpg|png|jpeg|gif))"
            for img in reversed(imgs['last_said']):
                urls = re.findall(url_regex, img)
                if urls:
                    url = random.choice(urls)
                    break
    if not url:
        return
    filename = enhance.to_jpg(url)
    url = "http://brittbot.brittg.com/{}".format(filename)
    msgs = load_db()
    msgs[msg.sender]['last_said'].append(url)
    save_db(msgs)
    jenni.reply(url)
img_save_as_jpg.rule = r'^!jpe?g( \S+)?$'


def img_zoom(jenni, msg):
    url = msg.groups()[0]
    if not url:
        imgs = load_db().get(msg.sender)
        if imgs and 'last_said' in imgs:
            url_regex = "(https?://\S+\.(?:jpg|png|jpeg|gif))"
            for img in reversed(imgs['last_said']):
                urls = re.findall(url_regex, img)
                if urls:
                    url = random.choice(urls)
                    break
    if not url:
        return
    filename = enhance.zoom(url)
    url = "http://brittbot.brittg.com/{}".format(filename)
    msgs = load_db()
    msgs[msg.sender]['last_said'].append(url)
    save_db(msgs)
    jenni.reply(url)
img_zoom.rule = r'^!zoom( \S+)?$'


def process_deepdream(file_handle, img_filter=None):
    if not img_filter:
        img_filter = 'trippy'

    data = MultipartEncoder({
        'title': 'wat',
        'description': 'none',
        'filter': img_filter,
        'submit': "Let's Dream",
        'image': ('img0.jpg', file_handle, 'image/jpeg'),
    })
    response = requests.post(
        'https://dreamscopeapp.com/api/images',
        data=data,
        verify=False,
        headers={
            'Content-Type': data.content_type
        }
    )
    if response.status_code >= 400:
        print response
        print response.content
        raise("An error has occurred")
    image_id = json.loads(response.text)['uuid']
    for _ in range(30):
        time.sleep(1.5)
        r = requests.get('https://dreamscopeapp.com/api/images/{}'.format(image_id))
        final_url = r.json()['filtered_url']
        if final_url:
            break
    if not final_url:
        raise('Deep dream took too long to complete. Try a smaller image.')
    return final_url


def deepdream(jenni, msg):
    if 'last_trip' in jenni.brain and time.time() - jenni.brain['last_trip'] < 30:
        jenni.reply('Tripping too hard right now, please try again in 30 seconds.')
        return
    img_filter = msg.groups()[0]
    in_url = msg.groups()[1]
    if img_filter in ['lsd', 'deepdream']:
        img_filter = 'trippy'
    if not in_url:
        imgs = load_db().get(msg.sender)
        if imgs and 'last_said' in imgs:
            url_regex = "(https?://\S+\.(?:jpg|png|jpeg))"
            for img in reversed(imgs['last_said']):
                urls = re.findall(url_regex, img)
                if urls:
                    in_url = random.choice(urls)
                    break
    if not in_url:
        return
    f = open('/tmp/img.jpg', 'wb')
    f.write(urllib.urlopen(in_url).read())
    f.close()

    if in_url.endswith('.gif'):
        from PIL import (
            Image,
            ImageSequence,
        )
        import io
        from modules.brittbot.pil.images2gif import writeGif

        img = Image.open('/tmp/img.jpg')
        if hasattr(img, 'format') and img.format.lower() == 'gif':
            if not msg.admin:
                return
            original_duration = img.info['duration']
            frames = [frame.copy() for frame in ImageSequence.Iterator(img)]
            if len(frames) > 40:
                jenni.reply("Too many frames :(")
                return
            final_frames = []
            for i, frame in enumerate(frames):
                im = frame.convert('RGBA')
                im.save('/tmp/frame{}.jpg'.format(i), 'jpeg', quality=100)
                print "Processing frame {}...".format(i)
                url = process_deepdream(open('/tmp/frame{}.jpg'.format(i), 'rb'), img_filter)
                im = Image.open(io.BytesIO(urllib.urlopen(url).read()))
                final_frames.append(im)
                time.sleep(2)
            imagepath = '/var/www/htdocs/brittbot/'
            imagename = "%s.gif" % str(uuid.uuid4()).replace('-', '')[0:8]
            writeGif(imagepath + imagename, final_frames, duration=original_duration/1000.0, dither=0)
    else:
        final_url = process_deepdream(open('/tmp/img.jpg', 'rb'), img_filter)
        jenni.brain['last_trip'] = time.time()
        img = urllib.urlopen(final_url).read()
        imagepath = '/var/www/htdocs/brittbot/'
        imagename = "%s.jpg" % str(uuid.uuid4()).replace('-', '')[0:8]
        f = open(imagepath + imagename, 'w')
        f.write(img)
        f.close()
    url = "http://brittbot.brittg.com/{}".format(imagename)
    msgs = load_db()
    msgs[msg.sender]['last_said'].append(url)
    save_db(msgs)
    jenni.reply(url)
deepdream.rule = r'^!(lsd|deepdream|{})( \S+)?'.format('|'.join(image_filters))


def justxthingshandler(jenni, msg):

    hashtag = msg.groups()[1]
    quote = msg.groups()[0]

    if not quote:
        quotes = load_db().get(msg.sender)
        if quotes and 'last_said' in quotes:
            quotes['last_said'] = [q for q in quotes['last_said'] if not re.match(r'(.*)(#\S+\w)$', q)]
            quote = ''.join(quotes['last_said'][-1].split(':')[1:])

    if quote[0] in ['!'] or 'http' in quote:
        return
    if hashtag.startswith("##"):
        return
    if "action" in msg.lower():
        return
    if len(quote.split(' ')) > 25:
        return
    url = "http://brittbot.brittg.com/{}".format(justxthings.generate_image(
        str(quote),
        hashtag,
    ))
    jenni.reply(url)
justxthingshandler.rule = r"(.*)(#\S+\w)$"


def justxthingslistener(jenni, msg):
    if 'last_action' not in jenni.brain:
        jenni.brain['last_action'] = {}
    if msg.sender not in jenni.brain['last_action']:
        jenni.brain['last_action'][msg.sender] = 0
    if time.time() < jenni.brain['last_action'][msg.sender] + 3600:
        return
    if len(msg.split(' ')) == 1 or len(msg.split(' ')) > 20:
        return
    try:
        if str(msg)[0] in ['!']:
            return
    except Exception:
        return
    if "action" in msg.lower():
        return

    if random.choice(range(175)) == 0:
        url = "http://brittbot.brittg.com/{}".format(justxthings.generate_image(
            str(msg),
            "#just{}things".format(msg.nick)
        ))
        jenni.say(url)
        jenni.brain['last_action'][msg.sender] = time.time()
justxthingslistener.rule = r".*"
