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

class WevitySailer(Sailer):
    def start(self):
        activity_contest_array = ['active', 'find']
        for self.activity_contest in activity_contest_array:
            for i in range(70):
                self.page_url = "https://www.wevity.com/?c={0}&s=1&mode=ing&gp={1}".format(self.activity_contest, i + 1)
                self.page()

    def page(self):
        self.go(self.page_url)
        if self.activity_contest == 'active':
            self.contents = self.xpaths(r'//*[@id="container"]/div[2]/div[1]/div[2]/div[2]/ul/li[*]/a')
        else :
            self.contents = self.xpaths(r'//*[@id="container"]/div[2]/div[1]/div[2]/div[3]/div/ul/li[*]/div[1]/a')
        urls = []
        for c in self.contents:
            urls.append(c.get_attribute('href'))
        for self.url in urls:
            self.data_parse()

    def data_parse(self):
        self.go(self.url)
        print(self.url)
        data_dic = {}
        datas = self.xpaths(r'//*[@id="container"]/div[2]/div[1]/div[2]/div/div[2]/div[2]/ul/li[*]')
        for d in datas:
            if d.text == '':
                continue
            if d.text.split('\n')[0] == d.text.split('\n')[-1]:
                data_dic[d.text.split('\n')[0].strip()] = ''
            else:
                data_dic[d.text.split('\n')[0].strip()] = d.text.split('\n')[-1].strip()

        self.label = data_dic.get('분야', '')
        self.thumnail = self.xpath(
            r'//*[@id="container"]/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[1]/img').get_attribute('src')
        self.host = data_dic.get('주최/주관', '')
        self.sub = self.xpath(r'//*[@id="container"]/div[2]/div[1]/div[2]/div/div[1]/h6').text
        self.start_date = data_dic.get('접수기간', '').split()[0]
        self.end_date = data_dic.get('접수기간', '').split()[2]
        # self.dday = data_dic.get('접수기간', '').split()[3]
        # print(self.label)
        # print(self.thumnail)
        # print(self.host)
        # print(self.sub)
        # print(self.start_date)
        # print(self.end_date)
        self.target = data_dic.get('응모대상', '')
        self.benefit = data_dic.get('총 상금', '')
        self.detail = self.xpath(r'//*[@id="viewContents"]').text
        self.home_url = data_dic.get('홈페이지', '')
        print(self.home_url)
        poster_file = download_to_temp(self.thumnail)
        self.files = {'poster': poster_file}
        post_store(self)
        time.sleep(random.randrange(5, 10))


wvs = WevitySailer()
wvs.start()
wvs.close()
