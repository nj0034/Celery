from sailer.sailer import Sailer
from sailer.pacific import store_notice_article
from sailer.utils import convert_datetime
import random
import time
from .notice_common import *


class SportSailer(Sailer):
    def start(self):
        self.category = '스포츠과학대학'
        for i in range(0, 18):
            self.page_url = "http://sport.skku.edu/sports/menu_4/sub4_1.jsp?mode=list&board_no=824&pager.offset={}0".format(i)
            self.go(self.page_url)
            print("# {} page start".format(i + 1))
            self.page()

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

    def data_parse(self):
        for self.number, self.url in zip(self.numbers, self.sub_url):
            self.go(self.url)
            self.sub = self.xpath(r'//*[@id="jwxe_main_content"]/div/div[1]/table/tbody/tr[1]/td').text
            self.writer = self.xpath(r'//*[@id="jwxe_main_content"]/div/div[1]/table/tbody/tr[2]/td[1]').text
            self.content = self.xpath(r'//*[@id="article_text"]').get_attribute('innerHTML')
            self.hit = self.xpath(r'//*[@id="jwxe_main_content"]/div/div[1]/table/tbody/tr[2]/td[3]').text
            date = self.xpath(r'//*[@id="jwxe_main_content"]/div/div[1]/table/tbody/tr[2]/td[2]').text
            self.date = convert_datetime(date, '%Y-%m-%d', '%Y-%m-%d %H:%M:%S')

            self.img_url = []
            imgs = self.xpaths(r'//*[@id="article_text"]/p[*]/img')
            for img in imgs:
                self.img_url.append(img.get_attribute('src'))

            self.attach_url = []
            self.attach_name = list()
            attachs = self.xpaths(
                r'//*[@id="jwxe_main_content"]/div/div[1]/table/tbody/tr[3]/td/ul/li[*]/a')
            for attach in attachs:
                self.attach_url.append(attach.get_attribute('href'))
                self.attach_name.append(attach.get_attribute('title').split('다운로드')[0].strip())

            notice_store(self)
            time.sleep(random.randrange(5, 10))


sports = SportSailer()
sports.start()
sports.close()
