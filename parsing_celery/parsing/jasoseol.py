import re

import os
from datetime import timedelta

from sailer.sailer import Sailer
from sailer.pacific import *
from sailer.utils import *
import random
import time
import json
import requests

from .recruit_common import *



class JasoseolSailer(Sailer):
    def start(self):
        self.page_url = "http://jasoseol.com/recruit"
        self.page()

    def page(self):
        self.go(self.page_url)
        time.sleep(10)
        today = datetime.now().date()
        for i in range(7):
            self.date = today + timedelta(days=i)
            print(self.date)
            try:
                regex = re.compile(r'{0}".*id="(?P<num>\d*)"'.format(str(self.date).replace('-', '')))
                nums = regex.findall(self.html)
                print(nums)
            except:
                nums = None
                print("No recruitment")

            for num in nums:
                self.url = "http://jasoseol.com/recruit/" + num
                self.data_parse()

    def data_parse(self):
        self.go(self.url)
        print(self.url)
        try:
            self.start_date = self.xpath(r'/html/body/div[3]/div[2]/div/div[1]/div[1]/div/div[2]/div[2]/div/span[1]').text
            self.end_date = self.xpath(r'/html/body/div[3]/div[2]/div/div[1]/div[1]/div/div[2]/div[2]/div/span[2]').text
            self.start_date = convert_datetime(self.start_date, '%Y.%m.%d %H:%M', '%Y-%m-%d %H:%M')
            self.end_date = convert_datetime(self.end_date, '%Y.%m.%d %H:%M', '%Y-%m-%d %H:%M')

        except:
            self.start_date = None
            self.end_date = None
        self.home_url = self.xpath(
            r'/html/body/div[3]/div[2]/div/div[1]/div[1]/div/div[2]/div[3]/div[1]/a[2]').get_attribute('href')
        try:
            self.detail_img = self.xpath(r'/html/body/div[3]/div[2]/div/div[1]/div[3]/div/p/img').get_attribute('src')
            self.thumbnail = self.xpath(r'/html/body/div[3]/div[2]/div/div[1]/div[1]/div/div[1]/img').get_attribute('src')
            self.files = download_to_temp(self.detail_img, self.thumbnail)
        except:
            self.files = None

        companies = self.xpaths(r'/html/body/div[3]/div[2]/div/div[1]/div[2]/table/tbody/tr[*]/td[1]')
        fields = self.xpaths(r'/html/body/div[3]/div[2]/div/div[1]/div[2]/table/tbody/tr[*]/td[2]')

        regex = re.compile(r'employment.division.*>(?P<type>.*)<\/td>')
        recruitment_types = regex.findall(self.html)

        # recruitment_types = self.xpaths(r'/html/body/div[3]/div[2]/div/div[1]/div[2]/table/tbody/tr[*]/td[3]')

        for company, field, recruitment_type in zip(companies, fields, recruitment_types):
            self.company = company.text
            self.field = field.text
            self.recruitment_type = recruitment_type
            print(self.company, '/', self.field, '/', self.recruitment_type)

            print(self.start_date, '~', self.end_date)
            print(self.home_url)
            print(self.detail_img)

            recruit_store(self)

        for file in self.files.values():
            os.remove(file)

        time.sleep(random.randrange(5, 10))


jss = JasoseolSailer()
jss.start()
jss.close()
