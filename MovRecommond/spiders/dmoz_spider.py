# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.spider import BaseSpider
from MovRecommond.items import MovieItem



class DmozSpider(BaseSpider):
    name = "movspider"
    allowed_domains = []
    start_urls = ['http://www.dytt8.net/']

    def parse(self, response):
        a = 1
        for item in response.xpath('//*[@id="header"]/div/div[3]/div[2]/div[1]/div[2]/div[2]/ul/a'):

            mvUrl = item.xpath("@href").extract_first()
            mvName = item.xpath("text()").extract_first()

            yield scrapy.Request(url="http://www.dytt8.net%s"%(mvUrl),callback=self.parse_mor)



    def parse_mor(self, response):
        # 详情介绍页面
        mvname = response.xpath("//div[@class='title_all']//h1/font/text()").extract()
        mvdesc = response.xpath("//div[@class='co_content8']//p/text()").extract()

        if len(mvdesc):
            print("")
        else:
            mvdesc = response.xpath("//div[@class='co_content8']//div[@id='Zoom']//text()").extract()
        # 海报是个集合，包含2-3个图，一般第一个是大海报，后面的是剧照
        if len("".join(mvdesc).strip())==0:
            mvdesc = response.xpath("//div[@class='co_content8']//div[@id='Zoom']//text()").extract()

        if len("".join(mvdesc).strip())==0:
            return

        # 海报是个集合，包含2-3个图，一般第一个是大海报，后面的是剧照
        mvPoster = response.xpath("//div[@class='co_content8']//p/img/@src").extract()
        # 磁力下载链接，如果是个集合，列出
        mv_magnetUrl = response.xpath("//div[@class='co_content8']//p/a[contains(@href,'magnet')]/@href").extract()
        # ftp下载
        mv_ftp_name = response.xpath("//div[@class='co_content8']//table//a/text()").extract()
        # 分集的下载地址
        mv_ftp = response.xpath("//div[@class='co_content8']//table//a/@href").extract()
        # 更新时间
        mv_time = response.xpath("//div[@class='co_content8']//ul/text()").extract_first().strip()
        time = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", mv_time).group(0)

        mvdtilte = "磁力下载"
        # 下载地址集合，第一个元素是磁力链，后面的是ftp，针对剧集类，磁力可能为空，ftp的是个集合
        downUrlList = []
        # 如果磁力地址不为空
        if len(mv_magnetUrl):
            downUrlList.extend(mv_magnetUrl)
        else:
            if len(mv_ftp):
                print('')
            else:
                return
        # 如果下载地址不为空
        if len(downUrlList):
            downUrlList.extend(mv_ftp)
        Item = MovieItem()
        Item['movClass'] = '热门推荐'
        Item['downLoadName'] = mvname
        Item['downdtitle'] = str(mvdtilte)
        Item['downimgurl'] = str("".join(mvPoster))
        url = ','.join(downUrlList)
        Item['downLoadUrl'] = url
        Item['mvdesc'] = "".join(mvdesc).strip()
        Item['mv_update_time'] = time
        yield Item