from sailer.sailer import Sailer
from sailer.pacific import *
from sailer.utils import *
import random
import time
from .notice_common import *

XPATH_JSON = {
    "parsing_method": "url_based / next_button / ",
    "host": "",
    "page_url": "",
    "category": "category",
    "start_page": 1,
    "props": {
        "title": {
            "xpath": "",
            "url_xpath": "",
            "position": "in",
        },
        "number": {
            "xpath": "",
            "position": "out",
        },
        "date": {
            "xpath": "",
            "format": "",
            "position": "in",
        },
        "writer": {
            "type": "xpath",
            "xpath": "",
            "position": "in",
        },
        "hit": {
            "xpath": "",
            "position": "in",
        },
        "content": {
            "xpath": "",
            "position": "in",
        },
        "img": {
            "xpath": "",
            "position": "in",
        },
        "attach": {
            "xpath": "",
            "position": "in",
            "name_regex": "",
            "HTML_xpath": "",
        }
    }
}


class TestModule(Sailer):
    def start(self):
        self.category = XPATH_JSON['category']
        self.top = False
        parsing_method = XPATH_JSON['parsing_method']
        if parsing_method == 'url_based':
            start_page = XPATH_JSON['start_page']
            for i in range(start_page, 100):
                page_url = XPATH_JSON.get('page_url').format(page=i)
                self.go(page_url)
                print("# {} page start".format(i + 1))
                self.url_based()
        elif parsing_method == 'next_button':
            page_url = XPATH_JSON.get('page_url')
            self.go(page_url)
            self.next_button()
        else:
            pass

    def next_button(self):
        in_prop_list = XPATH_JSON['props'].keys()
        top_article_url = self.xpath(XPATH_JSON['top_article_xpath']).get_attribute('href')
        self.go(top_article_url)

        while (True):
            parsing_result_json_list = [{"url": self.current_url}]
            parsing_result_json_list = self.parsing_in_prop(in_prop_list, parsing_result_json_list)

            next_button_url = self.xpath(XPATH_JSON['next_button_xpath']).get_attribute('href')
            if next_button_url:
                self.go(next_button_url)
            else:
                break

    def url_based(self):
        props = XPATH_JSON['props']
        out_prop_list = list()
        in_prop_list = list()
        for key, value in props.items():
            if value['position'] == 'out':
                out_prop_list.append(key)
            else:
                in_prop_list.append(key)

        title_url_xpaths = self.xpaths(props['title']['url_xpath'])
        parsing_result_json_list = [{"url": title_url_xpath.get_attribute('href')} for title_url_xpath in
                                    title_url_xpaths]

        for out_prop in out_prop_list:
            xpath_list = self.xpaths(props[out_prop]['xpath'])
            for xpath, parsing_result_json in zip(xpath_list, parsing_result_json_list):
                parsing_result_json.update({out_prop: xpath.text})

        parsing_result_json_list = self.parsing_in_prop(in_prop_list, parsing_result_json_list)

        # es에 저장(top 글이면 저장 안함)
        time.sleep(random.randrange(5, 10))

        self.top = True

    def parsing_in_prop(self, in_prop_list, parsing_result_json_list):
        props = XPATH_JSON['props']
        for parsing_result_json in parsing_result_json_list:
            self.go(parsing_result_json['url'])
            for in_prop in in_prop_list:
                xpath = props[in_prop]['xpath']

                if in_prop == 'content':
                    in_prop_json = {
                        "content_text": self.xpath(xpath).text,
                        "content_HTML": self.xpath(xpath).get_attribute('innerHTML'),
                    }
                elif in_prop == 'date':
                    date = self.xpath(xpath).text
                    format = props[in_prop]['format']
                    date = convert_datetime(date, format, '%Y-%m-%d %H:%M:%S')
                    in_prop_json = {
                        "date": date
                    }
                elif in_prop == 'img':
                    img_url_list = [xpath.get_attribute('src') for xpath in self.xpaths(xpath) if xpath]

                    # s3에 저장하는 함수 넣기 + s3 url list 만들기
                    img_s3_url_list = list()

                    in_prop_json = {
                        "img": img_s3_url_list
                    }
                elif in_prop == 'attach':
                    attach_url_list = [xpath.get_attribute('href') for xpath in self.xpaths(xpath) if xpath]
                    attach_name_list = re.findall(props[in_prop]['name_regex'],
                                                  self.xpath(props[in_prop]['HTML_xpath']).get_attribute('innerHTML'))

                    # s3에 저장하는 함수 넣기 + s3 url list 만들기
                    attach_s3_url_list = list()

                    in_prop_json = {
                        "attach": attach_s3_url_list
                    }
                else:
                    in_prop_json = {
                        in_prop: self.xpath(xpath).text
                    }

                parsing_result_json.update(in_prop_json)

        return parsing_result_json_list


test_module = TestModule()
test_module.start()
test_module.close()
