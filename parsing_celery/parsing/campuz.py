import os
from sailer.sailer import Sailer
from sailer.pacific import *
from sailer.utils import *
import random
import time

from .post_common import post_store, download_to_temp

LUNA_PACIFIC_ENDPOINT = "https://luna.devhi.me/pacific/post_store"

class CampuzSailer(Sailer):
    def start(self):
        self.category = {'supporters': 216, 'overseas': 218, 'volunteer': 222, 'programs': 257, 'contest': 229}
        self.content_td_num = 2
        for self.key in self.category:
            print(self.key)
            if self.key == 'contest':
                self.content_td_num = 3
            for i in range(70):
                self.page_url = "http://www.campuz.net/index.php?mid={0}&page={1}".format(self.key, i + 1)
                self.page()

    def page(self):
        self.go(self.page_url)
        self.contents = self.xpaths(r'//*[@id="bd_{0}_0"]/div[2]/table/tbody/tr[*]/td[{1}]/a'.format(self.category[self.key], self.content_td_num))
        urls = []
        for c in self.contents:
            urls.append(c.get_attribute('href'))
        for self.url in urls:
            self.data_parse()

    def data_parse(self):
        self.go(self.url)
        print(self.url)
        id = self.url.split('=')[-1]
        try:
            self.thumnail = self.xpath(r'//*[@id="bd_{0}_{1}"]/div[2]/div[2]/article/div/p[*]/img'.format(self.category[self.key], id)).get_attribute('src')
        except:
            self.thumnail = None

        data_dic = {}
        indexs = self.xpaths(r'//*[@id="bd_{0}_{1}"]/div[2]/div[1]/table/tbody/tr[*]/th'.format(self.category[self.key], id))
        datas = self.xpaths(r'//*[@id="bd_{0}_{1}"]/div[2]/div[1]/table/tbody/tr[*]/td'.format(self.category[self.key], id))

        for i, d in zip(indexs, datas):
            data_dic[i.text] = d.text

        self.host = data_dic.get('주최', '')
        if self.key == 'contest':
            self.sub = data_dic.get('공모전제목', '')
        else:
            self.sub = data_dic.get('모집제목', '')
        self.start_date = data_dic.get('모집시작', '')
        self.end_date = data_dic.get('모집마감', '')
        # 마감일 23일 전인 글 삭제
        try:
            if datetime.strptime(self.end_date, '%Y-%m-%d') < datetime(year=2018, month=2, day=23):
                return
        except:
            pass

        print(self.thumnail)
        print(self.host)
        print(self.sub)
        # if datetime.strptime(self.end_date, '%Y-%m-%d') < datetime.now():
        #     print("<----------------------end---------------------->")
        #     quit()
        # self.dday = str(datetime.strptime(self.end_date, '%Y-%m-%d') - datetime.now()).split()[0]
        # self.dday = 'D-' + str(int(self.dday) + 1)
        # print(self.dday)
        self.target = ''
        self.benefit = ''
        # self.detail = self.xpath(r'//*[@id="bd_{0}_{1}"]/div[2]/div[2]/article/div'.format(self.category[self.key], id)).text
        # print(self.detail)
        self.detail = self.driver.find_element_by_class_name('*' and 'xe_content').text
        print(self.detail)
        self.home_url = data_dic.get('홈페이지', '')
        self.apply_url = data_dic.get('이메일접수', '')
        print(self.home_url)
        print(self.apply_url)

        self.files = download_to_temp(self.thumnail)
        post_store(self)
        time.sleep(random.randrange(5, 10))



cams = CampuzSailer()
cams.start()
cams.close()
