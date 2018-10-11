# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.spider import BaseSpider
from MovRecommond.items import MovieItem


# 电影港最新栏目下的资源
class MostNewSpider(BaseSpider):
    name = "subject_spider"
    allowed_domains = []
    start_urls = ['http://www.dygang.net/dyzt/']

    def parse(self, response):
        # 当前页面，从第一页到第4页

        for index in range(0, 10):
            if index == 0:
                requestUrl = "http://www.dygang.net/dyzt/"
            else:
                requestUrl = "http://www.dygang.net/dyzt/index_%s.htm" % (index + 1)
            # yield
            print('zhengzaipa',requestUrl)
            yield scrapy.Request(url=requestUrl, callback=self.parse_mor)

    def parse_mor(self, response):
        for item in response.xpath('//tbody/tr/td//a[@class="classlinkclass"]'):
            mvUrl = item.xpath("@href").extract_first()#专题详情页地址
            mvName = item.xpath("text()").extract()#专题详情页标题
            print('---------------------哈哈哈哈2------------------------------',mvUrl)
            yield scrapy.Request(url=mvUrl,meta={"mvclass":mvName},callback=self.parse_subject_page)
            # yield
    # 进入专题页，获取影片列表
    def parse_subject_page(self, response):
        mvClass = response.meta['mvclass']
        for item in response.xpath('//td[@bgcolor="#ffffbb"]//a'):
            mvUrl = item.xpath("@href").extract_first()
            print('---------------------哈哈哈哈------------------------------', mvUrl)
            yield scrapy.Request(url=mvUrl,meta={"mvclass":mvClass},callback=self.parse_detail)

    # 解析并保存进数据库，这里为了方便，用工具类封装了一下，便于其他爬虫用此方法
    def parse_detail(self,response):

        # 分类名称，也就是专题名称
        mvClass = response.meta['mvclass']
        # 影片名称
        mvname = response.xpath("//div[@class='box']/h1/text()").extract_first()
        mvdesc =response.xpath("//div[@id='endText']//p/text()").extract()

        if len("".join(mvdesc).strip())==0:
            return
        # 海报是个集合，包含2-3个图，一般第一个是大海报，后面的是剧照
        mvPoster = response.xpath("//div[@id='endText']/p/img/@src").extract()
        # 更新时间，由于是专题，此字段没有意义
        mv_time = "2018-10-28"

        mgnetUrl = response.xpath("//div[@class='box']//a[contains(@href,'magnet')]/@href").extract()

        mgnetName = response.xpath("//div[@class='box']//a[contains(@href,'magnet')]/text()").extract()

        ed2k = response.xpath("//div[@class='box']//a[contains(@href,'ed2k')]/@href").extract()
        ed2kName = response.xpath("//div[@class='box']//a[contains(@href,'ed2k')]/text()").extract()
        # 下载地址集合，第一个元素是磁力链，后面的是ftp，针对剧集类，磁力可能为空，ftp的是个集合
        downUrlList = []
        downTitleList = []

        # 如果磁力地址不为空
        if len(mgnetUrl):
            downUrlList.extend(mgnetUrl)
            downTitleList.extend(mgnetName)
        else:
            if len(ed2k) == 0:
                return
        if len(ed2k):
            downUrlList.extend(ed2k)
            downTitleList.extend(ed2kName)
        Item = MovieItem()
        Item['movClass'] = mvClass
        Item['downLoadName'] = mvname
        Item['downdtitle'] = ','.join(downTitleList)
        Item['downimgurl'] = str(",".join(mvPoster))
        url = ','.join(downUrlList)
        Item['downLoadUrl'] = url
        Item['mvdesc'] = "".join(mvdesc).strip()
        Item['mv_update_time'] = mv_time
        print('---------------save', str(downUrlList))
        yield Item
        # yield