import re

import os
from sailer.sailer import Sailer
from sailer.pacific import *
from sailer.utils import *
import random
import time

from .post_common import post_store, download_to_temp

LUNA_PACIFIC_ENDPOINT = "https://luna.devhi.me/pacific/post_store"

class CampusmonSailer(Sailer):
    def start(self):
        field_code_dic = {'B': 7, 'A': 16}  # B: 대외활동, A: 공모전
        for code in field_code_dic:
            for num in range(field_code_dic[code]):
                for i in range(20):
                    self.page_url = "http://campusmon.jobkorea.co.kr/Contest/List?_Page={0}&_Tot_Cnt=1646&_Field_Code={1}00{2}".format(i + 1, code, num+1)
                    self.page()

    def page(self):
        self.go(self.page_url)
        print(self.page_url)
        try:
            self.xpath(r'//*[@id="contents"]/div[3]')   # 주목할만한 공모전 테이블이 있을 때
            self.contents = self.xpaths(r'//*[@id="contents"]/div[3]/table/tbody/tr[*]/td[1]/p[1]/a')
            self.states = self.xpaths(r'//*[@id="contents"]/div[3]/table/tbody/tr[*]/td[4]/span')
        except:
            self.contents = self.xpaths(r'//*[@id="contents"]/div[2]/table/tbody/tr[*]/td[1]/p[1]/a')
            self.states = self.xpaths(r'//*[@id="contents"]/div[2]/table/tbody/tr[*]/td[4]/span')
        urls = []
        states = []
        for c, s in zip(self.contents, self.states):
            urls.append(c.get_attribute('href'))
            states.append(s.text)
        for self.url, self.state in zip(urls, states):
            if self.state == '마감':
                break
            self.data_parse()

    def data_parse(self):
        self.go(self.url)
        print(self.url)
        data_dic = {}
        indexs = self.xpaths(r'//*[@id="container"]/div[2]/div/div[1]/ul/li[*]/strong')
        datas = self.xpaths(r'//*[@id="container"]/div[2]/div/div[1]/ul/li[*]/span')

        for i, d in zip(indexs, datas):
            data_dic[i.text] = d.text

        # labels = self.xpaths(r'//*[@id="container"]/div[2]/div/div[2]/div[4]/ul/li[*]/a')
        # self.label = []
        # for l in labels:
        #     self.label.append(l.text)

        try:
            self.thumnail = self.xpath(r'//*[@id="Image_poster"]').get_attribute('src')
        except:
            self.thumnail = None
        self.host = data_dic.get('주최', '')
        self.sub = self.xpath(r'//*[@id="container"]/div[2]/h3').text
        self.start_date = self.xpath(r'//*[@id="container"]/p[1]/span[2]/em').text.split('(')[0]
        self.end_date = self.xpath(r'//*[@id="container"]/p[1]/span[2]/em').text.split('~')[1].split()[0]
        self.start_date = convert_datetime(self.start_date, '%Y.%m.%d', '%Y-%m-%d')
        self.end_date = convert_datetime(self.end_date, '%Y.%m.%d', '%Y-%m-%d')
        # self.dday = self.xpath(r'//*[@id="container"]/p[1]/span[2]/strong').text
        print(self.thumnail)
        print(self.host)
        print(self.sub)
        print(self.start_date)
        print(self.end_date)
        self.target = data_dic.get('응모대상', '')
        self.benefit = data_dic.get('특전', '')
        try:
            regex = re.compile(r'<a href="(?P<url>.*)" target.*홈페이지')
            self.home_url = regex.search(self.html).group("url")
        except:
            self.home_url = ''

        print(self.home_url)
        detail_url = self.xpath(r'//*[@id="Dtl_Gdln"]').get_attribute('src')
        self.go(detail_url)
        self.detail = self.xpath(r'/html/body').text

        poster_file = download_to_temp(self.thumnail)
        print(poster_file)
        self.files = {'poster': poster_file}
        print(self.files)
        post_store(self)
        time.sleep(random.randrange(5, 10))


cms = CampusmonSailer()
cms.start()
cms.close()
