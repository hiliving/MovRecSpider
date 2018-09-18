# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

from twisted.enterprise import adbapi
import pymysql
from MovRecommond import settings
class MoviePipeline(object):

    def __init__(self):

        # 连接数据库
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()
        print('数据库连接，----------------------------连接成功-------------------------------------')

    def process_item(self, item, spider):

        if spider.name=='movspider':

            try:
                # 插入数据
                # 查重处理
                self.cursor.execute(
                    """select * from mov_rec where downLoadName = %s""",
                    item['downLoadName'])
                # 是否有重复数据
                repetition = self.cursor.fetchone()
                # 重复
                if repetition is not None:
                    #结果返回，已存在，则不插入
                    pass
                else:
                        # 提交sql语句
                    self.cursor.execute(
                        """insert into mov_rec(movClass, downLoadName, downLoadUrl, mvdesc,downimgurl,downdtitle,mv_update_time )
                        value (%s, %s, %s, %s, %s, %s, %s)""",
                        (item['movClass'],
                         item['downLoadName'],
                         item['downLoadUrl'],
                         item['mvdesc'],
                         item['downimgurl'],
                         item['downdtitle'],
                         item['mv_update_time']
                         ))
                    self.connect.commit()
                    print('插入数据库，----------------------------插入完成-------------------------------------')
            except Exception as error:
                print('插入数据库，--------插入出错----------------',str(error))
                return item
        elif spider.name =='latestmovie':
            try:
                # 插入数据
                # 查重处理
                self.cursor.execute(
                    """select * from mov_update where downLoadName = %s""",
                    item['downLoadName'])
                # 是否有重复数据
                repetition = self.cursor.fetchone()
                # 重复
                if repetition is not None:
                    #结果返回，已存在，则不插入
                    print('插入数据库，----------------------------已存在，则不插入-------------------------------------')
                    pass
                else:
                        # 提交sql语句
                    self.cursor.execute(
                        """insert into mov_update(movClass, downLoadName, downLoadUrl, mvdesc,downimgurl,downdtitle,mv_update_time )
                        value (%s, %s, %s, %s, %s, %s, %s)""",
                        (item['movClass'],
                         item['downLoadName'],
                         item['downLoadUrl'],
                         item['mvdesc'],
                         item['downimgurl'],
                         item['downdtitle'],
                         item['mv_update_time']
                         ))
                    self.connect.commit()
                    print('插入数据库，----------------------------插入完成-------------------------------------')
            except Exception as error:
                print('插入数据库，--------插入出错----------------',str(error))
                return item
        elif spider.name=="dygangspider":
            try:
                # 插入数据
                # 查重处理
                self.cursor.execute(
                    """select * from mov_update where downLoadName = %s""",
                    item['downLoadName'])
                # 是否有重复数据
                repetition = self.cursor.fetchone()
                # 重复
                if repetition is not None:
                    #结果返回，已存在，则不插入
                    print('插入数据库，----------------------------已存在，则不插入-------------------------------------')
                    pass
                else:
                        # 提交sql语句
                    self.cursor.execute(
                        """insert into mov_update(movClass, downLoadName, downLoadUrl, mvdesc,downimgurl,downdtitle,mv_update_time )
                        value (%s, %s, %s, %s, %s, %s, %s)""",
                        (item['movClass'],
                         item['downLoadName'],
                         item['downLoadUrl'],
                         item['mvdesc'],
                         item['downimgurl'],
                         item['downdtitle'],
                         item['mv_update_time']
                         ))
                    self.connect.commit()
                    print('插入数据库，----------------------------插入完成-------------------------------------')
            except Exception as error:
                print('插入数据库，--------插入出错----------------',str(error))
                return item
        elif spider.name=="video_library_spider":
            try:
                # 插入数据
                # 查重处理
                self.cursor.execute(
                    """select * from mov_host_library where downLoadName = %s""",
                    item['downLoadName'])
                # 是否有重复数据
                repetition = self.cursor.fetchone()
                # 重复
                if repetition is not None:
                    #结果返回，已存在，则不插入
                    print('插入数据库，----------------------------已存在，则不插入-------------------------------------')
                    pass
                else:
                        # 提交sql语句
                    self.cursor.execute(
                        """insert into mov_host_library(movClass, downLoadName, downLoadUrl, mvdesc,downimgurl,downdtitle,mv_update_time )
                        value (%s, %s, %s, %s, %s, %s, %s)""",
                        (item['movClass'],
                         item['downLoadName'],
                         item['downLoadUrl'],
                         item['mvdesc'],
                         item['downimgurl'],
                         item['downdtitle'],
                         item['mv_update_time']
                         ))
                    self.connect.commit()
                    print('插入数据库，----------------------------插入完成-------------------------------------')
            except Exception as error:
                print('插入数据库，--------插入出错----------------',str(error))
                return item
        elif spider.name=="homespider":
            try:
                # 插入数据
                # 查重处理
                self.cursor.execute(
                    """select * from mov_update where downLoadName = %s""",
                    item['downLoadName'])
                # 是否有重复数据
                repetition = self.cursor.fetchone()
                # 重复
                if repetition is not None:
                    #结果返回，已存在，则不插入
                    print('插入数据库，----------------------------已存在，则不插入-------------------------------------')
                    pass
                else:
                        # 提交sql语句
                    self.cursor.execute(
                        """insert into mov_update(movClass, downLoadName, downLoadUrl, mvdesc,downimgurl,downdtitle,mv_update_time )
                        value (%s, %s, %s, %s, %s, %s, %s)""",
                        (item['movClass'],
                         item['downLoadName'],
                         item['downLoadUrl'],
                         item['mvdesc'],
                         item['downimgurl'],
                         item['downdtitle'],
                         item['mv_update_time']
                         ))
                    self.connect.commit()
                    print('插入数据库，----------------------------插入完成-------------------------------------')
            except Exception as error:
                print('插入数据库，--------插入出错----------------',str(error))
                return item