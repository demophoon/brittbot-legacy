#!/usr/bin/env python
# encoding: utf-8
# jenni brittbot/awyiss.py - Aw Yisser

import urllib
import urllib2
import json

from modules.brittbot.filters import smart_ignore


@smart_ignore
def awwyiss(jenni, input):
    url = 'http://awyisser.com/api/generator'
    data = {
        "phrase": input.groups()[1],
        "tweet": False,
    }
    data = urllib.urlencode(data)
    req = urllib2.Request(url, data)
    response = json.loads(urllib2.urlopen(req).read())
    jenni.say("aw yiss. motha. fuckin. %s. %s" % (
        input.groups()[1],
        response.get("link", ""))
    )
awwyiss.rule = "^(aw+ ?yis+),? (.*)"
awwyiss.priority = 'medium'
