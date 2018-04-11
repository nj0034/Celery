from sailer.sailer import Sailer
from sailer.pacific import store_notice_article
from sailer.utils import convert_datetime
import random
import time
import datetime
from .notice_common import *


class MedSailer(Sailer):
    def start(self):
        self.category = '의과대학'
        for i in range(1, 5):
            self.page_url = "http://www.skkumed.ac.kr/notice.asp?keyword=&startpage=1&bcode=nt&pg={}".format(i)
            self.go(self.page_url)
            print("# {} page start".format(i))
            self.page()

    def page(self):
        self.sub_url = []
        self.numbers = []
        sub_urls = self.xpaths(r'/html/body/div/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[4]/td/table/tbody/tr[*]/td[3]/div/a[1]')

        for url in sub_urls:
            self.sub_url.append(url.get_attribute('href'))
        self.data_parse()

    def data_parse(self):
        for self.url in self.sub_url:
            self.go(self.url)
            self.sub = self.xpath(
                r'/html/body/div/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td[3]').text
            self.writer = self.xpath(
                r'/html/body/div/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td[3]').text
            self.content = self.xpath(
                r'/html/body/div/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[8]/td').text
            self.hit = self.xpath(
                r'/html/body/div/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[4]/td[11]/div').text
            date = self.xpath(
                r'/html/body/div/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[4]/td[7]/div').text
            if(date.split()[1] == '오전'):
                self.date = convert_datetime(date.split()[0] + 'AM' + date.split()[2], '%Y-%m-%d%p%I:%M:%S', '%Y-%m-%d %H:%M:%S')
            else:
                self.date = convert_datetime(date.split()[0] + 'PM' + date.split()[2], '%Y-%m-%d%p%I:%M:%S', '%Y-%m-%d %H:%M:%S')

            self.img_url = []
            imgs = self.xpaths(r'/html/body/div/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[8]/td/img')
            for img in imgs:
                self.img_url.append(img.get_attribute('src'))

            self.attach_url = []
            attachs = self.xpaths(r'/html/body/div/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[6]/td[3]/a')
            for attach in attachs:
                self.attach_url.append(attach.get_attribute('href'))

            notice_store(self)
            time.sleep(random.randrange(5, 10))


meds = MedSailer()
meds.start()
meds.close()
