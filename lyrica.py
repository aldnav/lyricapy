"""
Usage: lyrica.py <title> <artist>
"""

import re
import requests
from bs4 import BeautifulSoup
from docopt import docopt

headers = {
    'User-Agent': 'Mozilla/5.0'
}


def parse_lyrics(text):
    lyrics_obj = []
    for line in text.split('\n'):
        line = line.strip()
        if (len(line) == 0 or
                'RentAnAdviser.com' in line):
            continue
        ts = line.split(']')[0][1:]
        li = line.split(']')[1]
        lyrics_obj.append((ts, li))
    return lyrics_obj


def get_lyrics(title="", artist=""):
    """Get lyrics for a given song via rentanadviser.com"""
    try:
        title = title.decode('utf-8')
        artist = artist.decode('utf-8')
    except AttributeError:
        pass
    title = title.replace(' ', '+')
    artist = artist.replace(' ', '+')
    url = 'http://www.rentanadviser.com/en/subtitles/getsubtitle.aspx'
    r = requests.get(url, params={'artist': artist, 'song': title})
    if r.status_code != 200:
        return None
    if 'No subtitle were found!' in r.text:
        return 'Sorry. No lyrics found.'
    soup = BeautifulSoup(r.text, 'lxml')

    # request the simple one
    data = {
        '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$btnlyricssimple',
        '__EVENTARGUMENT': '',
        'ctl00$txtSearch': 'Search Apps...',
        'ctl00$Overcome_Enter_problem_in_IE1': '',
        'ctl00$ContentPlaceHolder1$txtsearchsubtitle': 'Search Subtitle...',
        'ctl00$ContentPlaceHolder1$Overcome_Enter_problem_in_IE2': '',
    }
    for inp in soup.find_all(id=re.compile('__.*')):
        data[inp.get('name')] = inp.get('value')
    r = requests.post(r.url, data=data)
    lyrics = r.text if not r.text.startswith('<html') else ''
    if lyrics == '':
        with open('out.html', 'w') as f:
            f.write(r.text)
    return lyrics


if __name__ == '__main__':
    args = docopt(__doc__)
    if not args:
        import sys
        sys.exit(0)
    title = args['<title>']
    artist = args['<artist>']
    lyrics = get_lyrics(title=title, artist=artist)
    parsed = parse_lyrics(lyrics)
    print(parsed)
