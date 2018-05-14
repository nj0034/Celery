from sailer.sailer import Sailer
from sailer.pacific import *
from sailer.utils import *
import random
import time
from .notice_common import *


class DormSuwon(Sailer):
    def start(self):
        self.category = '봉룡학사'
        self.top = False
        for i in range(0, 51):
            self.page_url = "https://dorm.skku.edu/skku/notice/notice_all.jsp?mode=list&board_no=16&pager.offset={}0".format(3*i)
            self.go(self.page_url)
            print("# {} page start".format(i + 1))
            self.page()

    def page(self):
        sub_xpaths = self.xpaths(r'//*[@id="item_body"]/div[3]/div/div[2]/div[1]/div[2]/div[2]/div/div[2]/table/tbody/tr[*]/td[3]/a')
        numbers = self.xpaths(r'//*[@id="item_body"]/div[3]/div/div[2]/div[1]/div[2]/div[2]/div/div[2]/table/tbody/tr[*]/td[1]')
        types = self.xpaths(r'//*[@id="item_body"]/div[3]/div/div[2]/div[1]/div[2]/div[2]/div/div[2]/table/tbody/tr[*]/td[2]')
        self.sub_urls = [xpath.get_attribute('href') for xpath in sub_xpaths]
        self.numbers = [number.text for number in numbers]
        self.types = [type.text for type in types]

        self.data_parse()
        self.top = True

    def data_parse(self):
        for self.number, self.url, self.type in zip(self.numbers, self.sub_urls, self.types):
            if not self.number:
                if self.type == 'Notice in English':
                    continue

                if not self.top:
                    self.number = 'top'
                else:
                    continue

            self.go(self.url)
            self.sub = self.xpath(
                r'//*[@id="item_body"]/div[3]/div/div[2]/div[1]/div[2]/div[2]/div/div[1]/table/tbody/tr[1]/td').text
            self.writer = ''
            self.content = self.xpath(r'//*[@id="article_text"]').get_attribute('innerHTML')
            self.hit = self.xpath(
                r'//*[@id="item_body"]/div[3]/div/div[2]/div[1]/div[2]/div[2]/div/div[1]/table/tbody/tr[2]/td').text.split(":")[-1].strip()
            date = self.xpath(
                r'//*[@id="item_body"]/div[3]/div/div[2]/div[1]/div[2]/div[2]/div/div[1]/table/tbody/tr[2]/td/span[4]').text
            self.date = convert_datetime(date, '%Y-%m-%d', '%Y-%m-%d %H:%M:%S')
            print(self.sub)
            print(self.writer)
            print(self.hit)
            print(self.date)
            print(self.number)
            print(self.content)

            img_urls = self.xpaths(r'//*[@id="article_text"]/p[*]/img')
            self.img_url = [url.get_attribute('src') for url in img_urls]

            print(self.img_url)

            self.attach_url = []
            self.attach_name = list()
            attachs = self.xpaths(r'//*[@id="item_body"]/div[3]/div/div[2]/div[1]/div[2]/div[2]/div/div[1]/table/tbody/tr[3]/td/div[*]/a')
            for attach in attachs:
                self.attach_url.append(attach.get_attribute('href'))
                self.attach_name.append(attach.get_attribute('title').split('다운로드')[0].strip())

            notice_store(self)

            time.sleep(random.randrange(5, 10))


ds = DormSuwon()
ds.start()
ds.close()
