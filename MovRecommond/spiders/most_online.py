# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.spider import BaseSpider
from MovRecommond.items import MovieItem
import time

# 66影视在线播放的资源，包含下载地址
class MostNewSpider(BaseSpider):
    name = "online_spider"
    allowed_domains = []
    start_urls = ['https://www.66s.cc/']

    def parse(self, response):
        listHead = response.xpath("//div[@class='topnav']/ul/li")
        # 去掉第一个元素，去掉最后两个元素
        listHead.pop(0)
        listHead.pop()
        listHead.pop()

        for item in listHead:

            requestUrl = item.xpath("a/@href").extract_first()
            for index in range(0,160):
                if index==0:
                    mvUrl = requestUrl
                    print("----------url-------------", mvUrl)
                    mvClass = item.xpath("a/text()").extract_first()
                    yield scrapy.Request(url=mvUrl, meta={"currentUrl": requestUrl, "mvClass": mvClass},
                                         callback=self.parse_mor)
                else:
                    mvUrl = "%sindex_%s.html" % (requestUrl,index + 1)
                    print("----------url-------------",mvUrl)
                    mvClass = item.xpath("a/text()").extract_first()
                    yield scrapy.Request(url=mvUrl,meta={"currentUrl":requestUrl,"mvClass":mvClass}, callback=self.parse_mor)


    def parse_mor(self, response):

        currentUrl = response.meta['currentUrl']
        mvClass = response.meta['mvClass']

        for item in response.xpath("//div[@class='thumbnail']"):
            # 爬取5页，左开右闭
            mvUrl = item.xpath("a/@href").extract_first()
            print("---------------------gggg------------------------------", mvUrl)
            if "http" in mvUrl:
                print('---')
            else:
                mvUrl = "https://www.66s.cc" + mvUrl
                print("---------------------gggg22------------------------------", mvUrl)
            yield scrapy.Request(url=mvUrl, meta={"mvClass": mvClass}, callback=self.parse_detail)
            # yield


    # 解析并保存进数据库，这里为了方便，用工具类封装了一下，便于其他爬虫用此方法
    def parse_detail(self,response):

        mvClass = response.meta['mvClass']
        # 详情介绍页面
        mvname = response.xpath("//div[@class='mainleft']//h1/text()").extract_first()
        mvdesc = response.xpath("//div[@id='post_content']/p/text()").extract()
        if len("".join(mvdesc).strip())==0:
            return
        # 海报是个集合，包含2-3个图，一般第一个是大海报，后面的是剧照
        mvPoster = response.xpath("//div[@id='post_content']/p/img/@src").extract()

        mvTime =response.xpath("//span[@class='info_date info_ico']/text()").extract_first()
        mvdtilte = "磁力下载"

        mgnetUrl = response.xpath("//div[@id='post_content']//a[contains(@href,'magnet')]/@href").extract()
        mgnetName = response.xpath("//div[@id='post_content']//a[contains(@href,'magnet')]/text()").extract()
        ed2k =response.xpath("//div[@id='post_content']//a[contains(@href,'ed2k')]/@href").extract()
        ed2k_name = response.xpath("//div[@id='post_content']//a[contains(@href,'ed2k')]/text()").extract()
        # 下载地址集合，第一个元素是磁力链，后面的是ftp，针对剧集类，磁力可能为空，ftp的是个集合
        downUrlList = []
        downTitleList =[]
        # 如果磁力地址不为空
        if len(mgnetUrl):
            downUrlList.extend(mgnetUrl)
            downTitleList.extend(mgnetName)
        else:
            if len(ed2k)==0:
                return
        if len(ed2k):
            downUrlList.extend(ed2k)
            downTitleList.extend(ed2k_name)
        #在线播放地址
        mvPlayUrl = response.xpath("//div[@class='widget box row'][2]/a[@class='lBtn']/@href").extract()
        mvPlayName = response.xpath("//div[@class='widget box row'][2]/a[@class='lBtn']/text()").extract()
        Item = MovieItem()
        Item['movClass'] =mvClass
        Item['downLoadName'] = mvname
        Item['downdtitle'] =','.join(downTitleList)
        Item['downimgurl'] = str(",".join(mvPoster))
        url = ','.join(downUrlList)
        Item['downLoadUrl'] = url
        Item['mvdesc'] ="".join(mvdesc).strip()
        Item['mv_update_time'] = mvTime
        Item['playUrl'] =','.join(mvPlayUrl)
        Item['playName'] =','.join(mvPlayName)
        if len(mvPlayUrl)==0:
            print("---------------","无在线播放地址")
            pass
            yield
        else:
            print('---------------save',','.join(mvPlayUrl),'-------',','.join(mvPlayName))
            yield Item