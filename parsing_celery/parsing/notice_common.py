import json

import os
import requests
from sailer.sailer import Sailer
from sailer.pacific import *
from sailer.utils import *
import re


def notice_store(notice):
    LUNA_PACIFIC_ENDPOINT = "https://luna.devhi.me/pacific/article/notice"

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

    res = requests.post(LUNA_PACIFIC_ENDPOINT, **output)
    if res:
        res = json.loads(res.text)
        print("Response of notice_store : ", res)

        if res['uuid']:
            for img_url in notice.img_url:
                s3_img_url = download_to_temp(img_url, res['uuid'], '')
                notice.content.replace('img_url', s3_img_url)

            print(notice.content)

            for attach_url, attach_name in zip(notice.attach_url, notice.attach_name):
                download_to_temp(attach_url, res['uuid'], attach_name)


def store_file(**kwargs):
    LUNA_PACIFIC_STOREFILE_ENDPOINT = "https://luna.devhi.me/pacific/article/notice/file"
    #LUNA_PACIFIC_STOREFILE_ENDPOINT = "http://13.125.125.118:8000/pacific/article/notice/file"

    body = {
        "uuid": kwargs['uuid']
    }
    files = {
        "upload_file": kwargs['file']
    }

    output = {"data": body, "files": files}

    res = requests.post(LUNA_PACIFIC_STOREFILE_ENDPOINT, **output)
    if res:
        res = json.loads(res.text)
        print("Response of store_file : ", res)
        return res.get('url', '')


def download_to_temp(url, uuid, name):
    # if not url:
    #     return None
    try:
        if name:
            filename = name
        else:
            filename = url.split('/')[-1]
        filepath = r'/home/ec2-user/Celery/parsing_celery/parsing/tmp/%s' % filename
        download(url, filepath)
        s3_url = store_file(uuid=uuid, file=open(filepath, 'rb'))
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
