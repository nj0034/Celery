from sailer.sailer import Sailer
from sailer.pacific import *
from sailer.utils import *
import random
import time
from .notice_common import *


class HakbuSailer(Sailer):
    def start(self):
        self.category = '학부대학'
        self.top = False
        for i in range(0, 51):
            self.page_url = "http://hakbu.skku.edu/hakbu/menu_7/sub_07_01.jsp?mode=list&board_no=107&pager.offset={}0".format(
                i)
            self.go(self.page_url)
            print("# {} page start".format(i + 1))
            self.page()

    def page(self):
        self.sub_url = []
        self.numbers = []
        sub_urls = self.xpaths(
            r'//*[@id="item_body"]/div[1]/div[2]/div/div[2]/div[2]/div[2]/div/div[2]/table/tbody/tr[*]/td[2]/a')
        numbers = self.xpaths(
            r'//*[@id="item_body"]/div[1]/div[2]/div/div[2]/div[2]/div[2]/div/div[2]/table/tbody/tr[*]/td[1]')
        for n in numbers:
            self.numbers.append(n.text)
        for url in sub_urls:
            self.sub_url.append(url.get_attribute('href'))
        self.data_parse()
        self.top = True

    def data_parse(self):
        for self.number, self.url in zip(self.numbers, self.sub_url):
            if not self.number:
                if not self.top:
                    self.number = 'top'
                else:
                    continue

            self.go(self.url)
            self.sub = self.xpath(
                r'//*[@id="item_body"]/div[1]/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/table/tbody/tr[1]/td').text
            self.writer = self.xpath(
                r'//*[@id="item_body"]/div[1]/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/table/tbody/tr[2]/td[1]').text
            self.content = self.xpath(r'//*[@id="article_text"]').get_attribute('innerHTML')
            self.hit = self.xpath(
                r'//*[@id="item_body"]/div[1]/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/table/tbody/tr[2]/td[3]').text
            date = self.xpath(
                r'//*[@id="item_body"]/div[1]/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/table/tbody/tr[2]/td[2]').text
            self.date = convert_datetime(date, '%Y-%m-%d', '%Y-%m-%d %H:%M:%S')
            # print(self.sub)
            # print(self.writer)
            # print(self.hit)
            # print(self.date)
            # print(self.number)
            # print(self.content)

            self.img_url = []
            imgs = self.xpaths(r'//*[@id="article_text"]/p[*]/img')
            for img in imgs:
                self.img_url.append(img.get_attribute('src'))

            self.attach_url = []
            self.attach_name = list()
            attachs = self.xpaths(r'//*[@id="item_body"]/div[1]/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/table/tbody/tr[3]/td/ul/li[*]/a')
            for attach in attachs:
                self.attach_url.append(attach.get_attribute('href'))
                self.attach_name.append(attach.get_attribute('title').split('다운로드')[0].strip())

            notice_store(self)

            time.sleep(random.randrange(5, 10))


hakbus = HakbuSailer()
hakbus.start()
hakbus.close()
