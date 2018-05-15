import json

import os
import requests
from sailer.sailer import Sailer
from sailer.pacific import *
from sailer.utils import *
import re
from bs4 import BeautifulSoup


LUNA_PACIFIC_ENDPOINT = "https://luna.devhi.me/pacific/article/notice"
LUNA_TEST_PACIFIC_ENDPOINT = "https://toast-test.devhi.me/pacific/article/notice"
#LUNA_PACIFIC_ENDPOINT = "http://13.125.125.118:8000/pacific/article/notice"

def notice_store(notice):

    if datetime.strptime(notice.date, "%Y-%m-%d %H:%M:%S") < datetime(year=2018, month=5, day=1):
        if notice.number != 'top':
            print(notice.date)
            print("parsing quit")
            quit()

    body = {
        "no": notice.number,
        "title": notice.sub,
        "content": notice.content,
        "hit": notice.hit,
        "writer": notice.writer,
        "url": notice.url,
        "created_at": notice.date,
        "category": notice.category,
    }

    output = {"data": body}

    request_post(LUNA_PACIFIC_ENDPOINT, output, notice)
    request_post(LUNA_TEST_PACIFIC_ENDPOINT, output, notice)


def request_post(ENDPOINT, output, notice):
    res = requests.post(ENDPOINT, **output)
    if res:
        res = json.loads(res.text)
        print("Response of notice_store : ", res)

        if res.get('uuid', ''):
            if notice.img_url:
                converted_img_content = notice.content
                # img_src_list = re.findall(r'<img.*src="(?P<url>.*)"\s', converted_img_content)
                content_html = BeautifulSoup(converted_img_content, "html.parser")
                img_list = content_html.find_all('img')
                img_src_list = [img.get('src') for img in img_list]

                for img_src, img_url in zip(img_src_list, notice.img_url):
                    s3_img_url = download_to_temp(ENDPOINT, img_url, res['uuid'], '')
                    converted_img_content = re.sub(img_src, s3_img_url, converted_img_content)
                data = {
                    "uuid": res['uuid'],
                    "content": converted_img_content
                }
                requests.post(ENDPOINT + '/modify', data=data)

            for attach_url, attach_name in zip(notice.attach_url, notice.attach_name):
                download_to_temp(ENDPOINT, attach_url, res['uuid'], attach_name)



def store_file(ENDPOINT, **kwargs):
    body = {
        "uuid": kwargs['uuid']
    }
    files = {
        "upload_file": kwargs['file']
    }

    output = {"data": body, "files": files}

    res = requests.post(ENDPOINT + "/file", **output)
    if res:
        res = json.loads(res.text)
        print("Response of store_file : ", res)
        return res.get('url', '')


def download_to_temp(ENDPOINT, url, uuid, name):
    # if not url:
    #     return None
    try:
        if name:
            filename = name
        else:
            filename = url.split('/')[-1]
        filepath = r'/home/ec2-user/Celery/parsing_celery/parsing/tmp/%s' % filename
        download(url, filepath)
        s3_url = store_file(ENDPOINT, uuid=uuid, file=open(filepath, 'rb'))
        os.remove(filepath)
        return s3_url
    except:
        return None


def download(url, filename):
    res = requests.get(url, stream=True)
    with open(filename, "wb") as file:
        for chunk in res:
            file.write(chunk)


def notice_attach_url(file_hrefs):
    attach_url_form = 'http://www.skku.edu/new_home/campus/skk_comm/notice_download_hp.jsp?userfile={}'
    attach_url = list()

    for file_href in file_hrefs:
        file_name = file_href.split('\'')[1]
        attach_url.append(attach_url_form.format(file_name))

    return attach_url


def ptag_img_regex(html):
    regex = re.compile(r'<p.*\s*.*<img.*src="(?P<img_url>.*)"\s')
    return regex.search(html).group("img_url")
