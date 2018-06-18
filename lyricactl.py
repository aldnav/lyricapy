import subprocess
from lyrica import get_lyrics, parse_lyrics

get_title_cmd = 'playerctl metadata title'
get_artist_cmd = 'playerctl metadata artist'


def clean_title(title):
    title = title.split('-')[0]
    title = title.split('(')[0]
    return title.strip()


def lyricactl():
    title = subprocess.check_output(get_title_cmd.split())
    artist = subprocess.check_output(get_artist_cmd.split())
    title = clean_title(title.decode())
    print('{} - {}'.format(title, artist))
    lyrics = parse_lyrics(get_lyrics(title, artist))
    if len(lyrics) == 0:
        print(':( Lyrics not available.')
    else:
        print(lyrics)


lyricactl()
