import requests
from bs4 import BeautifulSoup
import lxml
import json
import requests_cache

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                         'AppleWebKit/537.11 (KHTML, like Gecko) '
                         'Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}


class feedToJSON:
    def __init__(self, url="", pageNo=-1, noItems=0, offset=0, s="",cacheFlag = True):
        self.url = url
        self.pageNo = pageNo
        self.noItems = noItems
        self.offset = offset
        self.s = s
        self.cacheFlag = cacheFlag

    def channelinfo(self):
        try:
            sourceinfo = dict()
            channelInfoReq = requests.get(self.url, headers=headers)
            if channelInfoReq.status_code == 200:
                channelsoup = BeautifulSoup(channelInfoReq.content, "xml")
                channelTitle = channelsoup.find('title')
                channelDesc = channelsoup.find('description')
                channelLink = channelsoup.find('link')
                imageFind = channelsoup.find('image')
                lastUpdated = channelsoup.find('lastBuildDate')
                sourceinfo['lastUpdated'] = '' if lastUpdated is None else lastUpdated.text.strip()
                try:
                    sourceinfo['link'] = '' if channelLink is None else channelLink['href'][:-5]
                except:
                    sourceinfo['link'] = ''
                sourceinfo['title'] = '' if channelTitle is None else channelTitle.text.strip()
                if imageFind is None:
                    sourceinfo['image'] = ''
                else:
                    try:
                        sourceinfo['image'] = imageFind.find('url').text.strip()
                    except:
                        sourceinfo['image'] = ""
                sourceinfo['desc'] = "" if channelDesc is None else channelDesc.text.strip()
                return sourceinfo

        except Exception as e:
            return {'error': str(e)}

    def getfeed(self):
        params = {}
        feedlist = list()
        if self.pageNo > 0:
            params['paged'] = self.pageNo
        if self.s != "":
            params['s'] = self.s
        try:
            if self.cacheFlag == True:
                feedreq = requests.get(self.url, headers=headers, params=params)
            else:
                with requests_cache.disabled():
                    feedreq = requests.get(self.url, headers=headers, params=params)
        except Exception as e:
            print(str(e))
            return {'error': str(e)}
        feedsoup = BeautifulSoup(feedreq.content, 'xml')
        items = feedsoup.findAll('item')
        items = items if self.offset == 0 else items[self.offset - 1:]
        items = items if self.noItems == 0 else items[0:self.noItems]
        for item in items:
            newsd = dict()
            tags = list()
            title = item.find('title')
            link = item.find('link')
            description = item.find('description')
            descsoup = BeautifulSoup(description.text, 'lxml')
            categories = item.findAll('category')
            publishedDate = item.find('pubDate')
            author = item.find('creator')
            newsd['title'] = '' if title is None else title.text.strip()
            newsd['link'] = '' if link is None else link.text.strip()
            imgfind = descsoup.find('img')
            newsd['image'] = '' if imgfind is None else imgfind['src']
            newsd['fulldesc'] = description.text
            for el in ['div', 'img', 'a']:
                for p in descsoup.findAll(el):
                    p.extract()
            newsd['desc'] = '' if description is None else descsoup.text.strip()
            for category in categories:
                tags.append(category.text.lower())
            newsd['tags'] = tags
            newsd['published'] = '' if publishedDate is None else publishedDate.text.strip()
            newsd['author'] = '' if author is None else author.text.strip()
            feedlist.append(newsd)
        return feedlist
