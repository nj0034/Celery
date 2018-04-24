from sailer.sailer import Sailer
from sailer.pacific import *
from sailer.utils import *
import random
import time
from .notice_common import *


class SoftSailer(Sailer):
    def start(self):
        self.category = '소프트웨어대학'
        self.page_url = "http://cs.skku.edu/open/notice/list"
        self.go(self.page_url)
        self.top_topic()

    def top_topic(self):
        self.xpath('//*[@id="boardList"]/tbody/tr[1]/td[3]')
        top_number = self.xpath(r'//*[@id="boardList"]/tbody/tr[1]/td[1]').text
        self.go("http://cs.skku.edu/open/notice/view/" + top_number)
        self.parse_topics()

    def parse_topics(self):
        for i in range(1000):
            # print("# {} pages".format(i + 1))
            self.data_parse()
            self.xpath('//*[@id="next"]').click()

    def data_parse(self):
        self.xpath(r'//*[@id="title"]')
        self.sub = self.xpath(r'//*[@id="title"]').text
        self.writer = self.xpath(r'//*[@id="name"]').text
        self.content = self.xpath(r'//*[@id="text"]').get_attribute('innerHTML')
        self.hit = self.xpath(r'//*[@id="views"]').text
        date = self.xpath(r'//*[@id="time"]').text
        self.date = convert_datetime(date, '%Y-%m-%d', '%Y-%m-%d %H:%M:%S')
        self.url = self.current_url
        self.number = self.url.split('/')[6]
        # print(self.number)

        self.img_url = []
        imgs = self.xpaths(r'//*[@id="text"]/p[*]/img')
        for img in imgs:
            self.img_url.append(img.get_attribute('src'))

        self.attach_url = []
        attachs = self.xpaths(r'//*[@id="files"]/div[*]/div/a')
        for attach in attachs:
            self.attach_url.append(attach.get_attribute('href'))
            print(attach.text)

        # notice_store(self)

        time.sleep(random.randrange(5, 10))


softs = SoftSailer()
softs.start()
softs.close()
