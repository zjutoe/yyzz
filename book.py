#!/usr/bin/env python3

import random
import time
import sys
import re
import requests
import bs4
import json


def req_get(url):
    return requests.get(url, headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safiri/537.36 SE 2.X MetaSr 1.0"})
    

class Book:
    def __init__(self, book):
        divs = book.find_all('div')
        div_pic, div_info, div_pub = divs[:3]
        
        pic_a = div_pic.find('a')
        pic_img = div_pic.find('img')
        self.url_douban = pic_a['href']
        self.url_cover = pic_img['src']

        info_a = div_info.find('a')
        self.title = info_a['title']

        self.pub = div_pub.text.strip()


    def tojson(self):
        j = {
            'title':self.title,
            'publish':self.pub,
            'url_douban':self.url_douban,
            'url_cover':self.url_cover,
        }
        return json.dumps(j)
    


def parse_book_list(soup):
    ret = []
    # soup = bs4.BeautifulSoup(r.text, 'html.parser')
    lli = soup.find_all('li')
    for li in lli:
        if li.has_attr('class') and li['class'] == ['subject-item']:
            b = Book(li)
            ret.append(b)

    return ret
    
        
# def book_wish_list(bookurl):
#     ret = []
#     r = req_get(bookurl)

#     if r.status_code == 200:
#         ret += parse_book_list(r)


def book_count(soup):
    t = soup.title.string
    count = re.findall('([0-9]+)', t)[-1]
    return int(count)



def book_list_all(url):
    ret = []

    num_book = 0
    r = req_get(url)
    if r.status_code == 200:
        soup = bs4.BeautifulSoup(r.text, 'html.parser')
        num_book = book_count(soup)
        ret += parse_book_list(soup)

    for page in range(15, num_book, 15):
        time.sleep(1 + 2*random.random()) # sleep for a random period to avoid being banned
        r = req_get(url + ('?sort=time&start=%d&filter=all&mode=grid&tags_sort=count' % page))
        if r.status_code == 200:
            soup = bs4.BeautifulSoup(r.text, 'html.parser')
            ret += parse_book_list(soup)
        
    return ret
    

# wish to read
def book_wish_list_all(uid):
    bookurl = 'https://book.douban.com/people/%s/wish' % uid
    return book_list_all(bookurl)


# currently reading
def book_reading_list_all(uid):
    bookurl = 'https://book.douban.com/people/%s/do' % uid
    return book_list_all(bookurl)


# finished read 
def book_finished_list_all(uid):
    bookurl = 'https://book.douban.com/people/%s/collect' % uid
    return book_list_all(bookurl)



if __name__ == '__main__':
    id = sys.argv[1]

    with open('read_%s_wish.json' % id, 'w') as f:
        for b in book_wish_list_all(bwish):
            f.write(b.tojson() + '\n')

    with open('read_%s_reading.json' % id, 'w') as f:
        for b in book_reading_list_all(bwish):
            f.write(b.tojson() + '\n')


    with open('read_%s_finished.json' % id, 'w') as f:
        for b in book_finished_list_all(bwish):
            f.write(b.tojson() + '\n')
            

