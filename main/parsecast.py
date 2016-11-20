from bs4 import BeautifulSoup as bs
from textrankr import TextRank

import requests

def get_list():
    url = 'http://navercast.naver.com/'
    req = requests.get(url)
    ret = list()

    if not req.ok:
        return ret

    soup = bs(req.text, 'html.parser')
    links = soup.find_all('a', {'class': 'card'})
    for link in links:
        ret.append(url + link['href'])

    return ret


def parse_link(url):
    req = requests.get(url)
    soup = bs(req.text, 'html.parser')

    title = str(soup.find('h3', {'class': 'ending_tit_new'}).find('img')['alt'])

    img_url = soup.find('span', {'class': 'img_wrap2'})
    if img_url:
        img_url = str(img_url.find('img')['src'])

    soup = soup.find('div', {'class': 'na_doc'})
    [tag.extract() for tag in soup.find_all('caption')]
    [tag.extract() for tag in soup.find_all('p', {'class': 'cap'})]
    [tag.extract() for tag in soup.find_all('div', {'class': 'tmp_source2'})]
    [tag.extract() for tag in soup.find_all('div', {'id': 'na_author_top'})]
    [tag.extract() for tag in soup.find_all('div', {'class': 't_pdate'})]
    [tag.extract() for tag in soup.find_all('div', {'class': 'na_cmt_bx'})]
    [tag.extract() for tag in soup.find_all('', {'style': 'display:none'})]
    text_all = ' '.join(soup.get_text().split())

    ret = list()
    ret.append(title)
    ret.append(url)
    ret.append(img_url)
    
    import jpype
    if jpype.isJVMStarted():
        jpype.attachThreadToJVM()
    ret.append(TextRank(text_all).summarize().split('\n'))

    return ret
    

if __name__ == '__main__':
    url_list = get_list()
    for url in url_list:
        print(parse_link(url))
