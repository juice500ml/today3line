from bs4 import BeautifulSoup as bs
from multiprocessing import Pool
from html2text import HTML2Text
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
    [tag.extract() for tag in soup.find_all('p', {'class': 'cap'})]
    [tag.extract() for tag in soup.find_all('caption')]
    dl = soup.find('dl', {'class': 'na_reference'})
    if not dl:
        dl = soup.find('div', {'id': 'na_author_top'})
    if not dl:
        [tag.extract() for tag in [tag for tag in dl.next_elements]]
    text_all = str(soup)
    
    helper = HTML2Text()
    helper.ignore_links = True
    helper.ignore_images = True
    helper.ignore_tables = True
    text_all = helper.handle(text_all)
    
    for ch in ['#', '/', '*', '_', '>', '&gt', '&lt', ';', ':', '\\']:
        text_all = text_all.replace(ch, ' ')
    text_all = ' '.join(text_all.split())

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
    print(parse_link(get_list()[0]))
    #pool = Pool(16)
    #ret = pool.map(parse_all, get_list())
