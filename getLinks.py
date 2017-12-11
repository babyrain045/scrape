from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
#获取网站上面的所有链接（外链，内链）
def getInternalLinks(bsObj, includeUrl):
    includeUrl = urlparse(includeUrl).scheme+"://"+urlparse(includeUrl).netloc
    internalLinks = []
    for link in bsObj.findAll("a", href = re.compile("^(/|.*"+includeUrl+")")):
        if link.attrs['href'] is not None:
            if (link.attrs['href'].startswith("/")):
                internalLinks.append(includeUrl + link.attrs['href'])
            else:
                internalLinks.append(link.attrs['href'])
    return internalLinks

def getExternalLinks(bsObj, externalUrl):
    externalLinks = []
    for link in bsObj.findAll("a", href = re.compile("^(http|www)((?!"+externalUrl+").)*$")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
    return externalLinks

def splitAddress(address):
    addressParts = address.replace("http://", "").split("/")
    return addressParts
