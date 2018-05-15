import os

import re
from sailer.sailer import Sailer
from sailer.pacific import *
from sailer.utils import *
import random
import time

from .post_common import post_store, download_to_temp

LUNA_PACIFIC_ENDPOINT = "https://luna.devhi.me/pacific/post_store"
LOCAL_PACIFIC_ENDPOINT = "http://127.0.0.1:8000/pacific/post_store"


class AllconSailer(Sailer):
    def start(self):
        activity_contest_array = ['activity', 'contest']
        for self.activity_contest in activity_contest_array:
            self.top_check = False  # 고정 글
            for i in range(70):
                self.page_url = "http://www.all-con.co.kr/page/uni_{0}.php?page={1}&sc=0&st=0&sstt=e&sst=cl_end_date%20%3C%20now()%20ASC,%20cl_update%20&stx=".format(
                    self.activity_contest, i + 1)
                self.page()

    def page(self):
        self.go(self.page_url)
        self.contents = self.xpaths(r'//*[@id="page_board_contents"]/div/table/tbody/tr[*]/td[2]/a')
        self.states = self.xpaths(r'//*[@id="page_board_contents"]/div/table/tbody/tr[*]/td[4]/div/img')
        urls = []
        states = []
        for c, s in zip(self.contents, self.states):
            if c.get_attribute('class') == 'active':
                if self.top_check:
                    continue
                else:
                    self.top_check = True
            urls.append(c.get_attribute('href'))
            states.append(s.get_attribute('alt'))
        for self.url, self.state in zip(urls, states):
            if self.state == '마감':
                break
            self.data_parse()

    def data_parse(self):
        self.go(self.url)
        print(self.url)
        # data_dic = {}
        # indexs = self.xpaths(r'//*[@id="page_board_contents"]/div[1]/div[2]/div[2]/table/tbody/tr[*]/td[1]')
        # datas = self.xpaths(r'//*[@id="page_board_contents"]/div[1]/div[2]/div[2]/table/tbody/tr[*]/td[2]')
        #
        # for i, d in zip(indexs, datas):
        #     print(i.text, d.text)
        #     data_dic[i.text] = d.text
        #
        # print(data_dic)
        try:
            regex = re.compile(r'src="(?P<poster>.*)" alt="포스터"')
            self.thumnail = 'http://www.all-con.co.kr' + regex.search(self.html).group("poster").strip()
        except:
            self.thumnail = None


        regex = re.compile(r'주관<\/td>\s*<td>(?P<host>.*)<')
        self.host = regex.search(self.html).group("host")
        self.sub = self.driver.find_element_by_class_name('board_cont_title').text
        regex = re.compile(r'접수기간<\/td>\s*<td><span class="none">(?P<date>.*)<\/span')
        date = regex.search(self.html).group("date")
        self.start_date = '20' + date.split('~')[0].strip()
        self.end_date = '20' + date.split('~')[1].strip()
        self.start_date = convert_datetime(self.start_date, '%Y.%m.%d', '%Y-%m-%d')
        self.end_date = convert_datetime(self.end_date, '%Y.%m.%d', '%Y-%m-%d')

        print(self.thumnail)
        print(self.host)
        print(self.sub)
        print(self.start_date)
        print(self.end_date)

        regex = re.compile(r'응모대상<\/td>\s*<td>(?P<target>.*)<')
        self.target = regex.search(self.html).group("target")
        print(self.target)

        if self.activity_contest == 'activity':
            regex = re.compile(r'혜택<\/td>\s*<td>(?P<benefit>.*)<')
        else:
            regex = re.compile(r'시상내역<\/td>\s*<td>(?P<benefit>.*)<')
        self.benefit = regex.search(self.html).group("benefit")
        print(self.benefit)

        self.detail = self.driver.find_element_by_class_name('board_body_txt').text
        try:
            regex = re.compile(r'class="homepage"><a href="(?P<home_url>.*)"\s')
            self.home_url = regex.search(self.html).group("home_url")
        except:
            self.home_url = None
        print(self.home_url)

        self.files = download_to_temp(self.thumnail)

        post_store(self)
        time.sleep(random.randrange(5, 10))


alls = AllconSailer()
alls.start()
alls.close()
