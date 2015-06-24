import urllib
import json
from urlparse import urlparse, parse_qs

from modules.brittbot.filters import smart_ignore
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


@smart_ignore
def yt_context(jenni, input):
    target = input.groups()[0]
    print target
    video_id = parse_qs(urlparse(target).query).get("v")
    if not video_id:
        video_id = [urlparse(target).path[1:]]
    yt = get_video_information(video_id[0], jenni.config.youtube_api_key)
    if yt:
        youtube = colorize("You", fg=colors['black'], bg=colors['white'])
        youtube += colorize("Tube", fg=colors['white'], bg=colors['red'])
        jenni.say("%s \"%s\" (%s) by %s - %s" % (
            youtube,
            yt['title'],
            yt['duration'],
            yt['author'],
            yt['shorturl'],
        ))
yt_context.rule = r'.*(https?://.*?youtu\S*)\s?'
yt_context.priority = 'medium'
