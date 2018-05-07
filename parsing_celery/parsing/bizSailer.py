from sailer.sailer import Sailer
from sailer.pacific import *
from sailer.utils import *
import random
import time
from .notice_common import *


class BizSailer(Sailer):
    def start(self):
        self.category = '경영대학'
        for i in range(1, 100):
            self.page_url = "https://biz.skku.edu/kr/boardList.do?bbsId=BBSMSTR_000000000001&pageIndex={}".format(i)
            self.page()
        self.go(self.page_url)

    def page(self):
        self.go(self.page_url)
        url_form = 'https://biz.skku.edu/kr/board.do?bbsId=BBSMSTR_000000000001&nttId={}'
        self.sub_url = list()
        sub_url_hrefs = self.xpaths(r'//*[@id="container"]/div[3]/div[1]/ul/li[*]/strong/a')
        for sub_url_href in sub_url_hrefs:
            nttId = sub_url_href.get_attribute('href').split('\'')[1]
            self.sub_url.append(url_form.format(nttId))

        for self.url in self.sub_url:
            self.data_parse()

    def data_parse(self):
        self.go(self.url)
        self.sub = self.xpath(r'//*[@id="container"]/div[3]/div[1]/div[1]/h2').text
        data = self.xpath(r'//*[@id="container"]/div[3]/div[1]/div[2]').text

        self.writer = data.split('분류')[1].split('번호')[0]
        self.number = data.split('분류')[1].split('번호')[1].split('작성일')[0]
        self.hit = data.split('분류')[1].split('번호')[1].split('작성일')[1].split('조회')[1]
        date = data.split('분류')[1].split('번호')[1].split('작성일')[1].split('조회')[0]
        self.date = convert_datetime(date, '%Y-%m-%d', '%Y-%m-%d %H:%M:%S')
        self.content = self.css(r'#container > div.content > div.board_view > div.view_content').get_attribute('innerHTML')
        print(self.sub)
        # print(self.writer)
        # print(self.hit)
        # print(self.date)
        # print(self.number)
        # print(self.content)

        self.img_url = []
        imgs = self.xpaths(r'//*[@id="container"]/div[3]/div[1]/div[*]/p[*]/img')
        for img in imgs:
            self.img_url.append(img.get_attribute('src'))

        self.attach_url = []
        self.attach_name = list()
        attach_url_form = 'https://biz.skku.edu/cmm/fms/FileDown.do?atchFileId={0}&fileSn={1}'
        # atchFileIds = self.xpaths(r'//*[@id="container"]/div[3]/div[1]/div[3]/a[*]')
        # print(atchFileIds)
        attach_html = self.xpath(r'//*[@id="container"]/div[3]/div[1]/div[3]').get_attribute('innerHTML')
        try:
            atchFileIds = re.findall('href=\".*\(\'(?P<atchFileId>.*)\',', attach_html)
        except:
            atchFileIds = None

        for fileSn, atchFileId in enumerate(atchFileIds):
            self.attach_name.append(atchFileId)
            print(self.attach_name)
            # atchFileId = atchFileId.split('\'')[1]
            self.attach_url.append(attach_url_form.format(atchFileId, fileSn))
            print(self.attach_url)

        notice_store(self)

        time.sleep(random.randrange(5, 10))


bizs = BizSailer()
bizs.start()
bizs.close()
