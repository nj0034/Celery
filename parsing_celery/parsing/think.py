import os
from sailer.sailer import Sailer
from sailer.pacific import *
from sailer.utils import *
import random
import time
import json

import requests

from .post_common import post_store, download_to_temp

LUNA_PACIFIC_ENDPOINT = "https://luna.devhi.me/pacific/post_store"
LOCAL_PACIFIC_ENDPOINT = "http://127.0.0.1:8000/pacific/post_store"

class ThinkSailer(Sailer):
    def start(self):
        for i in range(70):
            self.page_url = "http://www.thinkcontest.com/bbs/board.php?bo_table=sub4&category=all&searchState=3&page={}".format(
                i + 1)
            self.page()

    def page(self):
        self.go(self.page_url)
        self.contents = self.xpaths(
            r'//*[@id="fboardlist"]/table/tbody/tr[*]/td[1]/div[1]/a')
        self.ddays = self.xpaths(r'//*[@id="fboardlist"]/table/tbody/tr[*]/td[3]')
        urls = []
        ddays = []
        for c, d in zip(self.contents, self.ddays):
            urls.append(c.get_attribute('href'))
            ddays.append(d.text)
        for self.url, self.dday in zip(urls, ddays):
            self.data_parse()

    def data_parse(self):
        self.go(self.url)
        print(self.url)
        data_dic = {}
        indexs = self.xpaths(r'//*[@id="container_sub"]/div[2]/div[2]/div/div[3]/table/tbody/tr[*]/th')
        datas = self.xpaths(r'//*[@id="container_sub"]/div[2]/div[2]/div/div[3]/table/tbody/tr[*]/td')
        for i, d in zip(indexs, datas):
            data_dic[i.text.strip()] = d.text.strip()

        self.label = data_dic.get('응모분야', '')
        try:
            self.thumnail = self.xpath(r'//*[@id="poster_zoom"]').get_attribute('onclick').split('\'')[1].split('&wr_id')[0]
        except:
            self.thumnail = None
        self.host = data_dic.get('주최', '')
        self.sub = self.xpath(r'//*[@id="container_sub"]/div[2]/div[2]/h4').text.split('\n')[0]
        self.start_date = data_dic.get('접수기간', '').split()[0]
        self.end_date = data_dic.get('접수기간', '').split()[2]
        print(self.label)
        print(self.thumnail)
        print(self.host)
        print(self.sub)
        print(self.start_date)
        print(self.end_date)
        # print(self.dday)
        self.target = ''
        self.benefit = ''
        self.detail = self.xpath(r'//*[@id="container_sub"]/div[2]/div[2]/div/div[5]').text
        self.home_url = data_dic.get('홈페이지')
        print(self.home_url)

        poster_file = download_to_temp(self.thumnail)
        self.files = {'poster': poster_file}
        post_store(self)
        time.sleep(random.randrange(5, 10))


ths = ThinkSailer()
ths.start()
ths.close()
