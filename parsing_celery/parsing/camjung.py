import re

import os
from sailer.sailer import Sailer
from sailer.pacific import *
from sailer.utils import *
import random
import time

from .post_common import post_store, download_to_temp

LUNA_PACIFIC_ENDPOINT = "https://luna.devhi.me/pacific/post_store"


class CamjungSailer(Sailer):
    def start(self):
        activity_contest_array = ['active', 'contest']
        for self.activity_contest in activity_contest_array:
            for i in range(4):
                self.page_url = "http://campus.jungle.co.kr/{}_list.asp?ipage={}&vSoOpt=C&vCateSub=#1".format(
                    self.activity_contest, i + 1)
                self.page()

    def page(self):
        self.go(self.page_url)
        urls = []
        dates = []

        if self.activity_contest == 'active':
            self.contents = self.xpaths(
                r'/html/body/table[2]/tbody/tr/td[2]/table[7]/tbody/tr/td/table[1]/tbody/tr/td/table/tbody/tr[*]/td[1]/a')
            self.dates = self.xpaths(
                r'/html/body/table[2]/tbody/tr/td[2]/table[7]/tbody/tr/td/table[1]/tbody/tr/td/table/tbody/tr[*]/td[5]')
            for c, d in zip(self.contents, self.dates):
                urls.append(c.get_attribute('onclick').split('\'')[1])
                dates.append(d.text)
            for self.url in urls:
                self.url = 'http://campus.jungle.co.kr/' + self.url
                self.data_parse()

        else:
            self.contents = self.xpaths(
                r'/html/body/table[2]/tbody/tr/td[2]/table[10]/tbody/tr/td/table[1]/tbody/tr/td/table/tbody/tr[*]/td[1]/a')
            self.dates = self.xpaths(
                r'/html/body/table[2]/tbody/tr/td[2]/table[10]/tbody/tr/td/table[1]/tbody/tr/td/table/tbody/tr[*]/td[5]')
            for c, d in zip(self.contents, self.dates):
                urls.append(c.get_attribute('href'))
                dates.append(d.text)
            for self.url in urls:
                self.data_parse()

    def data_parse(self):
        self.url = self.url.replace(' ', '')
        print(self.url)
        self.go(self.url)
        data_dic = {}
        datas = self.xpaths(
            r'/html/body/table[2]/tbody/tr/td[2]/table/tbody/tr/td/table[1]/tbody/tr[2]/td[3]/table[5]/tbody/tr/td[2]/table/tbody/tr[*]/td')
        for d in datas:
            if d.text == '':
                continue
            # if d.text.split()[0].strip() == '홈페이지':
            #     data_dic[d.text.split(':')[0].strip()] = d.text.split()[-1].strip()
            else:
                data_dic[d.text.split(':')[0].strip()] = d.text.split(':')[1].strip()

        # self.label = data_dic.get('분야', '')
        self.thumnail = self.xpath(r'//*[@id="clickimg"]').get_attribute('src')
        self.host = self.xpath(
            r'/html/body/table[2]/tbody/tr/td[2]/table/tbody/tr/td/table[1]/tbody/tr[2]/td[3]/table[4]/tbody/tr[1]/td[1]').text.split('주최 : ')[1]
        self.sub = self.xpath(
            r'/html/body/table[2]/tbody/tr/td[2]/table/tbody/tr/td/table[1]/tbody/tr[2]/td[3]/table[3]/tbody/tr/td[1]/strong').text
        self.start_date = data_dic.get('접수기간', '').split('~')[0].strip()
        self.end_date = data_dic.get('접수기간', '').split('~')[1].split('(')[0].strip()
        self.start_date = convert_datetime(self.start_date, '%Y/%m/%d', '%Y-%m-%d')
        self.end_date = convert_datetime(self.end_date, '%Y/%m/%d', '%Y-%m-%d')
        # self.dday = data_dic.get('접수기간', '').split('(')[1].split(')')[0]
        # if self.dday == '마감':
        #     quit()
        # print(self.label)
        print(self.thumnail)
        print(self.host)
        print(self.sub)
        print(self.start_date)
        print(self.end_date)
        # print(self.dday)
        self.target = ''
        self.benefit = ''
        self.detail = self.xpath(
            r'/html/body/table[2]/tbody/tr/td[2]/table/tbody/tr/td/table[1]/tbody/tr[2]/td[3]/table[7]/tbody/tr/td').text
        try:
            regex = re.compile(r'홈페이지 :<\/strong>.*"(?P<url>.*)"\s')
            self.home_url = regex.search(self.html).group("url")
        except:
            self.home_url = ''
        print(self.home_url)

        self.files = download_to_temp(self.thumnail)
        post_store(self)

        # for img_url, img_name in zip(self.thumnail, self.thumnail_name):
        #     download(img_url, 'tmp/' + img_name)
        #     store_file(uuid=res['uuid'], files=['tmp/' + img_name])

        time.sleep(random.randrange(5, 10))


cms = CamjungSailer()
cms.start()
cms.close()
