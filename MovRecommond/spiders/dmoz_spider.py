# -*- coding: utf-8 -*-
import scrapy
from scrapy.spider import BaseSpider
from MovRecommond.items import MovieItem
from lxml import etree
import requests

class DmozSpider(BaseSpider):
    name = "movspider"
    allowed_domains = []
    start_urls = ['http://www.dytt8.net/']

    def parse(self, response):
        a = 1
        for item in response.xpath('//*[@id="header"]/div/div[3]/div[2]/div[1]/div[2]/div[2]/ul/a'):

            mvUrl = item.xpath("@href").extract_first()
            mvName = item.xpath("text()").extract_first()
            print("--------------",mvUrl,mvName)

            yield scrapy.Request(url="http://www.dytt8.net%s"%(mvUrl),callback=self.parse_mor)



    def parse_mor(self, response):
        # 详情介绍页面
        mvname = response.xpath("//div[@class='title_all']//h1/font/text()").extract()
        mvdesc = response.xpath("//div[@class='co_content8']//p").extract()
        # 海报是个集合，包含2-3个图，一般第一个是大海报，后面的是剧照
        mvPoster = response.xpath("//div[@class='co_content8']//p/img/@src").extract()
        # 磁力下载链接，如果是个集合，列出
        mv_magnetUrl = response.xpath("//div[@class='co_content8']//p/a[contains(@href,'magnet')]/@href").extract_first()
        mvdtilte = "磁力下载"

        Item = MovieItem()
        Item['movClass'] = '最新电影'
        Item['downLoadName'] = mvname
        Item['downdtitle'] = str(mvdtilte)
        Item['downimgurl'] = str(mvPoster)
        Item['downLoadUrl'] = str(mv_magnetUrl)
        Item['mvdesc'] = str(mvdesc)

        yield Item