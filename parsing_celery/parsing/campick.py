import re

import os
from sailer.sailer import Sailer
from sailer.pacific import *
from sailer.utils import *
import random
import time

from .post_common import post_store, download_to_temp

LUNA_PACIFIC_ENDPOINT = "https://luna.devhi.me/pacific/post_store"

class CampickSailer(Sailer):
    def start(self):
        self.page_url = "https://www.campuspick.com/community?id=2571"
        self.go(self.page_url)

        for i in range(10):
            print("down")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        self.contents = self.xpaths(r'//*[@id="container"]/ol/li[*]/a')

        urls = []
        for c in self.contents:
            urls.append(c.get_attribute('href'))
        for self.url in urls:
            self.data_parse()

    def data_parse(self):
        self.go(self.url)
        print(self.url)
        # indexs = self.xpaths(r'//*[@id="container"]/div[*]/h2')
        # datas = self.xpaths(r'//*[@id="container"]/div[*]')
        #
        # for d in datas:
        #     print(d.text)
        #     print("-------------------------------")

        self.thumnail = self.driver.find_element_by_tag_name('img').get_attribute('src')
        self.host = self.xpath(r'//*[@id="container"]/div[4]/dl/dd').text
        self.sub = self.xpath(r'//*[@id="container"]/div[1]/h1').text
        self.start_date = self.xpath(r'//*[@id="container"]/div[3]/p').get_attribute('data-start-date')
        self.end_date = self.xpath(r'//*[@id="container"]/div[3]/p').get_attribute('data-end-date')
        self.dday = self.driver.find_element_by_class_name('dday').text
        print(self.thumnail)
        print(self.host)
        print(self.sub)
        print(self.start_date)
        print(self.end_date)
        self.target = ''
        self.benefit = ''
        details = self.driver.find_elements_by_class_name('section' and 'description')
        self.detail = details[1].text
        print(self.detail)
        try:
            regex = re.compile(r'웹사이트<\/h2>\s*.*href="(?P<url>.*)" class')
            self.home_url = regex.search(self.html).group("url")
        except:
            self.home_url = ''
        print(self.home_url)

        self.files = download_to_temp(self.thumnail)
        post_store(self)
        time.sleep(random.randrange(5, 10))


cps = CampickSailer()
cps.start()
cps.close()
