import urllib
import json
from urlparse import urlparse, parse_qs

from modules.brittbot.helpers import (colorize, colors)


def get_duration(seconds):
    return seconds[2:].lower()
    if seconds < 60:
        return ":%s" % "{0:02d}".format(seconds)
    elif seconds > 61 and seconds < 3600:
        return "%s%s" % ("{0:02d}".format(seconds / 60), get_duration(seconds % 60))
    elif seconds > 3601:
        return "%d:%s" % (seconds / 3600, get_duration(seconds % 3600))


def get_video_information(videoid, api_key):
    get_data_url = "https://www.googleapis.com/youtube/v3/videos?id=%s&key=%s&part=snippet,contentDetails"
    if not(len(videoid) == 11):
        return False
    yturl = get_data_url % (videoid, api_key)
    vid = json.loads(urllib.urlopen(yturl).read())['items'][0]
    vid_obj = {
        'title': vid['snippet']['title'],
        'duration': get_duration(vid['contentDetails']['duration']),
        'description': vid['snippet']['description'],
        'author': vid['snippet']['channelTitle'],
        'shorturl': "http://youtu.be/" + videoid,
    }
    return vid_obj


def yt_context(jenni, msg):
    import random
    target = msg.groups()[0]
    video_id = parse_qs(urlparse(target).query).get("v")
    obfuscate = parse_qs(urlparse(target).query).get("o")
    if video_id and "QrGrOK8oZG8" in video_id and msg.nick == "demophoon":
        obfuscate = True
    if obfuscate is not None:
        video_id = [random.choice([
            # Maru
            "bXtHwvp7jYE",
            "8uDuls5TyNE",
            "jgxL-PwmY7s",
            "euCG3jbefH8",
            "6lC2lbeY_rU",
            "VKQtwvKa-aY",
            "AeJX7fxz-f4",
            # Music videos
            "gy1B3agGNxw",
            # Aunty Donna Thats what you get
            "9x7r1er6Ljw",
        ])]
    if not video_id:
        video_id = [urlparse(target).path[1:]]
    yt = get_video_information(video_id[0], jenni.config.youtube_api_key)
    if yt:
        if obfuscate is not None:
            yt['shorturl'] = "http://youtu.be/" + parse_qs(urlparse(target).query).get("v")[0]
        youtube = colorize("You", fg=colors['black'], bg=colors['white'])
        youtube += colorize("Tube", fg=colors['white'], bg=colors['red'])
        jenni.say("%s \"%s\" (%s) by %s - %s" % (
            youtube,
            yt['title'],
            yt['duration'],
            yt['author'],
            yt['shorturl'],
        ))
yt_context.rule = r'.*(youtu\S*)\s?'
yt_context.priority = 'medium'
