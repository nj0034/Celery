import json

import os
import requests


def post_store(post):
    LUNA_PACIFIC_ENDPOINT = "https://luna.devhi.me/pacific/post_store"

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

    res = requests.post(LUNA_PACIFIC_ENDPOINT, **output)
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
        download(url, filepath)
        return open(filepath, 'rb')
    except:
        return None
