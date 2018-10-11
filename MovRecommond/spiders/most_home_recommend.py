# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.spider import BaseSpider
from MovRecommond.items import MovieItem
import time

# 电影港最新栏目下的资源
class MostNewSpider(BaseSpider):
    name = "homespider"
    allowed_domains = []
    start_urls = ['http://www.dygang.net/']

    def parse(self, response):
        # 当前页面，从第一页到第4页
        requestUrl = "http://www.dygang.net/"
        yield scrapy.Request(url=requestUrl, callback=self.parse_mor)


    def parse_mor(self, response):
        for item in response.xpath("//div[@id='tab1_div_0']//a[@class='c2']"):
            mvUrl = item.xpath("@href").extract_first()#详情页地址
            print('---------------------哈哈哈哈------------------------------',mvUrl)
            yield scrapy.Request(url=mvUrl, callback=self.parse_detail)

    # 解析并保存进数据库，这里为了方便，用工具类封装了一下，便于其他爬虫用此方法
    def parse_detail(self,response):
        # 详情介绍页面
        response.xpath('//div[@class="title"]/a/text()').extract()
        mvname = response.xpath('//div[@class="title"]/a/text()').extract()
        mvdesc = response.xpath('//td[@id="dede_content"]/p/text()').extract()
        if len("".join(mvdesc).strip())==0:
            return
        # 海报是个集合，包含2-3个图，一般第一个是大海报，后面的是剧照
        mvPoster = response.xpath('//*[@id="dede_content"]/p/img/@src').extract()

        mvTime = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        mvdtilte = "磁力下载"

        mgnetUrl = response.xpath('//*[@id="dede_content"]/table//a[contains(@href,"magnet")]/@href').extract()
        ed2k = response.xpath('//*[@id="dede_content"]/table//a[contains(@href,"ed2k")]/@href').extract()
        ed2k_name = response.xpath('//*[@id="dede_content"]/table//a[contains(@href,"ed2k")]/text()').extract()
        # 下载地址集合，第一个元素是磁力链，后面的是ftp，针对剧集类，磁力可能为空，ftp的是个集合
        downUrlList = []
        # 如果磁力地址不为空
        if len(mgnetUrl):
            downUrlList.extend(mgnetUrl)
        else:
            if len(ed2k)==0:
                return
        if len(ed2k):
            downUrlList.extend(ed2k)

        Item = MovieItem()
        Item['movClass'] = '最新电影'
        Item['downLoadName'] = mvname
        Item['downdtitle'] = str(mvdtilte)
        Item['downimgurl'] = str(",".join(mvPoster))
        url = ','.join(downUrlList)
        Item['downLoadUrl'] = url
        Item['mvdesc'] ="".join(mvdesc).strip()
        Item['mv_update_time'] = mvTime
        print('---------------save',downUrlList)
        yield Item
        # yield