import json
import os
import requests
from PIL import Image


def recruit_store(recruit):
    LUNA_PACIFIC_ENDPOINT = "https://luna.devhi.me/pacific/recruit_store"
    LUNA_TEST_PACIFIC_ENDPOINT = "https://toast-test.devhi.me/pacific/recruit_store"

    body = {
        "company": recruit.company,
        "field": recruit.field,
        "recruitment_type": recruit.recruitment_type,
        "start_date": recruit.start_date,
        "end_date": recruit.end_date,
        "parsing_url": recruit.url,
        "home_url": recruit.home_url,
    }

    output = {"data": body}
    # recruit.files = {key: value for key, value in recruit.files.items() if value}

    if recruit.files:
        recruit.files = {key: value for key, value in recruit.files.items() if value}
        files = {
            "detail_img": open(recruit.files.get('detail_img', None), 'rb'),
            "thumbnail": open(recruit.files['thumbnail'], 'rb')
        }

        output.update({"files": files})

    # request_post(LUNA_PACIFIC_ENDPOINT, output)
    request_post(LUNA_TEST_PACIFIC_ENDPOINT, output)

    # for file in recruit.files.values():
    #     os.remove(file)


def request_post(ENDPOINT, output):
    res = requests.post(ENDPOINT, **output)
    if res:
        res = json.loads(res.text)
        print("Response of recruit_store : ", res)


def download(url, filename):
    res = requests.get(url, stream=True)
    with open(filename, "wb") as file:
        for chunk in res:
            file.write(chunk)


def download_to_temp(detail_img_url, thumbnail_url):
    # if not url:
    #     return None
    try:
        if detail_img_url:
            filename = detail_img_url.split('/')[-1]
            filepath = '/home/ec2-user/Celery/parsing_celery/parsing/tmp/%s' % filename
            download(detail_img_url, filepath)
        else:
            filepath = None

        thumbnail_filepath = '/home/ec2-user/Celery/parsing_celery/parsing/tmp/%s' % 'thumbnail.jpg'
        download(thumbnail_url, thumbnail_filepath)

        files_json = {
            # "detail_img": open(filepath, 'rb'),
            # "thumbnail": open(thumbnail_filepath, 'rb')
            "detail_img": filepath,
            "thumbnail": thumbnail_filepath
        }

        return files_json
    except:
        return None
