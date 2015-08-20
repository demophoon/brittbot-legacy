#!/usr/bin/env python
# encoding: utf-8

ORG_CODE = "d00d11e681934f4688fdce9cebd5afce"
SESSION = "Session goes here"


def voicebox(jenni, msg):
    jenni.reply("This function is currently disabled.")
    return
    ROOM_CODE = "HWWB"
    import urllib
    import urllib2

    text = msg.groups()[0]
    if not text:
        return
    nick = msg.nick
    text = "{}: {}".format(nick, text)
    data = urllib.urlencode({
        'organization': ORG_CODE,
        'room_code': ROOM_CODE,
        'session': SESSION,
        'text': text,
    })
    urllib2.urlopen("http://vbsongs.com/api/v1/popups", data=data)
    jenni.reply("Your message has been sent to the Voicebox room.")
voicebox.rule = r'^!voicebox (.*)'


def voicebox_whats_next(jenni, msg):
    return
    ROOM_CODE = "HWWB"
    import urllib2
    import json
    request = urllib2.Request("http://vbsongs.com/api/v1/queue?room_code={}".format(ROOM_CODE))
    request.add_header("Content-Type", "application/json; charset=utf-8")
    response = urllib2.urlopen(request).read()
    print response
    response = json.loads(response)
    title = response['current_song']['title']
    artist = response['current_song']['artist']
    jenni.reply("Current song playing at Voicebox now: {} by {}".format(title, artist))
voicebox_whats_next.rule = r'^!voicebox$'
