from sailer.sailer import Sailer
from sailer.pacific import store_notice_article
from sailer.utils import convert_datetime
import random
import time
from .notice_common import *


class Not_cheyongSailer(Sailer):
    def start(self):
        self.category = '채용&모집'
        for i in range(1, 300):
            self.page_url = "http://www.skku.edu/new_home/campus/skk_comm/notice_list.jsp?page={}&bCode=7&skey=BOARD_SUBJECT&keyword=".format(i)
            self.page()

    def page(self):
        self.go(self.page_url)
        self.sub_url = []
        sub_urls = self.xpaths(r'//*[@id="contents"]/table/tbody/tr[*]/td[2]/a')
        for url in sub_urls:
            self.sub_url.append(url.get_attribute('href'))
        self.data_parse()

    def data_parse(self):
        for self.url in self.sub_url:
            self.go(self.url)
            self.sub = self.xpath(r'//*[@id="contents"]/table[1]/tbody/tr[1]/td').text
            self.writer = self.xpath(r'//*[@id="contents"]/table[1]/tbody/tr[2]/td[1]').text
            self.number = self.xpath(r'//*[@id="contents"]/table[1]/tbody/tr[2]/td[2]').text
            self.hit = self.xpath(r'//*[@id="contents"]/table[1]/tbody/tr[3]/td[2]').text
            self.content = self.xpath(r'//*[@id="contents"]/div[1]').get_attribute('innerHTML')
            date = self.xpath(r'//*[@id="contents"]/table[1]/tbody/tr[3]/td[1]').text
            self.date = convert_datetime(date, '%Y.%m.%d %H:%M:%S', '%Y-%m-%d %H:%M:%S')

            self.img_url = []
            imgs = self.xpaths(r'//*[@id="contents"]/div[*]/img')
            for img in imgs:
                self.img_url.append(img.get_attribute('src'))

            file_hrefs = list()
            self.attach_name = list()
            files = self.xpaths(r'//*[@id="contents"]/div[2]/ul/li[*]/a')
            for file in files:
                file_hrefs.append(file.get_attribute('href'))
                self.attach_name.append(re.compile('(?P<attach_name>.*) \(\d*KB\)').search(file.text).group("attach_name"))

            self.attach_url = notice_attach_url(file_hrefs)
            print(self.attach_name)

            notice_store(self)
            time.sleep(random.randrange(5, 10))


ncs = Not_cheyongSailer()
ncs.start()
ncs.close()
