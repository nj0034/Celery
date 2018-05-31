from sailer.sailer import Sailer
from sailer.pacific import *
from sailer.utils import *
import random
import time
from .notice_common import *

XPATH_JSON = {
    "meta": {
        "site_name":"성균관대학교 홈페이지",
        "site_url":"http://skku.edu",
        "category": "category",
        "version":"1"
    },

    "parser": {
        "method": "url_based / next_button / ",
        "version": "1",
        "period": "15m",
        "stop": "size",
        "interval": "5-10"
    },

    "rule":{
        "page_url": "asdfasdf{page}asdfasdf",
        "start_page": 1,
        "properties": {
            "title": {
                "xpath": "",
                "url_xpath": "",
                "position": "in"
            },
            "number": {
                "xpath": "",
                "position": "out"
            },
            "date": {
                "xpath": "",
                "format": "",
                "position": "in"
            },
            "writer": {
                "type": "xpath",
                "xpath": "",
                "position": "in"
            },
            "hit": {
                "xpath": "",
                "position": "in"
            },
            "content": {
                "xpath": "",
                "position": "in"
            },
            "img": {
                "xpath": "",
                "position": "in"
            },
            "attach": {
                "xpath": "",
                "position": "in",
                "name_regex": "",
                "HTML_xpath": ""
            }
        }
    }
}


class TestModule(Sailer):
    def start(self):
        self.meta = XPATH_JSON['meta']
        self.parser = XPATH_JSON['parser']
        self.rule = XPATH_JSON['rule']
        self.props = self.rule['properties']

        self.top = False

        parsing_method = self.parser['parsing_method']
        page_url = self.rule['page_url']

        if parsing_method == 'url_based':
            start_page = int(self.rule['start_page'])

            for i in range(start_page, 100):
                self.go(page_url.format(page=i))
                print("# {} page start".format(i + 1))
                self.url_based()

        elif parsing_method == 'next_button':
            self.go(page_url)
            self.next_button()

        else:
            pass

    def next_button(self):
        in_prop_list = self.props.keys()
        top_article_url = self.xpath(XPATH_JSON['top_article_xpath']).get_attribute('href')
        self.go(top_article_url)

        while (True):
            parsing_result_json_list = [{"url": self.current_url}]
            parsing_result_json_list = self.parsing_in_props(in_prop_list, parsing_result_json_list)

            # es에 parsing_result_json_list 저장(top 글이면 저장 안함)

            next_button_url = self.xpath(XPATH_JSON['next_button_xpath']).get_attribute('href')
            if next_button_url:
                self.go(next_button_url)
            else:
                break

    def url_based(self):
        out_prop_list = list()
        in_prop_list = list()
        for key, value in self.props.items():
            if value['position'] == 'out':
                out_prop_list.append(key)
            else:
                in_prop_list.append(key)

        title_url_xpaths = self.xpaths(self.props['title']['url_xpath'])
        parsing_result_json_list = [{"url": title_url_xpath.get_attribute('href')} for title_url_xpath in
                                    title_url_xpaths]

        for out_prop in out_prop_list:
            xpath_list = self.xpaths(self.props[out_prop]['xpath'])
            for xpath, parsing_result_json in zip(xpath_list, parsing_result_json_list):
                out_prop_json = self.parsing_prop(out_prop)
                parsing_result_json.update(out_prop_json)

        parsing_result_json_list = self.parsing_in_props(in_prop_list, parsing_result_json_list)

        # es에 저장(top 글이면 저장 안함)

        time_interval = [int(n) for n in self.parser['interval'].split('-')]
        random_time = random.randint(*time_interval)

        time.sleep(random_time)

        self.top = True

    def parsing_in_props(self, in_prop_list, parsing_result_json_list):
        for parsing_result_json in parsing_result_json_list:
            self.go(parsing_result_json['url'])
            for in_prop in in_prop_list:

                in_prop_json = self.parsing_prop(in_prop)

                parsing_result_json.update(in_prop_json)

        return parsing_result_json_list

    def parsing_prop(self, prop):
        xpath = self.props[prop]['xpath']

        if prop == 'content':
            prop_json = {
                "content_text": self.xpath(xpath).text,
                "content_HTML": self.xpath(xpath).get_attribute('innerHTML'),
            }
        elif prop == 'date':
            date = self.xpath(xpath).text
            format = self.props[prop]['format']
            date = convert_datetime(date, format, '%Y-%m-%d %H:%M:%S')
            prop_json = {
                "date": date
            }
        elif prop == 'img':
            img_url_list = [xpath.get_attribute('src') for xpath in self.xpaths(xpath) if xpath]

            # s3에 저장하는 함수 넣기 + s3 url list 만들기
            img_s3_url_list = list()

            prop_json = {
                "img": img_s3_url_list
            }
        elif prop == 'attach':
            attach_url_list = [xpath.get_attribute('href') for xpath in self.xpaths(xpath) if xpath]
            attach_name_list = re.findall(self.props[prop]['name_regex'],
                                          self.xpath(self.props[prop]['HTML_xpath']).get_attribute('innerHTML'))

            # s3에 저장하는 함수 넣기 + s3 url list 만들기
            attach_s3_url_list = list()

            prop_json = {
                "attach": attach_s3_url_list
            }
        else:
            prop_json = {
                prop: self.xpath(xpath).text
            }

        return prop_json


test_module = TestModule()
test_module.start()
test_module.close()
