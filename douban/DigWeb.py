
from douban import IPAgent
import requests
import random
from bs4 import BeautifulSoup
from urllib import request


proxy_list = IPAgent.get_IPAgent()
headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
def BS(url):
    html_ = request.urlopen(url)
    soup = BeautifulSoup(html_,'lxml')
    return soup

page_url = 'http://movie.douban.com'
soup = BS(page_url)
movie_list = soup.findAll('li',{'class':'title'})
movie_url = movie_list[0].a.attrs['href']
soup = BS(movie_url)
movie_comment_url = soup.find('div',{'id':'comments-section'}).h2.span.a
all_comment_url = movie_comment_url.attrs['href']
print(all_comment_url)

def get_all_comment( all_comment_url, headers, proxy_list,count, x=1):
    proxy = random.choice(proxy_list)
    print(proxy)
    requrl = requests.get(all_comment_url,headers = headers,proxies = proxy)
    soup = BeautifulSoup(requrl.text,'lxml')
    orig_comment_list = soup.findAll('div',{'class':'comment'})
    comment_list = []
    for i in orig_comment_list:
        comment_list.append(i.p.get_text())
    for i in comment_list:
        print(x)
        print(i)
    if x<count:
        next_page = soup.find('div',{'id':'paginator'}).find('a',{'class','next'})
        next_url = next_page.attrs['href']
        url_split = all_comment_url.split('?')
        next_url = url_split[0] + next_url
        x += 1
        get_all_comment( next_url, headers, proxy_list,count,x)


get_all_comment( all_comment_url, headers, proxy_list,3)



