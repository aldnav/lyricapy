import subprocess
from lyrica import get_lyrics, parse_lyrics

get_title_cmd = 'playerctl metadata title'
get_artist_cmd = 'playerctl metadata artist'


def lyricactl():
    title = subprocess.check_output(get_title_cmd.split())
    artist = subprocess.check_output(get_artist_cmd.split())
    print('{} - {}'.format(title, artist))
    lyrics = parse_lyrics(get_lyrics(title, artist))
    if len(lyrics) == 0:
        print(':( Lyrics not available.')
    else:
        print(lyrics)


lyricactl()
