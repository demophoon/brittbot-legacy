#!/usr/bin/env python
'''
brittbot/hardware.py - playing around with hardware components with brittbot
'''

import time

try:
    import Adafruit_BMP.BMP085 as BMP085
    import Adafruit_BBIO.GPIO as GPIO
    import Adafruit_BBIO.PWM as PWM
except ImportError:
    raise Exception("Cannot utilize hardware components on this node.")

sensor = BMP085.BMP085()

colors = {
    'red': 'P9_14',
    'blue': 'P9_42',
    'green': 'P9_21',
}


def get_temp():
    c = sensor.read_temperature()
    f = c * (9.0 / 5.0) + 32
    return f


def high(color, brightness=None):
    if not brightness:
        brightness = 100
    PWM.start(colors[color], brightness)


def low(color):
    PWM.stop(colors[color])


def temp_reply(jenni, msg):
    jenni.reply("The tempurature at home is {0:0.1f}F".format(get_temp()))
temp_reply.rule = r'^!temp'


def mention_hilight(jenni, msg):
    if not msg.admin:
        high('red')
        high('green')
mention_hilight.rule = r'.*${admin}'


def admin_talking(jenni, msg):
    if msg.admin:
        low('red')
        low('green')
admin_talking.rule = r'.*'


def setup(jenni):
    for color, pin in colors.items():
        high(color, 15)

    time.sleep(1.0)

    for color, pin in colors.items():
        low(color)
