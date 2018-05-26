#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
import requests
import time
import os
import random
from urllib import parse


def get_json_data(offset):
    kw = '街拍'
    params = {
        'offset': offset,
        'format': 'json',
        'keyword': kw,
        'autoload': 'true',
        'count': '20',
        'cur_tab': '1',
        'from': 'search_tab'
        }
    headers = {
        'accept': 'application/json, text/javascript',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': 'tt_webid=6559429302055470605; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6559429302055470605; '
                  'UM_distinctid=163965e320e2b1-0b5e377a651d95-1b1b7758-144000-163965e320f261; '
                  'CNZZDATA1259612802=1633905207-1527230959-%7C1527230959; __tasessionId=yvvleu68e1527236146235',
        'referer': 'https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/68.0.3423.2 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    url = 'https://www.toutiao.com/search_content/?' + parse.urlencode(params)
    try:
        time.sleep(random.uniform(0.5, 1.5))
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            return resp.json()
    except ConnectionError:
        return None


def get_pic_url(json):
    if json.get('data'):
        for data in json.get('data'):
            if data.get('title'):
                title = data.get('title')
                pic_url = []
                for url in data.get('image_list'):
                    pic_url.append(url.get('url'))
                yield {
                    'title': title,
                    'url': pic_url
                }
    if json.get('return_count') == 0:
        yield {'title': None}


def save_pic(file_title:str, pic_url:list):
    for url in pic_url:
        pic_name = url.split('/')[-1]
        save_path = os.getcwd() + '\\pic_1\\{}'.format(file_title)
        save_path = os.path.abspath(save_path)
        if os.path.exists(save_path) is False:
            os.makedirs(save_path)
        try:
            resp = requests.get('http:' + url)
            if resp.status_code == 200:
                with open('{}\\{}.jpg'.format(save_path, pic_name), 'ab+') as pic_write:
                    pic_write.write(resp.content)
        except requests.ConnectionError:
            print("{}\n{}无法获取此图片，保存失败!".format(file_title, url))

def main():
    start_time = time.time()
    INIT_PAGE = 50
    offset_list = ([x * 20 for x in range(0, INIT_PAGE)])
    for offset in offset_list:
        json = get_json_data(offset)
        for info in get_pic_url(json):
            if info['title'] is not None:
                save_pic(info['title'], info['url'])
            else:
                print('offset={},已获取完街拍图片'.format(offset))
                break
            break
        break
    used_time = time.time() - start_time
    print("图片保存路径:", os.getcwd())
    print('耗费时间:', used_time)

if __name__ == '__main__':
    main()



# 不加多线程时间 181.3823745250702
# 多线程：耗费时间: 59.359395027160645