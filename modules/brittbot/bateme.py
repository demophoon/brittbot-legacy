#!/usr/bin/env python
# encoding: utf-8
# jenni brittbot/420.py - Get n0sc0ped.

import random

bates = [
    "I like to dissect girls. Did you know I'm utterly insane?",
    "I have to return some videotapes.",
    "I'm into, uh, well, murders and executions, mostly.",
    "I've killed a lot of people. Some girls in the apartment uptown uh, some homeless people maybe 5 or 10 um an NYU girl I met in Central Park. I left her in a parking lot behind some donut shop.",
    "Tonight I, uh, I just had to kill a LOT of people.",
    "Do you like Huey Lewis and The News?",
    "TRY GETTING A RESERVATION AT DORSIA NOW, YOU FUCKING STUPID BASTARD! YOU, FUCKING BASTARD!",
    "Do you like Phil Collins?",
    "Look at that subtle off-white coloring. The tasteful thickness of it. Oh, my God. It even has a watermark.",
    "Duct tape. I need it for... taping something.",
    "Cool it with the anti-Semitic remarks.",
]

def bate_me(jenni, input):
    index = random.choice(range(len(bates)))
    msg = "%s" % (
        bates[index]
    )
    jenni.say(msg)
bate_me.rule = "^(bate+ ?me+),? (.*)" 
bate_me.priority = 'medium'
