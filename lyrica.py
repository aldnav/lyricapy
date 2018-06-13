import re
import requests
from bs4 import BeautifulSoup

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
        l = line.split(']')[1]
        lyrics_obj.append((ts, l))
    return lyrics_obj


def get_lyrics(title="", artist=""):
    """Get lyrics for a given song via rentanadviser.com"""
    url = 'http://www.rentanadviser.com/en/subtitles/getsubtitle.aspx?'
    r = requests.get(url, params=dict(song=title, artist=artist))
    if r.status_code != 200:
        return None
    if 'No subtitle were found!' in r.text:
        return 'Sorry. No lyrics found.'
    soup = BeautifulSoup(r.text, 'lxml')
    
    # request the simple one
    data = {
        '__EVENTTARGET' : 'ctl00$ContentPlaceHolder1$btnlyricssimple',
        '__EVENTARGUMENT' : '',
        'ctl00$txtSearch' : 'Search Apps...',
        'ctl00$Overcome_Enter_problem_in_IE1' : '',
        'ctl00$ContentPlaceHolder1$txtsearchsubtitle' : 'Search Subtitle...',
        'ctl00$ContentPlaceHolder1$Overcome_Enter_problem_in_IE2' : '',
    }
    for inp in soup.find_all(id=re.compile('__.*')):
        data[inp.get('name')] = inp.get('value')

    r = requests.post(r.url, data=data)
    lyrics = r.text
    return lyrics


if __name__ == '__main__':
    lyrics = get_lyrics(title='Wiggle', artist='Jason Derulo')
    parsed = parse_lyrics(lyrics)
    print(parsed)

