#!/usr/bin/env python3
# coding=utf-8

"""
@Author：seeker0720
@File：run.py
@Date：2019/9/28 0:30
@Instruction：爬取豆瓣top250电影，同步，速度很慢,
下载全部的电影海报用时100s左右
"""
import requests
from bs4 import BeautifulSoup
import os, sys
import re
import time


def logger(func):
    def wrapper(*args, **kw):
        print('Please wait a minutes...')
        func(*args, **kw)
        print('Download successfully !')
    return wrapper


def timer(func):
    def wrapper(*args, **kw):
        start_time = time.time()
        func(*args, **kw)
        end_time = time.time()
        cost_time = end_time - start_time
        print(f'用时：{cost_time} s')
    return wrapper


def get_movie_info_tags(urls):
    rank_value_list = []
    title_list = []
    rating_num_list = []
    img_src_list = []
    quote_list = []

    for url in urls:
        # 发送请求，获得网页
        try:
            web_data = requests.get(url)
        except Exception as e:
            print(f'WARNING: {e}')
        else:
            print(f'200 : {url} ')
            # 解析网页
            soup = BeautifulSoup(web_data.text, 'lxml')
            # 将所需要的信息提取到列表中
            rank_value_list.extend(soup.select('div.pic > em'))
            title_list.extend((soup.select('div.hd > a')))
            rating_num_list.extend(soup.select('span.rating_num'))
            img_src_list.extend(soup.select('img[width="100"]'))
            quote_list.extend(soup.select('span.inq'))
    return rank_value_list,title_list, rating_num_list, img_src_list, quote_list


def get_movie_info(urls):
    rank_value_list, title_list, rating_num_list, img_src_list, quote_list = get_movie_info_tags(urls)
    movie_info_list = []
    img_url_list = []

    for rank_value, title, rating_num, img_src, quote in zip(rank_value_list,
                                                            title_list,
                                                            rating_num_list,
                                                            img_src_list,
                                                            quote_list):
        rank_value = rank_value.get_text()
        movie_title = list(title.stripped_strings)
        rate_num = rating_num.get_text()
        img_url = img_src.get('src')
        quote = quote.get_text()
        movie_url = title.get('href')

        movie_info = f'[{rank_value}、{movie_title[0]} {rate_num}]({movie_url})——{quote}'

        movie_info_list.append(movie_info)
        img_url_list.append(img_url)
    return movie_info_list, img_url_list


@logger
@timer
def download_movie_info(urls):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(BASE_DIR)

    fi = open(f'{BASE_DIR}\docs\豆瓣电影top250.md', 'w', encoding='utf8')
    movie_info_list, img_url_list = get_movie_info(urls)

    for movie_info, img_url in zip(movie_info_list, img_url_list):
        info = f'{movie_info}\n\n![]({img_url})\n\n'
        # 将电影信息的写入到markdown文件
        fi.write(info)
        # 下载电影的海报
        img_title = re.sub('[\[,\]]', '', re.findall('\[.*\]', movie_info)[0])
        try:
            img = requests.get(img_url)
        except Exception as e:
            print(f'Error: {e}')
        else:
            with open(f'{BASE_DIR}\download\pictures\\{img_title}.jpg', 'wb') as f:
                f.write(img.content)
            print(f'{img_title}  ...')
    fi.close()


if __name__ == '__main__':
    url_list = ['https://movie.douban.com/top250?start=' + str(i) +
                '&filter' for i in range(0, 250, 25)]
    # print('Please wait a minutes...')

    download_movie_info(urls=url_list)



