from sailer.sailer import Sailer
from sailer.pacific import *
from sailer.utils import *
import random
import time
import re
from .notice_common import *


class LiberalartsSailer(Sailer):
    def start(self):
        self.category = '문과대학'
        for i in range(0, 50):
            self.page_url = "http://liberalarts.skku.edu/liberal/menu_6/data_01.jsp?mode=list&board_no=229&pager.offset={}0".format(i)
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
            self.go('http://liberalarts.skku.edu/liberal/menu_6/data_01.jsp?mode=view&article_no=321684&board_wrapper=%2Fliberal%2Fmenu_6%2Fdata_01.jsp&pager.offset=0&board_no=229')
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


liberalartss = LiberalartsSailer()
liberalartss.start()
liberalartss.close()
