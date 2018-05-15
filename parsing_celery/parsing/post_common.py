import json
import os
import requests
from PIL import Image


def post_store(post):
    LUNA_PACIFIC_ENDPOINT = "https://luna.devhi.me/pacific/post_store"
    LUNA_TEST_PACIFIC_ENDPOINT = "https://toast-test.devhi.me/pacific/article/post_store"

    body = {
        "title": post.sub,
        "url": post.home_url,
        "host": post.host,
        "start_date": post.start_date,
        "end_date": post.end_date,
        "target": post.target,
        "benefit": post.benefit,
        "parsed_content": post.detail,
        "parsing_url": post.url,
    }

    output = {"data": body}
    post.files = {key: value for key, value in post.files.items() if value}

    if post.files:
        output.update({"files": post.files})

    request_post(LUNA_PACIFIC_ENDPOINT, output, post)
    request_post(LUNA_TEST_PACIFIC_ENDPOINT, output, post)


def request_post(ENDPOINT, output, post):
    res = requests.post(ENDPOINT, **output)
    if res:
        res = json.loads(res.text)
        print("Response of post_store : ", res)

    for file in post.files.values():
        os.remove(file.name)
    return res


def download(url, filename):
    res = requests.get(url, stream=True)
    with open(filename, "wb") as file:
        for chunk in res:
            file.write(chunk)


def download_to_temp(url):
    # if not url:
    #     return None
    try:
        filename = url.split('/')[-1]
        filepath = '/home/ec2-user/Celery/parsing_celery/parsing/tmp/%s' % filename
        thumbnail_filepath = '/home/ec2-user/Celery/parsing_celery/parsing/tmp/%s' % filename.split('.')[0] + '_thumbnail.jpg'

        download(url, filepath)
        resize_thumbnail(filepath, thumbnail_filepath)

        files_json = {
            "poster": open(filepath, 'rb'),
            "thumbnail": open(thumbnail_filepath, 'rb')
        }

        return files_json
        # return open(filepath, 'rb')
        # return filepath
    except:
        return None


def resize_thumbnail(filepath, thumbnail_filepath):
    thumbnail_img = Image.open(filepath)
    new_width = 680
    wpercent = (new_width / float(thumbnail_img.size[0]))
    new_height = int((float(thumbnail_img.size[1]) * float(wpercent)))
    thumbnail_img.thumbnail((new_width, new_height), Image.ANTIALIAS)
    thumbnail_img.save(thumbnail_filepath, quailty=60)

