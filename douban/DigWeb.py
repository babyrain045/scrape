from douban import Login
from douban import IPAgent
from douban import CloudWords
import requests
import random
from bs4 import BeautifulSoup
import time




proxy_list = IPAgent.get_IPAgent()
headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

page_url = 'http://movie.douban.com'
page_ = requests.Session().get(page_url)
soup = BeautifulSoup(page_.text,'lxml')
movie_list = soup.findAll('li',{'class':'title'})
movie_url = movie_list[0].a.attrs['href']
page_movie = requests.Session().get(movie_url)
soup = BeautifulSoup(page_movie.text,'lxml')
movie_comment_url = soup.find('div',{'id':'comments-section'}).h2.span.a
all_comment_url = movie_comment_url.attrs['href']
print(all_comment_url)
co = Login.login('am_cr','Cr930405')

def get_all_comment( all_comment_url, headers, proxy_list,count, x=1,all_comments = ''):
    proxy = random.choice(proxy_list)
    print(proxy)
    requrl = requests.Session().get(all_comment_url,headers = headers,proxies = proxy,cookies = co)
    soup = BeautifulSoup(requrl.text,'lxml')
    orig_comment_list = soup.findAll('div',{'class':'comment'})
    comment_list = []
    for i in orig_comment_list:
        comment_list.append(i.p.get_text())
    for i in comment_list:
        all_comments = all_comments+str(i.strip())
    if x<count:
        next_page = soup.find('div',{'id':'paginator'}).find('a',{'class','next'})
        next_url = next_page.attrs['href']
        if next_url is not None:
            url_split = all_comment_url.split('?')
            next_url = url_split[0] + next_url
            x += 1
            time_distribution = random.gauss(9,2)    #设定暂停时间，使得整个文档的运行更像高斯分布
            time_pause = time_distribution if time_distribution>2.1 else 2.1
            time.sleep(time_pause)
            return get_all_comment( next_url, headers, proxy_list,count,x,all_comments)

        else:
            print("已扫描完毕，没有寻找到更多评论")
            return all_comments
    else:
        print('已扫描完指定网页')
        return all_comments



all_comments = get_all_comment( all_comment_url, headers, proxy_list,10)
CloudWords.Word_Cloud(all_comments)





