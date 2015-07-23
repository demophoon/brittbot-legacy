import json

import pylast

from modules.brittbot.filters import smart_ignore
from modules.brittbot.helpers import colorize, colors


f = open('./modules/lastfm.json', 'r')
secret = json.loads(f.read())

network = pylast.LastFMNetwork(
    api_key=secret['api_key'],
    api_secret=secret['secret'],
    username=secret['username'],
    password_hash=pylast.md5(secret['password']),
)


def format_track(song_obj):
    track = song_obj.title
    artist = song_obj.artist.name
    # album = song_obj.album
    return "%s by %s" % (
        colorize(track, fg=colors['teal']),
        colorize(artist, fg=colors['teal']),
    )


@smart_ignore
def register_lastfm_account(jenni, msg):
    nick = msg.nick
    if 'lastfm' not in jenni.brain:
        jenni.brain['lastfm'] = {}
    jenni.brain['lastfm'][nick] = msg.groups()[0].strip()
    jenni.reply("You've registered %s to your nickname."
                " Say 'brittbot: what is %s listening to?' to activate" % (
                    msg.groups()[0].strip(),
                    nick,
                ))
register_lastfm_account.rule = r'^!lastfm register (\S+)'


@smart_ignore
def current_song(jenni, msg):
    import random
    if 'lastfm' not in jenni.brain:
        jenni.brain['lastfm'] = {}
    username = msg.groups()[0].strip()
    if username.lower() in ["i"]:
        username = msg.nick
    if username.lower() in ["you", "brittbot"]:
        robot_tracks = {
            'Styx': ['Mr. Roboto'],
            'The Flaming Lips': [
                'Yoshimi Battles the Pink Robots, Part 1',
                'Yoshimi Battles the Pink Robots, Part 2',
                'One More Robot/Sympathy 3000-21',
            ],
            'Daft Punk': [
                'Robot Rock',
                'Harder Better Faster Stronger',
                'Derezzed',
            ],
        }
        artist = random.choice(robot_tracks.keys())
        track = random.choice(robot_tracks[artist])
        track = "%s by %s" % (
            colorize(track, fg=colors['teal']),
            colorize(artist, fg=colors['teal']),
        )
        fmsg = "I am listening to %s right now!" % (
            track,
        )
        jenni.say(fmsg)
        return
    elif username in jenni.brain['lastfm']:
        username = jenni.brain['lastfm'][username]
    if not username:
        username = secret['username']
    user = network.get_user(username)
    current_song = user.get_now_playing()
    fmsg = ""
    recent_tracks_count = 3
    if current_song:
        fmsg += "%s is listening to %s right now! " % (
            username,
            format_track(current_song),
        )
        recent_tracks_count -= 1
    recent_tracks = user.get_recent_tracks()
    tracks = ", ".join([
        format_track(x.track) for x in recent_tracks[:recent_tracks_count]
    ])
    fmsg += "%s recent tracks: %s" % (username, tracks)
    jenni.say(fmsg)
current_song.rule = r'^(?i)(?:$nickname\S? )?what (?:am|are|is) (\S+) listen.*to'
current_song.priority = 'medium'
