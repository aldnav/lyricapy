import requests
from bs4 import BeautifulSoup


def get_lyrics(title="", artist=""):
    """Get lyrics for a given song via rentanadviser.com"""
    url = 'http://www.rentanadviser.com/en/subtitles/getsubtitle.aspx?'
    r = requests.get(url, params=dict(song=title, artist=artist))
    if r.status_code != 200:
        return None
    if 'No subtitle were found!' in r.text:
        return 'Sorry. No lyrics found.'
    soup = BeautifulSoup(r.text, 'lxml')
    lyrics_div = soup.find(id='myTabContent')
    print(list(lyrics_div.children)[1])

if __name__ == '__main__':
    get_lyrics(title='Wiggle', artist='Jason Derulo')

