
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup

import wget


def getURLInfo(webUrl):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/44.0.2403.157 Safari/537.36'}
    req = urllib.request.Request(url=webUrl, headers=header)
    response = urllib.request.urlopen(req, timeout=5)
    html = response.read().decode('gbk')

    if response.getcode() == 200:
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    return None

def getSearchPage(webInfo):
    """获取搜索的结果有多少页"""
    mapLink = {}
    tables = webInfo.findAll('td', attrs={'align': 'Center'})
    # print(tables)
    for tab in tables:
        txt = tab.text
        if len(txt) >= 10:
            startIndex = txt.rfind('为')
            endIndex = txt.find('页')
            pageCount = txt[int(startIndex + 1): int(endIndex)]
            return pageCount

    return 0

def getPageLinks(webInfo):
    mapLink = {}
    tables = webInfo.findAll('table', attrs={'bordercolordark': '#ffffff'})
    # print(tables)
    temp = tables[0]
    subTables = tables[0].findAll('div', attrs={'valign': 'middle'})

    mapDownInfo = {}
    # print(subTables[0])
    for item in subTables:
        title = item.text
        # title = item.text()
        href = item.find('a')
        urlDown = href.attrs['href']
        # print(title, urlDown)
        mapDownInfo[title] = urlDown

    return mapDownInfo


def getDownLink(urlDown):
    webInfo = getURLInfo(urlDown)

    if webInfo is None:
        return None

    TxtDiv = webInfo.find('div', attrs={'class': 'TxtDiv'})

    scoreTxt = TxtDiv.find('font', attrs={'color': '#CC0000'})
    score = scoreTxt.text
    if score != '0':
        return None

    p = TxtDiv.find('p')
    describe = p.text

    strExt = ''
    if describe.find('PSD') > -1:
        strExt = '_PSD'
    if describe.find('AI') > -1:
        strExt += '_AI'
    if describe.find('EPS') > -1:
        strExt += '_EPS'

    a = TxtDiv.find('a')
    url = a.attrs['href']

    return strExt, url


if __name__ == '__main__':
    keyWord = urllib.parse.quote('卡通')

    baseUrl = 'http://so.sccnn.com/search/' + keyWord + '/' + str(1) + '.html'
    webInfo = getURLInfo(baseUrl)
    pageCount = getSearchPage(webInfo)

    print(f'搜索到 {pageCount} 页')

    downCount = 0
    for pageNum in range(1, int(pageCount)):
        print(f'处理第 {pageNum} 页')
        baseUrl = 'http://so.sccnn.com/search/' + keyWord + '/' + str(pageNum) + '.html'
        webInfo = getURLInfo(baseUrl)

        if webInfo is not None:
            mapList = getPageLinks(webInfo)

            for key in mapList.keys():
                resInfos = getDownLink(mapList[key])
                if resInfos is not None:
                    name = key + resInfos[0]
                    urlDownload = resInfos[1]

                    dotIndex = urlDownload.rfind('.')
                    surf = urlDownload[dotIndex:]
                    path = 'F:/' + name + surf  # 保存的路径

                    print(f' {downCount} 即将下载: {urlDownload} \n\t 保存至: {path}')

                    wget.download(urlDownload, path)  # 下载
                    downCount += 1

    print(f'下载完成,共下载{downCount}个')

