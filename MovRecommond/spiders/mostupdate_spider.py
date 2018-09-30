# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.spider import BaseSpider
from MovRecommond.items import MovieItem


# 电影港最新栏目下的资源
class MostNewSpider(BaseSpider):
    name = "dygangspider"
    allowed_domains = []
    start_urls = ['http://www.dygang.net/ys/']

    def parse(self, response):
        # 当前页面，从第一页到第4页

        for index in range(0, 5):
            if index == 0:
                requestUrl = "http://www.dygang.net/ys/"
            else:
                requestUrl = "http://www.dygang.net/ys/index_%s.htm" % (index + 1)
            # yield
            print('zhengzaipa',requestUrl)
            yield scrapy.Request(url=requestUrl, callback=self.parse_mor)

    def parse_mor(self, response):
        # xpath('//tbody/tr/td//a[@class="classlinkclass"]/text()').extract() 电影名
        # response.xpath('//td[contains(@valign,"top")]/text()').extract() 简介
        for item in response.xpath('//tbody/tr/td//a[@class="classlinkclass"]'):
            # 爬取5页，左开右闭
            mvUrl = item.xpath("@href").extract_first()#详情页地址
            print('---------------------哈哈哈哈------------------------------',mvUrl)
            yield scrapy.Request(url=mvUrl, callback=self.parse_detail)
            # yield


            # yield
    # 解析并保存进数据库，这里为了方便，用工具类封装了一下，便于其他爬虫用此方法
    def parse_detail(self,response):
        # 详情介绍页面
        # 详情介绍页面
        mvname = response.xpath("//td[@class ='table-title']/div/a/text()").extract_first()
        mvdesc = response.xpath('//td[@id="dede_content"]/p/text()').extract()
        if len("".join(mvdesc).strip())==0:
            return
        # 海报是个集合，包含2-3个图，一般第一个是大海报，后面的是剧照
        mvPoster = response.xpath('//*[@id="dede_content"]/p/img/@src').extract()
        # 更新时间
        mv_time =  response.xpath("//td[@width='132']//td/text()").extract()
        if len(mv_time):
            time = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", mv_time).group(0)
        else:
            time = "2018-07-5"
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
        Item['mv_update_time'] = time
        print('---------------save',downUrlList)
        yield Item
        # yield