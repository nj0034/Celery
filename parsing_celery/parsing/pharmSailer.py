import re
from sailer.sailer import Sailer
from sailer.pacific import store_notice_article
from sailer.utils import convert_datetime
import random
import time
from .notice_common import *


PAGE_URL = "http://pharm.skku.edu/board/board.jsp?catg=notice&curPage={page}"
DATA_URL = "http://pharm.skku.edu/board/view.jsp?curNum={curNum}"

class PharmSailer(Sailer):
    def start(self):
        self.category = '약학대학'
        for i in range(1, 200):
            print("#{} page".format(i))
            self.page_url = PAGE_URL.format(page=i)
            self.page()

    def page(self):
        self.go(self.page_url)
        numbers = self.xpaths(r'//*[@id="content"]/div/div[2]/div/div/div[2]/table/tbody/tr[*]/td[1]')
        sub_urls = self.xpaths(r'//*[@id="content"]/div/div[2]/div/div/div[2]/table/tbody/tr[*]/td[2]/a')

        number_list = [number.text for number in numbers]
        curNum_list = [sub_url.get_attribute('href').split('(')[1].split(')')[0] for sub_url in sub_urls]

        for self.number, curNum in zip(number_list, curNum_list):
            self.url = DATA_URL.format(curNum=curNum)
            self.data_parse()

    def data_parse(self):
        self.go(self.url)
        self.sub = self.xpath(r'//*[@id="content"]/div/div[2]/div/div/div[1]/table/tbody/tr[1]/th').text

        regex = re.compile(r'작성자.*｜<\/span>(?P<writer>.*)<.*날짜.*｜<\/span>(?P<date>.*)<.*조회수.*｜<\/span>(?P<hit>.*)<')
        self.writer = regex.search(self.html).group("writer")
        date = regex.search(self.html).group("date")
        self.hit = regex.search(self.html).group("hit")

        self.content = self.xpath(r'//*[@id="contents"]').get_attribute('innerHTML')
        self.date = convert_datetime(date, '%Y-%m-%d', '%Y-%m-%d %H:%M:%S')

        print(self.sub)
        # print(self.writer)
        # print(self.hit)
        # print(self.date)
        # print(self.number)
        # print(self.content)
        imgs = self.xpaths(r'//*[@id="contents"]/p[*]/img')
        self.img_url = [img.get_attribute('src') for img in imgs]

        attachs = self.xpaths(r'//*[@id="content"]/div/div[2]/div/div/div[1]/table/tbody/tr[3]/td/a[*]')
        self.attach_url = [attach.get_attribute('href') for attach in attachs]
        self.attach_name = [attach.text.strip() for attach in attachs]

        print(self.attach_url)
        print(self.attach_name)

        notice_store(self)
        time.sleep(random.randrange(5, 10))


pharms = PharmSailer()
pharms.start()
pharms.close()
