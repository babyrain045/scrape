import urllib
import sys
import requests
from urllib import request
from bs4 import BeautifulSoup
import numpy
import pandas as pd
import matplotlib.pyplot as plt
import jieba
import time
import codecs
import matplotlib
import re
import pylab
from wordcloud import WordCloud
'''
matplotlib.rcParams['figure.figsize'] = (10.0, 5.0)
resp = request.urlopen('https://movie.douban.com/cinema/nowplaying/guangzhou/')
html_data = resp.read().decode('utf-8')
soup = BeautifulSoup(html_data,'lxml')
nowplaying_movie = soup.find_all('div',id = 'nowplaying')
nowplaying_movie_list = nowplaying_movie[0].find_all('li', class_ = 'list-item')
nowplaying_list = []
for item in nowplaying_movie_list:
    nowplaying_dict = {}
    nowplaying_dict['id'] = item['data-subject']
    for tag_img_item in item.find_all('img'):
        nowplaying_dict['name'] = tag_img_item['alt']
        nowplaying_list.append(nowplaying_dict)


url_login = 'http://accounts.douban.com/login'
s = requests.Session()
formdata = {'source':'index_nav',
             'redir':'https://www.douban.com',
             'form_email':'am_cr',
             'form_password':'cr930405'}
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
r = s.post(url_login,data=formdata,headers = headers)
content = r.text
soup = BeautifulSoup(content , 'lxml')
captcha = soup.find('img', id='captcha_image')

if captcha:
    captcha_url = captcha['src']
    re_captcha_id = r'<input type-"hidden" name="captcha-id" value="(.*?)"/'
    captcha_id = re.findall(re_captcha_id, content)
    print(captcha_id)
    print(captcha_url)
    captcha_text = input('Please input 验证码')
    formdata['captcha-solution'] = captcha_text
    formdata['captcha-id'] = captcha_id
    r = s.post(url_login,data = formdata,headers = headers)

'''
requrl = 'https://movie.douban.com/subject/' + '26862829' + '/comments'+'?'+'sort=new_score&status=P'
headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
requestURL = urllib.request.Request(url=requrl,headers=headers)
resp = urllib.request.urlopen(requestURL)
html_data = resp.read().decode('utf-8')
soup = BeautifulSoup(html_data,'lxml')
comment_div_list = soup.find_all('div',class_ = 'comment')

eachCommentList = []
for item in comment_div_list:
    if item.find_all('p')[0].string is not None:
        eachCommentList.append(item.find_all('p')[0].string)
next_ =  soup.find('a',{"class":"next"})
print(next_)

a_ = 0
while next_.attrs['href'] is not None:
    a_ += 1
    requrl = 'https://movie.douban.com/subject/' + '26862829' + '/comments' + next_.attrs["href"]
    requestURL = urllib.request.Request(url=requrl, headers=headers)
    resp = urllib.request.urlopen(requestURL)
    html_data = resp.read().decode('utf-8')
    soup = BeautifulSoup(html_data, 'lxml')
    comment_div_list = soup.find_all('div', class_='comment')
    print(a_)
    for item in comment_div_list:
        if item.find_all('p')[0].string is not None:
            eachCommentList.append(item.find_all('p')[0].string)

count = 0
for i in eachCommentList:
    count += 1
    print(count)
    print(i)





'''
def main():

    commentList = []
    for i in range(15):
        pagenum = i + 1
        commentList_temp = getComment(nowplaying_list[0]['id'], pagenum)
        commentList.append(commentList_temp)
    comments = ''
    for i in range(len(commentList)):
        comments = comments + (str(commentList[i])).strip()

    pattern = re.compile(r'[\u4e00-\u9fa5]+')
    filterdata = re.findall(pattern,comments)
    cleaned_comments = ''.join(filterdata)

    segment = jieba.lcut(cleaned_comments)
    words_df = pd.DataFrame({'segment':segment})

    stopwords = pd.read_csv("stopwords.txt",index_col=False,quoting=3,sep="\t",names=['stopword'], encoding='GBK')
    words_df = words_df[~words_df.segment.isin(stopwords.stopword)]

    words_stat = words_df.groupby(by=['segment'])['segment'].agg({"计数": numpy.size})
    words_stat = words_stat.reset_index().sort_values(by=["计数"], ascending=False)

    wordcloud = WordCloud(font_path="simhei.ttf", background_color="white", max_font_size=80)
    word_frequence = {x[0]: x[1] for x in words_stat.head(1000).values}

    word_frequence_list = []
    for key in word_frequence:
        temp = (key, word_frequence[key])
        word_frequence_list.append(temp)
    wordcloud = wordcloud.fit_words(dict(word_frequence_list))
    plt.imshow(wordcloud)
    pylab.show()


main()

'''