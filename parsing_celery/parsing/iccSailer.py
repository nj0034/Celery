from sailer.sailer import Sailer
from sailer.pacific import store_notice_article
from sailer.utils import convert_datetime
import random
import time
from .notice_common import *


class IccSailer(Sailer):
    def start(self):
        self.category = '정보통신대학'
        for i in range(1, 200):
            self.page_url = "http://icc.skku.ac.kr/icc_new/board_list_square?listPage=" + str(i) + "&boardName=board_notice&field=subject&keyword="
            self.page()

    def page(self):
        self.go(self.page_url)
        self.sub_url = []
        self.numbers = []
        self.hits = []
        sub_urls = self.xpaths(r'//*[@id="sub-container"]/div[3]/table/tbody/tr[*]/td[3]/a')
        numbers = self.xpaths(r'//*[@id="sub-container"]/div[3]/table/tbody/tr[*]/td[1]')
        hits = self.xpaths(r'//*[@id="sub-container"]/div[3]/table/tbody/tr[*]/td[6]')
        for n in numbers:
            self.numbers.append(n.text)
        for h in hits:
            self.hits.append(h.text)
        for url in sub_urls:
            self.sub_url.append(url.get_attribute('href'))
        self.data_parse()

    def data_parse(self):
        for i, self.url in enumerate(self.sub_url):
            self.go(self.url)
            self.sub = self.xpath(r'//*[@id="subject"]').text
            self.writer = self.xpath(r'//*[@id="writer"]').text
            self.content = self.xpath(r'//*[@id="content"]').get_attribute('innerHTML')
            date = self.xpath(r'//*[@id="time"]').text
            self.date = convert_datetime(date, '%Y-%m-%d', '%Y-%m-%d %H:%M:%S')
            self.number = self.numbers[i]
            self.hit = self.hits[i]

            self.img_url = []
            imgs = self.xpaths(r'//*[@id="content"]/p[*]/img')
            for img in imgs:
                self.img_url.append(img.get_attribute('src'))

            self.attach_url = []
            self.attach_name = list()
            attachs = self.xpaths(r'//*[@id="sub-container"]/div[3]/table/tbody/tr[*]/td[2]/a')
            for attach in attachs:
                self.attach_url.append(attach.get_attribute('href'))
                self.attach_name.append(re.compile('(?P<attach_name>.*) \(\d* Bytes\)').search(attach.text).group("attach_name"))


            notice_store(self)
            time.sleep(random.randrange(5, 10))


iccs = IccSailer()
iccs.start()
iccs.close()
