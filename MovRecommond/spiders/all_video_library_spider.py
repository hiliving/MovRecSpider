# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.spider import BaseSpider
from MovRecommond.items import MovieItem


# 电影港所有栏目下的资源，
class MostNewSpider(BaseSpider):
    name = "video_library_spider"
    allowed_domains = []
    start_urls = ['http://www.dygang.net/']

    def parse(self, response):
        head = response.xpath("/html/body/table[3]/tbody/tr/td/a")
        head.pop()
        head.pop(0)
        for item in head:

            mvClass = item.xpath("text()").extract()
            mvUrl = item.xpath("@href").extract_first()

            if mvUrl =='/':
                continue
            print("allvideolibrary",mvUrl)
            for index in range(0, 15):
                # 不爬帮助页，跳出循环
                if "help.html" in mvUrl:
                    break
                if index==0:
                    requestUrl = mvUrl
                else:
                    requestUrl = "%sindex_%s.htm" % (mvUrl,index + 1)
                # yield
                print('zhengzaipa',requestUrl)
                # yield

                yield scrapy.Request(url=requestUrl,meta={"mvclass":mvClass},callback=self.parse_mor)


    def parse_mor(self, response):
        # xpath('//tbody/tr/td//a[@class="classlinkclass"]/text()').extract() 电影名
        # response.xpath('//td[contains(@valign,"top")]/text()').extract() 简介
        mvClass = response.meta['mvclass']
        for item in response.xpath('//tbody/tr/td//a[@class="classlinkclass"]'):
            # 爬取5页，左开右闭
            mvUrl = item.xpath("@href").extract_first()#详情页地址
            print('---------------------哈哈哈哈------------------------------',mvClass)
            yield scrapy.Request(url=mvUrl, meta={"mvclass":mvClass},callback=self.parse_detail)
            # yield


            # yield
    # 解析并保存进数据库，这里为了方便，用工具类封装了一下，便于其他爬虫用此方法
    def parse_detail(self,response):
        # 详情介绍页面
        # 详情介绍页面
        mvClass = response.meta['mvclass']
        mvname =  response.xpath('//div[@class="title"]/a/text()').extract()
        mvdesc = response.xpath('//td[@id="dede_content"]/p/text()').extract()
        if len("".join(mvdesc).strip())==0:
            return
        # 海报是个集合，包含2-3个图，一般第一个是大海报，后面的是剧照
        mvPoster = response.xpath('//*[@id="dede_content"]/p/img/@src').extract()
        # 更新时间
        mv_time =  response.xpath("//table[@width='91%']//tr[2]/td/text()").extract_first()

        if len(mv_time):
            time = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", mv_time).group(0)
        else:
            time = "2018-07-5"
        mvdtilte = "磁力下载"

        mgnetUrl = response.xpath('//*[@id="dede_content"]/table//a[contains(@href,"magnet")]/@href').extract()
        mgnetName = response.xpath('//*[@id="dede_content"]/table//a[contains(@href,"magnet")]/text()').extract()

        ed2k = response.xpath('//td[@id="dede_content"]//a[contains(@href,"ed2k")]/@href').extract()
        ed2kName = response.xpath('//td[@id="dede_content"]//a[contains(@href,"ed2k")]/text()').extract()

        # 下载地址集合，第一个元素是磁力链，后面的是ftp，针对剧集类，磁力可能为空，ftp的是个集合
        downUrlList = []
        downTitleList=[]
        # 如果磁力地址不为空
        if len(mgnetUrl):
            downUrlList.extend(mgnetUrl)
            downTitleList.extend(mgnetName)
        else:
            if len(ed2k)==0:
                return
        if len(ed2k):
            downUrlList.extend(ed2k)
            downTitleList.extend(ed2kName)

        Item = MovieItem()
        Item['movClass'] = mvClass[0]
        Item['downLoadName'] = mvname
        Item['downdtitle'] = ','.join(downTitleList)
        Item['downimgurl'] = str(",".join(mvPoster))
        url = ','.join(downUrlList)
        Item['downLoadUrl'] = url
        Item['mvdesc'] ="".join(mvdesc).strip()
        Item['mv_update_time'] = time
        print('---------------save',downUrlList)
        yield Item
        # yield