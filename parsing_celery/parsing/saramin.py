import re

import os
from sailer.sailer import Sailer
from sailer.pacific import *
from sailer.utils import *
import random
import time

from .post_common import post_store, download_to_temp

LUNA_PACIFIC_ENDPOINT = "https://luna.devhi.me/pacific/post_store"

class SaraminSailer(Sailer):
    def start(self):
        activity_contest_array = ['outreach?saramin_category=C002', 'contests?saramin_category=C001']
        for self.activity_contest in activity_contest_array:
            for i in range(70):
                self.page_url = "http://contests.saramin.co.kr/{0}&state=3&page={1}".format(self.activity_contest,
                                                                                            i + 1)
                self.page()

    def page(self):
        self.go(self.page_url)
        self.contents = self.xpaths(r'//*[@id="content"]/div/div[2]/div[3]/table/tbody/tr[*]/td[2]/a')
        self.ddays = self.xpaths(r'//*[@id="content"]/div/div[2]/div[3]/table/tbody/tr[*]/td[4]')
        urls = []
        ddays = []
        for c, d in zip(self.contents, self.ddays):
            urls.append(c.get_attribute('href'))
            ddays.append(d.text.split('\n')[1].strip())
        for self.url, self.dday in zip(urls, ddays):
            self.data_parse()

    def data_parse(self):
        self.go(self.url)
        print(self.current_url)
        data_dic = {}
        if self.current_url.split('/')[3] == 'design':
            datas = self.xpaths(r'//*[@id="container"]/div[1]/div[1]/div[2]/div[1]/ul/li[*]')
            self.sub = self.xpath(r'//*[@id="container"]/div[1]/div[1]/div[1]').text.split('\n')[0].strip()
            self.detail = self.xpath(r'//*[@id="container"]/div[1]/div[1]/div[2]/div[2]').text
        else:
            datas = self.xpaths(r'//*[@id="content"]/div/div[2]/div[2]/div[1]/ul/li[*]')
            self.sub = self.xpath(r'//*[@id="content"]/div/div[2]/div[1]').text.split('\n')[0].strip()
            self.detail = self.xpath(r'//*[@id="content"]/div/div[2]/div[2]/div[2]').text

        for d in datas:
            if d.text == '':
                continue
            if d.text.split('\n')[0] == d.text.split('\n')[-1]:
                data_dic[d.text.split('\n')[0].strip()] = ''
            else:
                data_dic[d.text.split('\n')[0].strip()] = d.text.split('\n')[-1].strip()

        self.label = data_dic.get('공모분류', '')
        self.thumnail = self.xpath(r'//*[@id="imageZoomOut"]').get_attribute('src')
        self.host = data_dic.get('주최', '')
        self.start_date = data_dic.get('접수기간', '').split()[0]
        self.end_date = data_dic.get('접수기간', '').split()[2]
        self.start_date = convert_datetime(self.start_date, '%Y.%m.%d', '%Y-%m-%d')
        self.end_date = convert_datetime(self.end_date, '%Y.%m.%d', '%Y-%m-%d')
        print(self.thumnail)
        print(self.host)
        print(self.sub)
        print(self.start_date)
        print(self.end_date)
        self.target = data_dic.get('참가조건', '')
        self.benefit = data_dic.get('총 상금', '')
        try:
            regex = re.compile(r'홈페이지.*href="(?P<url>.*)" target')
            self.home_url = regex.search(self.html).group("url")
        except:
            self.home_url = ''
        print(self.home_url)

        self.files = download_to_temp(self.thumnail)
        post_store(self)

        time.sleep(random.randrange(5, 10))


srs = SaraminSailer()
srs.start()
srs.close()
