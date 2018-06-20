"""
Usage: lyricactl.py [<persist>]
"""

import subprocess
import time
from docopt import docopt
from lyrica import get_lyrics, parse_lyrics

get_title_cmd = 'playerctl metadata title'
get_artist_cmd = 'playerctl metadata artist'
get_player_status = 'playerctl status'
song = ''
song_d = ''


def clean_title(title):
    title = title.split('-')[0]
    title = title.split('(')[0]
    return title.strip()


def get_lines(lyrics):
    return '\n'.join([x[1] for x in lyrics])


def lyricactl():
    global song_d
    global song
    song_d = song
    song, title, artist = get_song()
    print(song)
    lyrics = get_lines(parse_lyrics(get_lyrics(title, artist)))
    if len(lyrics) == 0:
        print(':( Lyrics not available.')
        song = ''
    else:
        print(lyrics)


def get_song():
    title = subprocess.check_output(get_title_cmd.split())
    artist = subprocess.check_output(get_artist_cmd.split())
    title = clean_title(title.decode())
    return ('{} - {}'.format(title, artist), title, artist)


if __name__ == '__main__':
    args = docopt(__doc__)
    if not args:
        import sys
        sys.exit(0)
    persist = args['<persist>'] == '1'
    if persist:
        while True:
            song, _, _ = get_song()
            if song_d != song:
                lyricactl()
            time.sleep(0.5)
    else:
        lyricactl()
