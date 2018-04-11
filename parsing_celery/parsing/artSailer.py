from raven import Client

from sailer.sailer import Sailer
from sailer.pacific import store_notice_article
from sailer.utils import convert_datetime
import random
import time
from .notice_common import *


class ArtSailer(Sailer):
    def start(self):
        try:
            self.category = '예술대학'
            self.top = False
            for i in range(0, 20):
                self.page_url = "http://art.skku.edu/art/menu_4/sub4_1.jsp?mode=list&board_no=165&pager.offset={}0".format(
                    i)
                self.go(self.page_url)
                print("# {} page start".format(i + 1))
                self.page()

            # self.close()

        except Exception as e:
            client = Client(
                'https://c1e68dfaf122426ab3b6edd880d08759:1237daf5ec7a47269eb5925ff8244446@sentry.io/245310')
            client.captureException()
            return str(e)

    def page(self):
        self.sub_url = []
        self.numbers = []
        sub_urls = self.xpaths(r'//*[@id="jwxe_main_content"]/div/div[2]/table/tbody/tr[*]/td[2]/a')
        numbers = self.xpaths(r'//*[@id="jwxe_main_content"]/div/div[2]/table/tbody/tr[*]/td[1]')
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
            self.sub = self.xpath(r'//*[@id="jwxe_main_content"]/div/div[1]/table/tbody/tr[1]/td').text
            self.writer = self.xpath(r'//*[@id="jwxe_main_content"]/div/div[1]/table/tbody/tr[2]/td[1]').text
            self.content = self.xpath(r'//*[@id="article_text"]').text
            self.hit = self.xpath(r'//*[@id="jwxe_main_content"]/div/div[1]/table/tbody/tr[2]/td[3]').text
            date = self.xpath(r'//*[@id="jwxe_main_content"]/div/div[1]/table/tbody/tr[2]/td[2]').text
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
            attachs = self.xpaths(r'//*[@id="jwxe_main_content"]/div/div[1]/table/tbody/tr[3]/td/ul/li[*]/a')
            for attach in attachs:
                self.attach_url.append(attach.get_attribute('href'))

            notice_store(self)
            time.sleep(random.randrange(5, 10))


arts = ArtSailer()
arts.start()
# arts.close()
