import re

import os
from sailer.sailer import Sailer
from sailer.pacific import *
from sailer.utils import *
import random
import time

from .post_common import post_store, download_to_temp

LUNA_PACIFIC_ENDPOINT = "https://luna.devhi.me/pacific/post_store"

class LinkareerSailer(Sailer):
    def start(self):
        activity_contest_array = ['activity', 'contest']
        for activity_contest in activity_contest_array:
            self.page_url = "http://linkareer.com/list/{}".format(activity_contest)
            self.go(self.page_url)

        # for i in range(4):
        #     self.driver.find_element_by_tag_name('body').send_keys(Keys.END)
        #     print('down')
        #     time.sleep(11)
        #     print(self.xpaths(r'/html/body/div[5]/div[3]/a[16]'))
        for i in range(20):
            print("down")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        self.contents = self.xpaths(r'/html/body/div[5]/div[3]/a[*]')

        url = []
        for c in self.contents:
            url.append(c.get_attribute('href'))

        print(len(url))

        for self.url in url:
            self.data_parse()

    def data_parse(self):
        self.go(self.url)
        print(self.url)
        data_dic = {}

        self.css(r'#activity-container > div.activity-content > div.activity-bottom > div > div.activity-detail > div.activity-detail-more').click()
        self.thumnail = self.css(
            r'#activity-container > div.activity-content > div.activity-info > div.activity-thumb > a > span > img').get_attribute(
            'src')
        self.host = self.css(
            r'#activity-container > div.activity-content > div.activity-info > div.activity-sum > p').text
        self.sub = self.css(
            r'#activity-container > div.activity-content > div.activity-header > div.activity-title > p').text
        # self.dday = self.css(
        #     r'#activity-container > div.activity-content > div.activity-header > div.activity-title > div').text
        print(self.thumnail)
        print(self.host)
        print(self.sub)
        # print(self.dday)
        # self.start =
        # self.end =
        self.target = self.css(
            r'#activity-container > div.activity-content > div.activity-info > div.activity-sum > div.activity-sum-info > div.activity-sum-right > dl:nth-child(1) > dd').text
        self.benefit = self.css(
            r'#activity-container > div.activity-content > div.activity-info > div.activity-sum > div.activity-sum-info > div.activity-sum-right > dl.benefit-data > dd').text
        self.detail = self.css(
            r'#activity-container > div.activity-content > div.activity-bottom > div > div.activity-detail').text.split('간단히')[0]
        try:
            regex = re.compile(r'homepage-url" href="(?P<url>.*)"\s')
            self.home_url = regex.search(self.html).group("url")
        except:
            self.home_url = ''

        self.start_date = None
        self.end_date = None

        print(self.target)
        print(self.benefit)
        print(self.home_url)

        poster_file = download_to_temp(self.thumnail)
        self.files = {'poster': poster_file}
        post_store(self)
        time.sleep(random.randrange(5, 10))


links = LinkareerSailer()
links.start()
links.close()
