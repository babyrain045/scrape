import requests
from bs4 import BeautifulSoup
import re

#使用ID和验证码登录
#第一次登录后获得登录后的COOKIES，在后面的信息自动带入登录时候的COOKIES即可
def login(username,password):
    url_login = 'http://accounts.douban.com/login'
    s = requests.Session()
    formdata = {'source':'index_nav',
            "Referer": "https://douban.com/accounts/login",
            "Host": "accounts.douban.com",
            "Connection": "Keep-Alive",
             'form_email':username,
             'form_password':password}
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    r = s.get(url_login,headers = headers)
    content = r.text
    soup = BeautifulSoup(content , 'lxml')
    captcha = soup.find('img', id='captcha_image')

    if captcha:
        captcha_url = captcha['src']
        re_captcha_id = r'<input type="hidden" name="captcha-id" value="(.*?)"/'
        captcha_id = re.findall(re_captcha_id, content)
        print(captcha_id)
        print(captcha_url)
        captcha_text = input('Please input 验证码')
        formdata['captcha-solution'] = captcha_text
        formdata['captcha-id'] = captcha_id
    r = s.post(url_login, data=formdata, headers=headers)
    cookies_ = r.cookies
    return cookies_




