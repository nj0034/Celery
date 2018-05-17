import json
import os
import requests
from PIL import Image


def post_store(post):
    LUNA_PACIFIC_ENDPOINT = "https://luna.devhi.me/pacific/post_store"
    LUNA_TEST_PACIFIC_ENDPOINT = "https://toast-test.devhi.me/pacific/post_store"

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

    request_post(LUNA_PACIFIC_ENDPOINT, output, post)
    request_post(LUNA_TEST_PACIFIC_ENDPOINT, output, post)

    for file in post.files.values():
        os.remove(file)


def request_post(ENDPOINT, output, post):
    if post.files:
        post.files = {key: value for key, value in post.files.items() if value}
        files = {
            "poster": open(post.files['poster'], 'rb'),
            "thumbnail": open(post.files['thumbnail'], 'rb')
        }
        output.update({"files": files})

    res = requests.post(ENDPOINT, **output)
    if res:
        res = json.loads(res.text)
        print("Response of post_store : ", res)


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
            "poster": filepath,
            "thumbnail": thumbnail_filepath
        }

        return files_json
        # return open(filepath, 'rb')
        # return filepath
    except:
        return None


def resize_thumbnail(filepath, thumbnail_filepath):
    thumbnail_img = Image.open(filepath)
    new_width = 400
    wpercent = (new_width / float(thumbnail_img.size[0]))
    new_height = int((float(thumbnail_img.size[1]) * float(wpercent)))
    thumbnail_img.thumbnail((new_width, new_height), Image.ANTIALIAS)
    thumbnail_img = thumbnail_img.convert("RGB")
    thumbnail_img.save(thumbnail_filepath, quailty=60)

