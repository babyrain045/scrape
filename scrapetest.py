from urllib.request import urlopen
from bs4 import BeautifulSoup
from getLinks import *
import datetime
import random
import re
import socket


random.seed(datetime.datetime.now())

def getLinks(articleUrl):
    NET_STATUS = False
    while not NET_STATUS:
        try:
            html = urlopen("http://en.wikipedia.org/wiki/Kevin_Bacon",timeout=5)
            bsObj = BeautifulSoup(html,"lxml")
            return bsObj.find("div",{"id":"bodyContent"}).findAll("a",href = re.compile("^(/wiki/)((?!:).)*$"))
        except socket.timeout:
            print("网页未响应")
            NET_STATUS = False

links = getLinks("/wiki/Kevin_Bacon")
while len(links) > 0:
    newArticle = links[random.randint(0, len(links)-1)].attrs["href"]
    print(newArticle)
    links = getLinks(newArticle)