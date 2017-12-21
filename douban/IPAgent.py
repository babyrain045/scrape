
import urllib
from urllib import request
from bs4 import BeautifulSoup
import socket
from urllib.request import ProxyHandler,build_opener

socket.setdefaulttimeout(3)

def get_IPAgent():
    User_Agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    header = {'User-Agent':User_Agent}


    url = 'http://www.xicidaili.com/nn/1'
    req = urllib.request.Request(url,headers = header)
    res = urllib.request.urlopen(req).read()

    soup = BeautifulSoup(res,'lxml')
    ips = soup.findAll('tr')
    f = open('src/proxy','w')


    for i in range(1,len(ips)):
        ip = ips[i]
        tds = ip.findAll("td")
        ip_temp = tds[1].contents[0] + "\t" + tds[2].contents[0] + "\n"
        f.write(ip_temp)

    f.close()
    f = open('src/proxy','r')
    lines = f.readlines()
    proxys = []


    for i in range(0,len(lines)):
        ip = lines[i].strip("\n").split("\t")
        proxy_host = "http://" + ip[0] + ":" + ip[1]
        proxy_temp = {"http":proxy_host}
        proxys.append(proxy_temp)
    print("已获得高匿IP，并存放与src目录中")
    return proxys


'''
#测试代理IP是否可以使用
url = "http://ip.chinaz.com/getip.aspx"
for i in proxys:
    try:
        Proxy_Handler = ProxyHandler(i)
        opener = build_opener(Proxy_Handler)
        response = opener.open(url)
        print(response.read().decode('utf-8'))
    except Exception as e :
        print(i)
        print(e)
        continue
'''