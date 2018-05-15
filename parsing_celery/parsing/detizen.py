import re

import os
from sailer.sailer import Sailer
from sailer.pacific import *
from sailer.utils import *
import random
import time

from .post_common import post_store, download_to_temp

LUNA_PACIFIC_ENDPOINT = "https://luna.devhi.me/pacific/post_store"

class DetizenSailer(Sailer):
    def start(self):
        activity_contest_array = ['activity', 'contest']
        for activity_contest in activity_contest_array:
            for i in range(70):
                self.page_url = "http://www.detizen.com/{0}/?Category=3&IngYn=Y&PC={1}".format(activity_contest, i + 1)
                self.page()

    def page(self):
        self.go(self.page_url)
        self.contents = self.xpaths(r'//*[@id="Main"]/section[2]/div/ul/li[*]/div[1]/h4/a[1]')
        self.ddays = self.xpaths(r'//*[@id="Main"]/section[2]/div/ul/li[*]/div[1]/p/span')
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
        indexs = self.xpaths(r'//*[@id="Main"]/section[2]/div/div/div[2]/div[2]/table/tbody/tr[*]/th')
        datas = self.xpaths(r'//*[@id="Main"]/section[2]/div/div/div[2]/div[2]/table/tbody/tr[*]/td')

        for i, d in zip(indexs, datas):
            data_dic[i.text] = d.text

        self.label = data_dic.get('분야', '')
        print(self.label)
        try:
            self.thumnail = self.xpath(r'//*[@id="Main"]/section[2]/div/div/div[2]/div[1]/div/a').get_attribute('href')
        except:
            self.thumnail = None
        self.host = data_dic.get('주최', '')
        self.sub = self.xpath(r'//*[@id="Main"]/section[2]/header/h3/span[1]').text
        self.start_date = data_dic.get('기간', '').split()[0].strip()
        self.end_date = data_dic.get('기간', '').split()[2].strip()
        self.start_date = convert_datetime(self.start_date, '%Y.%m.%d', '%Y-%m-%d')
        self.end_date = convert_datetime(self.end_date, '%Y.%m.%d', '%Y-%m-%d')
        print(self.thumnail)
        print(self.host)
        print(self.sub)
        print(self.start_date)
        print(self.end_date)
        # print(self.dday)
        self.target = data_dic.get('대상', '')
        self.benefit = data_dic.get('특전', '')
        self.detail = self.xpath(r'//*[@id="Main"]/section[2]/div/div/ul').text
        try:
            regex = re.compile(r'홈페이지<\/th>\s*<td>.+href="(?P<url>.+)"\s')
            self.home_url = regex.search(self.html).group("url")
        except:
            self.home_url = ''
        print(self.home_url)

        self.files = download_to_temp(self.thumnail)
        post_store(self)
        time.sleep(random.randrange(5, 10))


dets = DetizenSailer()
dets.start()
dets.close()
